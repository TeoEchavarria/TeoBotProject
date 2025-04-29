import traceback
import os, logging, base64
from typing import Any, Dict
from openai import OpenAI

def chart_code(
    requirement: str,
    *,
    viz_library: str = "matplotlib",
    model: str = "o3-mini-2025-01-31",
    max_attempts: int = 3,
    out_path: str = "temp_chart.png",
):

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Define OPENAI_API_KEY env var before calling chart_code()")

    client = OpenAI(api_key=api_key)
    print(f"API Key: {api_key}")

    base_system = (
        "You are a senior data‑visualization engineer. "
        "Generate runnable Python code that uses {lib} and saves the final chart as a PNG at the path held in the variable OUTPUT_PATH. "
        "The code must: (1) include all necessary imports, (2) create or load data, (3) save the figure with fig.savefig(OUTPUT_PATH, dpi=300, bbox_inches='tight'), "
        "and (4) not print or display anything else. Do NOT wrap code in triple backticks—return code only."
    ).format(lib=viz_library)

    messages = [
        {"role": "system", "content": base_system},
        {"role": "user", "content": f"Requirement: {requirement}"},
    ]

    for attempt in range(1, max_attempts + 1):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        code: str = response.choices[0].message.content.strip()
        # Create an execution namespace with OUTPUT_PATH injected
        exec_globals: Dict[str, Any] = {"OUTPUT_PATH": str(out_path)}
        try:
            exec(code, exec_globals)
            if not exec_globals.get("OUTPUT_PATH"):
                raise RuntimeError("Code executed without errors but image was not saved to OUTPUT_PATH")
            return base64.b64encode(open(exec_globals['OUTPUT_PATH'], 'rb').read()).decode()
        except Exception as e:  # pragma: no cover
            logging.error(f"Attempt {attempt} failed: {e}")
            tb = traceback.format_exc()
            if attempt == max_attempts:
                raise RuntimeError(f"Failed after {max_attempts} attempts. Last error:\n{tb}") from e
            # Append error feedback and retry
            messages.append(
                {
                    "role": "assistant",
                    "content": code,
                }
            )
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "The previous code raised this exception. Please fix it and resend complete code only.\n\n" + tb
                    ),
                }
            )
        finally:
            # Clean up the generated file if it exists
            if os.path.exists(out_path):
                os.remove(out_path)

    # Should not reach here
    raise RuntimeError("OpenAI did not return valid code after retries")