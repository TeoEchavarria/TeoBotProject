from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.services.response import answer_with_parsed_json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
     title="TeoBotProject API - Response BrainyTutor",
    version="1.1.0",
    description="API for TeoBotProject, a chatbot designed to assist users in learning and understanding complex topics through step-by-step guidance and suggestions.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de petición para la función execute
class ExecuteRequest(BaseModel):
    question: str
    step_by_step: bool = False
    profile: str = "default"

@app.post("/execute")
async def execute(request: ExecuteRequest):
    logger.info(f"Received request: {request}")
    return answer_with_parsed_json(**request.model_dump())