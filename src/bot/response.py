import os
import json
import openai
from typing import Any, Dict

# Configuración de la API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def infer_json_schema_from_example(example: Any) -> Dict:
    """
    Recursivamente genera un JSON Schema a partir de un ejemplo de payload.
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
        items_schema = infer_json_schema_from_example(example[0]) if example else {}
        return {"type": "array", "items": items_schema}
    if isinstance(example, dict):
        props = {}
        required = []
        for k, v in example.items():
            props[k] = infer_json_schema_from_example(v)
            required.append(k)
        return {
            "type": "object",
            "properties": props,
            "required": required
        }
    # Caso por defecto
    return {}

def answer_with_dynamic_schema(question: str) -> Dict:
    """
    Realiza dos llamadas a la API:
    1. Sugiere formatos de presentación (opciones).
    2. Construye un JSON Schema dinámico basado en el payload de la opción elegida,
       y fuerza al modelo a generar una respuesta acorde a ese schema.
    Retorna un dict con:
    - 'chosen_option'
    - 'final_payload' (los argumentos de la función generados en la segunda llamada)
    """
    # 1) Obtener sugerencias de formatos
    suggestion_schema = {
        "name": "suggest_presentation_formats",
        "description": "Genera una lista de formatos creativos y efectivos para presentar la solución a la pregunta dada.",
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

    suggest_resp = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": (
                "Eres un asistente creativo y conciso. Recibe la pregunta del usuario y devuelve **solo** "
                "la llamada a la función 'suggest_presentation_formats' con un array 'options'." 
            )},
            {"role": "user", "content": question}
        ],
        functions=[suggestion_schema],
        function_call={"name": "suggest_presentation_formats"}
    )

    # Parsear la respuesta de la sugerencia
    call = suggest_resp.choices[0].message["function_call"]
    args = json.loads(call["arguments"])
    options = args.get("options", [])
    if not options:
        raise ValueError("No se generaron opciones de presentación.")

    # Elegir la primera opción
    chosen = options[0]
    payload_example = chosen["payload"]

    # 2) Construir JSON Schema dinámico
    dynamic_schema = {
        "name": f"execute_{chosen['type']}",
        "description": f"Implementa la presentación usando el formato “{chosen['title']}”.",
        "parameters": infer_json_schema_from_example(payload_example)
    }

    # 2a) Hacer la segunda llamada forzada a la nueva función
    final_resp = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": (
                "Ahora genera **solo** la llamada a la función para presentar la respuesta final "
                "siguiendo el schema proporcionado en 'parameters'." 
            )},
            {"role": "user", "content": question}
        ],
        functions=[dynamic_schema],
        function_call={"name": dynamic_schema["name"]}
    )

    final_call = final_resp.choices[0].message["function_call"]
    final_args = json.loads(final_call["arguments"])

    return {
        "chosen_option": chosen,
        "final_payload": final_args
    }

# Ejemplo de uso
if __name__ == "__main__":
    pregunta = "¿Cómo funciona el efecto Doppler en el sonido?"
    resultado = answer_with_dynamic_schema(pregunta)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
