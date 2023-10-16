ARG CUDA_IMAGE="12.1.1-devel-ubuntu22.04"
FROM nvidia/cuda:${CUDA_IMAGE}

ENV HOST 0.0.0.0

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y git build-essential \
    python3 python3-pip gcc wget \
    ocl-icd-opencl-dev opencl-headers clinfo \
    libclblast-dev libopenblas-dev \
    && mkdir -p /etc/OpenCL/vendors && echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd

COPY . .

# setting build related env vars
ENV CUDA_DOCKER_ARCH=all
ENV LLAMA_CUBLAS=1

# Install depencencies
RUN python3 -m pip install --upgrade pip pytest cmake \
    scikit-build setuptools fastapi uvicorn sse-starlette \
    pydantic-settings starlette-context gradio huggingface_hub hf_transfer

# Install llama-cpp-python (build with cuda)
RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./packages.txt /app/packages.txt

RUN apt-get update && xargs -r -a /app/packages.txt apt-get install -y && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# User
RUN useradd -m -u 1000 user
USER user
ENV HOME /home/user
ENV PATH $HOME/.local/bin:$PATH

WORKDIR $HOME
RUN mkdir app
WORKDIR $HOME/app
COPY . $HOME/app

EXPOSE 8501
CMD streamlit run app.py \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --server.fileWatcherType none