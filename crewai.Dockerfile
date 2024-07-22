FROM python:3.12-slim

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

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY crewai-ollama.py ./

CMD [ "python3", "-u", "main-crewai.py" ]