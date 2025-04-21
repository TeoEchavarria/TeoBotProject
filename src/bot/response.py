import os
import json
import logging
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 1) Inicializar cliente con la API Key
try:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    raise

def infer_json_schema_from_example(example):
    """
    Genera recursivamente un JSON Schema a partir de un ejemplo de objeto.
    """
    try:
        logger.debug(f"Inferring schema from example of type: {type(example)}")
        if isinstance(example, str):
            return {"type": "string"}
        if isinstance(example, bool):
            return {"type": "boolean"}
        if isinstance(example, int):
            return {"type": "integer"}
        if isinstance(example, float):
            return {"type": "number"}
        if isinstance(example, list):
            items = infer_json_schema_from_example(example[0]) if example else {}
            return {"type": "array", "items": items}
        if isinstance(example, dict):
            props, req = {}, []
            for k, v in example.items():
                props[k] = infer_json_schema_from_example(v)
                req.append(k)
            return {"type": "object", "properties": props, "required": req}
        return {}
    except Exception as e:
        logger.error(f"Error inferring JSON schema: {e}")
        raise

def answer_with_dynamic_schema(question: str):
    """
    1. Llama a suggest_presentation_formats para obtener opciones.
    2. Construye un JSON Schema basado en la opción elegida.
    3. Fuerza una segunda llamada al endpoint dinámico usando client.chat.completions.create.
    """
    try:
        logger.info(f"Processing question: {question[:50]}...")
        
        # Esquema de la primera función
        suggestion_schema = {
            "name": "suggest_presentation_formats",
            "description": "Generate creative options for presenting the solution. Use camelcase for titles, parameter descriptions should be short and concise.",
            "parameters": {
                "type": "object",
                "properties": {
                    "options": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "description": {"type": "string"},
                                "type": {"type": "string", "enum": ["string", "object", "array", "integer"]},
                                "payload": {"type": "object"}
                            },
                            "required": ["title", "description", "type", "payload"]
                        }
                    }
                },
                "required": ["options"]
            }
        }

        # === Primera llamada: obtener opciones ===
        logger.info("Making first API call to get presentation options")
        try:
            suggest_resp = client.chat.completions.create(
                model="o3-mini-2025-01-31",
                messages=[
                    {"role":"system","content":(
                        "Eres un asistente creativo. Recibe la pregunta y llama **solo** a "
                        "'suggest_presentation_formats' con un array 'options'."
                    )},
                    {"role":"user","content":question}
                ],
                functions=[suggestion_schema],
                function_call={"name":"suggest_presentation_formats"}
            )
            logger.info("First API call successful")
        except Exception as e:
            logger.error(f"First API call failed: {e}")
            raise

        try:
            func = suggest_resp.choices[0].message.function_call
            opts = json.loads(func.arguments)["options"]
            logger.info(f"Received {len(opts)} presentation options")
            chosen = opts[0]  # Puedes cambiar la lógica de selección
            logger.info(f"Selected option: {chosen['title']}")
            payload_example = chosen["payload"]
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.error(f"Error processing first API response: {e}")
            logger.debug(f"Response content: {suggest_resp}")
            raise

        # === Construir schema dinámico para la segunda función ===
        try:
            logger.info("Building dynamic schema based on selected option")
            dynamic_schema = {
                "name": f"execute_{chosen['type']}",
                "description": f"Presenta el resultado usando el formato «{chosen['title']}».",
                "parameters": infer_json_schema_from_example(payload_example)
            }
            logger.debug(f"Dynamic schema created: {json.dumps(dynamic_schema)[:200]}...")
        except Exception as e:
            logger.error(f"Error building dynamic schema: {e}")
            raise

        # === Segunda llamada: ejecutar según schema generado ===
        logger.info("Making second API call with dynamic schema")
        try:
            final_resp = client.chat.completions.create(
                model="gpt-4o-search-preview",
                messages=[
                    {"role":"system","content":(
                        "Ahora llama **solo** la función dinámica según el schema proporcionado."
                    )},
                    {"role":"user","content":question}
                ],
                functions=[dynamic_schema],
                function_call={"name":dynamic_schema["name"]}
            )
            logger.info("Second API call successful")
        except Exception as e:
            logger.error(f"Second API call failed: {e}")
            raise

        try:
            final_call = final_resp.choices[0].message.function_call
            final_payload = json.loads(final_call.arguments)
            logger.info("Successfully parsed final response")
        except (AttributeError, json.JSONDecodeError) as e:
            logger.error(f"Error processing second API response: {e}")
            logger.debug(f"Response content: {final_resp}")
            raise

        logger.info("Processing completed successfully")
        return {
            "chosen_option": chosen,
            "final_payload": final_payload
        }
    
    except Exception as e:
        logger.error(f"Uncaught exception in answer_with_dynamic_schema: {e}", exc_info=True)
        # You might want to return a fallback response instead of re-raising
        return {
            "error": str(e),
            "status": "failed"
        }