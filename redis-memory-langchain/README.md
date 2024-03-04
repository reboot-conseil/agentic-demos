# Redis x Langchain memory

Low-latency reads and writes at the service of a long-term chat conversation history. This also respects your privacy since we run Mistral locally using `ollama` 😎.

## Prerequisites

- a working Python environment with `python3-venv` installed
- Docker and Docker Compose installed
- [`ollama`](https://ollama.com/) installed

## How to run

- `docker compose up -d`
- `python3 -m venv venv`
- `source venv/bin/activate`
- talk to the bot with `python3 app.py "my interaction"`
- stop the Redis instance with `docker compose down`
- deactivate the virtual environment with `deactivate`
- you can come back a few days later (provided that you didn't kill your docker volumes), the bot will remember you!
