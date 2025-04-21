from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import tempfile, os, requests, PyPDF2

from src.bot.response import answer_with_dynamic_schema

app = FastAPI()

# Modelo de petición para la función execute
class ExecuteRequest(BaseModel):
    question: str

# Función auxiliar que delega a answer_with_dynamic_schema
def response_answer(question: str):
    return answer_with_dynamic_schema(question)

@app.post("/execute")
async def execute(request: ExecuteRequest):
    return response_answer(request.question)
