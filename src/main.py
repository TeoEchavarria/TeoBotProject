from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.bot.response import answer_with_parsed_json

app = FastAPI()

# Configuración CORS
origins = [
    "http://localhost",
    "http://localhost:9002",
    # añade aquí otros orígenes permitidos
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de petición para la función execute
class ExecuteRequest(BaseModel):
    question: str

@app.post("/execute")
async def execute(request: ExecuteRequest):
    #return answer_with_parsed_json(request.question)
    return {
  "Step 1: Identify and Simplify Terms": "Los bonos son préstamos que le haces a un estado o empresa, mientras que los CDT (Certificados de Depósito) son préstamos que le haces a un banco.",
  "Step 2: Use Metaphors": "Imagina que comprar un bono es como prestarle a un amigo $50 con la promesa de que te devolverá más tarde. Un CDT es como poner tu dinero en una alcancía que te paga una pequeña recompensa por no tocarlo.",
  "Step 3: Provide Concrete Examples": "Cuando compras un bono del gobierno, estás ayudando a financiar un proyecto como una nueva escuela. Al abrir un CDT, si depositas $1,000 en un banco por un año, el banco te paga intereses por eso.",
  "Step 4: Highlight Key Differences": "Los bonos suelen tener un mayor riesgo y potencial de recompensa, como invertir en una startup. Los CDT son de bajo riesgo y menor retorno, similares a guardar tu dinero en un lugar seguro.",
  "Step 5: Conclude with a Summary": "En resumen, los bonos son como prestar dinero al estado para un proyecto, mientras que los CDT son como prestar dinero al banco para un retorno más seguro."
}
