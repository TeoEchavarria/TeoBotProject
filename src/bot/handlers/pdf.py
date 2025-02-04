import tempfile, zipfile, PyPDF2, os
from datetime import datetime

from src.bot.response import generate_answer
from src.utils.mongodb import find_one
from src.document_processing.create_zip import create_zip_from_notes

from telegram import Update
from telegram.ext import CallbackContext

async def handle_pdf(update: Update, context: CallbackContext) -> None:
    document = update.message.document

    if document.mime_type != 'application/pdf':
        await update.message.reply_text("Por favor, envíame un archivo PDF.")
        return

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
        pdf_path = tmp_pdf.name

    file_obj = await document.get_file()
    await file_obj.download_to_drive(custom_path=pdf_path)

    try:
        pdf_text = ""
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pdf_text += text

        if not pdf_text:
            await update.message.reply_text("No se pudo extraer texto del PDF.")
            return

        user = find_one("users", {"_id": update.message.from_user.username})
        openai_key = user["openai_key"]

        try:
            results = generate_answer(context=None, question=pdf_text, openai_key=openai_key, mode="pdf_extract")
        except Exception as e:
            await update.message.reply_text("Error generating the response")
            return

        if not results:
            await update.message.reply_text("No results were generated.")
            return
        
        notes = {}
        try:
            for note in results["notes"]:
                format = generate_answer(context=note["title"], question=note["description-note"], openai_key=openai_key, mode="note_create")
                format["key_points"] = "\n".join(f"- {point}" for point in format["key_points"])
                format["practical_examples"] = "\n".join(f">[!example] {example}" for example in format["practical_examples"])
                format["date"] = datetime.now().strftime("%d-%m-%Y")
                with open("src/core/formard.md", "r", encoding="utf8") as f:
                    template_md = f.read()
                formatted_note = template_md.format(**format)
                notes[format["title"].lower()] = formatted_note
                
        except Exception as e:
            print(f"Error generating the note: {note['title']}")
        


        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
            zip_path = create_zip_from_notes(notes)

        # with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        #     for filename, file_content in results.items():
        #         zipf.writestr(filename, file_content)

        with open(zip_path, "rb") as zip_file:
            await update.message.reply_document(document=zip_file, filename="resultados.zip", caption="Aquí están los archivos extraídos en formato .md")

    except Exception as e:
        await update.message.reply_text(f"Ocurrió un error: {e}")

    finally:
        # Limpiamos los archivos temporales
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        if 'zip_path' in locals() and os.path.exists(zip_path):
            os.remove(zip_path)
