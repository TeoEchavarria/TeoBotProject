from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.services.response import answer_with_parsed_json

app = FastAPI()

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

@app.post("/execute")
async def execute(request: ExecuteRequest):
    #return answer_with_parsed_json(**request.model_dump())
    return 	{
  "Conociendo el cerebro": "Las redes neuronales son sistemas computacionales inspirados en el funcionamiento del cerebro humano, que buscan interpretar y procesar datos de manera similar a cómo lo hace un ser humano.",
  "Neurona como un interruptor": "Cada neurona en una red actúa como un interruptor que se activa al recibir señales, permitiendo pasar la información sólo si cumple con ciertos umbrales.",
  "Conectando neuronas": "Las neuronas están interconectadas a través de sinapsis, e intercambian información creando caminos de comunicación que se fortalecen con el aprendizaje.",
  "Entrenamiento de la red": "El entrenamiento implica ajustar los pesos de las conexiones mediante algoritmos, como el retropropagación, para que la red minimice errores en sus predicciones.",
  "Redes neuronales en acción": "Las redes neuronales se utilizan en diversas aplicaciones, como reconocimiento de imágenes, procesamiento de lenguaje natural y sistemas de recomendación."
} if request.step_by_step else {
  "Step 1: Identify and Simplify Terms": "Los bonos son préstamos que le haces a un estado o empresa, mientras que los CDT (Certificados de Depósito) son préstamos que le haces a un banco.",
  "Step 2: Use Metaphors": "Imagina que comprar un bono es como prestarle a un amigo $50 con la promesa de que te devolverá más tarde. Un CDT es como poner tu dinero en una alcancía que te paga una pequeña recompensa por no tocarlo.",
  "Step 3: Provide Concrete Examples": "Cuando compras un bono del gobierno, estás ayudando a financiar un proyecto como una nueva escuela. Al abrir un CDT, si depositas $1,000 en un banco por un año, el banco te paga intereses por eso.",
  "Step 4: Highlight Key Differences": "Los bonos suelen tener un mayor riesgo y potencial de recompensa, como invertir en una startup. Los CDT son de bajo riesgo y menor retorno, similares a guardar tu dinero en un lugar seguro.",
  "Step 5: Conclude with a Summary": "En resumen, los bonos son como prestar dinero al estado para un proyecto, mientras que los CDT son como prestar dinero al banco para un retorno más seguro."
}
