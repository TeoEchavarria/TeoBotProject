import re
from typing import Dict, Any

def normalize_key(title: str) -> str:
    """Convert a human title into snake_case without accents."""
    s = (title.lower()
         .replace("á","a").replace("é","e")
         .replace("í","i").replace("ó","o")
         .replace("ú","u").replace("ñ","n"))
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")

def format_response_keys(data: dict) -> dict:
    """
    Transforms a dictionary by using the first value as the key,
    and joining all remaining values as a string for the value.
    """
    # If the dictionary is empty, return an empty dictionary
    if not data:
        return {}
    
    # Get all values as a list
    values = list(data.values())
    
    # If there are no values, return an empty dictionary
    if not values:
        return {}
    
    # Use the first value as the new key
    new_key = str(values[0])
    
    # Join the rest of the values as a single string value
    new_value = "\n".join(str(v) for v in values[1:]) if len(values) > 1 else ""
    
    # Return a new dictionary with single entry: first value as key, rest joined as value
    return {new_key: new_value}

def process_hints_dictionary(data: dict) -> dict:
    result = {}
    
    for hint in data.get("hints", []):
        # Extract fields
        title = hint.get("title", "")
        question = hint.get("question", "")
        
        # Get answer components
        answer = hint.get("answer", {})
        summary = answer.get("summary", "")
        explanation = answer.get("explanation", "")
        example = answer.get("example", "")
        
        # Create key using normalize_key function
        key = f"{title} {question}"
        
        # Create value by combining all answer components
        value = f"{summary} {explanation} {example}"
        
        # Add to result dictionary
        result[key] = value
    
    return result

def format_answer_with_parsed_json(json, step_by_step : bool) -> Dict[str, Any]:
    # ...existing code...
    
    # --- Consolidate result -----------------------------------------------
    if step_by_step:
        return process_hints_dictionary(json)
    else:
        return format_response_keys(json)