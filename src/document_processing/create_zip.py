import tempfile
import zipfile

def create_zip_from_notes(notes: dict) -> str:
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip_file:
        zip_path = tmp_zip_file.name

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for filename, content in notes.items():
            safe_filename = f"{filename}.md" if not filename.endswith(".md") else filename
            zipf.writestr(safe_filename, content)

    return zip_path