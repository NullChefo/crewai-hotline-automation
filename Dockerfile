FROM python:3.12-slim as base

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    sqlite3 \
    libsqlite3-dev \
    build-essential \
    curl \
    wget \
    software-properties-common

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

WORKDIR /app

ARG OPENAI_API_KEY
ARG OPENAI_API_BASE
ARG OPENAI_MODEL_NAME

# Specify the command to run on container start
CMD ["python", "main.py"]
