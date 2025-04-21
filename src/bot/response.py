import os
import json
from openai import OpenAI

# 1) Inicializar cliente con la API Key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def infer_json_schema_from_example(example):
    """
    Genera recursivamente un JSON Schema a partir de un ejemplo de objeto.
    """
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

def answer_with_dynamic_schema(question: str):
    """
    1. Llama a suggest_presentation_formats para obtener opciones.
    2. Construye un JSON Schema basado en la opción elegida.
    3. Fuerza una segunda llamada al endpoint dinámico usando client.chat.completions.create.
    """
    # Esquema de la primera función
    suggestion_schema = {
        "name": "suggest_presentation_formats",
        "description": "Genera opciones creativas para presentar la solución.",
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
                            "type": {"type": "string"},
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
    suggest_resp = client.chat.completions.create(
        model="o1-mini",
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
    func = suggest_resp.choices[0].message.function_call
    opts = json.loads(func.arguments)["options"]
    chosen = opts[0]  # Puedes cambiar la lógica de selección
    payload_example = chosen["payload"]

    # === Construir schema dinámico para la segunda función ===
    dynamic_schema = {
        "name": f"execute_{chosen['type']}",
        "description": f"Presenta el resultado usando el formato «{chosen['title']}».",
        "parameters": infer_json_schema_from_example(payload_example)
    }

    # === Segunda llamada: ejecutar según schema generado ===
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
    final_call = final_resp.choices[0].message.function_call
    final_payload = json.loads(final_call.arguments)

    return {
        "chosen_option": chosen,
        "final_payload": final_payload
    }