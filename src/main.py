from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.services.response import answer_with_parsed_json
import logging

import base64

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
    #logger.info(f"Received request: {request}")
    return answer_with_parsed_json(**request.model_dump())
#     return {
#   "La oferta y la demanda son conceptos fundamentales en economía que interactúan para determinar el precio y la cantidad de bienes en un mercado. La oferta es la cantidad de un producto que los productores están dispuestos a vender a diferentes precios, mientras que la demanda es la cantidad que los consumidores están dispuestos a comprar. La relación entre ambas se ilustra a través de la ley de la oferta y la demanda, que sostiene que si la oferta de un bien supera la demanda, los precios tienden a bajar, y viceversa. En equilibrio, la cantidad ofrecida es igual a la cantidad demandada, estableciendo así el precio de mercado. Visualmente, se puede representar en un gráfico donde la curva de oferta asciende de izquierda a derecha y la curva de demanda desciende. El punto donde se cruzan ambas curvas es el punto de equilibrio.": "",
#   "search_video": [
#     "https://www.youtube.com/watch?v=G0T8xGu2NxY", "https://www.youtube.com/watch?v=G0T8xGu2NxY"
#   ],
#   "generate_image": [
#     base64.b64encode(open("/Users/teoechavarria/Documents/GitHub/TeoBotProject/output_chart.png", "rb").read()).decode('utf-8'),
#     base64.b64encode(open("/Users/teoechavarria/Documents/GitHub/TeoBotProject/output_chart.png", "rb").read()).decode('utf-8')
#   ],
#   "generate_graphic": [
#     base64.b64encode(open("/Users/teoechavarria/Documents/GitHub/TeoBotProject/cat.jpg", "rb").read()).decode('utf-8'),
#     base64.b64encode(open("/Users/teoechavarria/Documents/GitHub/TeoBotProject/cat.jpg", "rb").read()).decode('utf-8')
#   ]}