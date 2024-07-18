# Ollama

```bash
docker volume create ollama-local
```

```bash
docker compose up -d
```

## Enter the container
```bash
docker exec -it ollama bash
```

## Execute from container
```bash
ollama pull llama3:8b
```

```bash
docker build -t crewai-agents -f crewai.Dockerfile .
```


# Runs it and stops it
```bash

docker compose up -d && docker compose logs crewai-agents -f && docker compose down
```