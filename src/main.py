from fastapi import FastAPI
from pydantic import BaseModel
from src.bot.response import answer_with_dynamic_schema

app = FastAPI()

# Modelo de petición para la función execute
class ExecuteRequest(BaseModel):
    question: str

@app.post("/execute")
async def execute(request: ExecuteRequest):
    return answer_with_dynamic_schema(request.question)
