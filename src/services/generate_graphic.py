import openai  # type: ignore
import tempfile, textwrap, traceback, uuid, contextlib, io, types as _types
import os
from pathlib import Path
from typing import Any, Dict

def chart_code(
    requirement: str,
    *,
    viz_library: str = "matplotlib",
    model: str = "gpt-4o-mini",
    temperature: float = 0.4,
    max_attempts: int = 3,
    out_path: Path | str | None = None,
) -> Path:

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Define OPENAI_API_KEY env var before calling chart_code()")

    openai.api_key = api_key

    if out_path is None:
        out_path = Path(tempfile.gettempdir()) / f"chart_{uuid.uuid4().hex}.png"
    else:
        out_path = Path(out_path)

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
        response = openai.ChatCompletion.create(
            model=model,
            temperature=temperature,
            messages=messages,
        )
        code: str = response.choices[0].message.content.strip()

        # Create an execution namespace with OUTPUT_PATH injected
        exec_globals: Dict[str, Any] = {"OUTPUT_PATH": str(out_path)}
        try:
            exec(code, exec_globals)
            if not out_path.exists():
                raise RuntimeError("Code executed without errors but image was not saved to OUTPUT_PATH")
            return out_path
        except Exception as e:  # pragma: no cover
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

    # Should not reach here
    raise RuntimeError("OpenAI did not return valid code after retries")
