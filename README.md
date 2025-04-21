# TeoBot: Your Personal Knowledge Companion

TeoBot is a FastAPI‑powered service that turns any natural‑language question into a two‑step, JSON‑structured answer:
1. It suggests a presentation framework (metaphors, examples, analogies).
2. It returns the final answer following that framework.

## Features

- Two‑step GPT‑4O process for structured, bite‑sized explanations  
- Dynamic Pydantic model generation for schema‑validated JSON  
- FastAPI endpoint for easy integration  
- Optional Docker configuration for containerized deployment  

## Prerequisites

- Python 3.10+  
- [OpenAI API Key](https://platform.openai.com/docs/api-reference/authentication)  
- [MongoDB URI](https://www.mongodb.com/docs/atlas/getting-started/)  
- (Optional) Pinecone API Key for embeddings  

## Installation

1. Clone the repo  
2. Create a virtual env and install dependencies  
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Running Locally
```sh
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```
The API is now available at http://localhost:8000.

## Docker
Build and run with:
```sh
docker build -t teobot .
docker run -e OPENAI_API_KEY -e MONGODB_URI -p 80:80 teobot
```

## Usage
POST your question to `/execute`:
```sh
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"question":"¿Cómo funciona la fotosíntesis?"}'
```

## Contribution

We welcome community contributions. If you wish to contribute to TeoBot, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Make your changes: `git commit -m 'Add new feature'`.
4. Push the branch: `git push origin feature/YourFeature`.
5. Open a Pull Request.

## License

This project is licensed under the MIT License. For more details, refer to the LICENSE file.
