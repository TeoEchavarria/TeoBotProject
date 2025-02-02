# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install curl (and optionally ca-certificates) so we can fetch the Ollama install script
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama using the official script
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy the requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files
COPY . .

# Copy an entrypoint script that launches Ollama in the background, then your Python app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Avoid Python writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Final command
CMD ["/entrypoint.sh"]