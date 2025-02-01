import os
import tempfile
from telegram import Update
from telegram.ext import ContextTypes
from openai import OpenAI
from pydub import AudioSegment

async def transcribe_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    file_id = update.message.voice.file_id
    voice_file = await context.bot.get_file(file_id)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    with tempfile.NamedTemporaryFile(delete=True, suffix=".ogg") as tf:
        await voice_file.download_to_drive(tf.name)
        tf.seek(0)
        audio = AudioSegment.from_file(tf.name)
        duration_ms = len(audio)
        duration_seconds = duration_ms / 1000
        
        try:
            with open(tf.name, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["word"]
                )
            return transcript.text, duration_seconds
        except Exception as e:
            raise RuntimeError("Could not transcribe the audio.")