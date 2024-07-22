

pip install python-dotenv
pip install -U langchain-community
pip install -U duckduckgo-search


# Activate the env

```bash
sh ./venv/bin/activate
```

# Dependencies to requirements.txt

```bash
 pip freeze > requirements.txt
```


# Create docker container

```bash
docker build . -t crewai:latest
```

# Run docker container with LL Studio

```bash
docker run -p 8080:8080 -e OPENAI_API_KEY='lm-studio' -e OPENAI_API_BASE='http://127.0.0.1:1234/v1' crewai:latest
```

# Swagger

http://localhost:8000/docs

# Redoc

http://localhost:8000/redoc