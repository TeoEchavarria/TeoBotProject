#!/bin/bash
set -e

# Start Ollama
ollama serve &

# Wait for Ollama to start
sleep 15

# Pull the model at runtime
ollama pull deepseek-r1:7b

# Now run your Python code
python setup.py