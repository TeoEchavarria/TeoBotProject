from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import tempfile, os, requests, PyPDF2

from src.utils.mongodb import add_or_update_key, find_one, insert, update_one
from src.services.embeddings.embedder import get_embedding
from src.services.embeddings.pinecone import upsert_embeddings_to_pinecone
from src.bot.response import generate_answer
from src.bot.response_flow import response_flow
from src.document_processing.create_zip import create_zip_from_notes

app = FastAPI()
