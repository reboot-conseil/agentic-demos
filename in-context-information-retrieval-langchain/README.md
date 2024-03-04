# Gemini Chat in-context information retrieval

An implementation of in-context information retrieval using the Gemini Chat Langchain API.

We are using a lengthy PDF and we stuff the LLM context with selected parts of the splitted document to answer the user's query.

## Prerequisites

- a working Python environment with `python3-venv` installed
- Docker and Docker Compose installed
- a Google Cloud project with billing enabled
- a service account with the role `Vertex AI User` set up
- a JSON key for this service account called `vertexai-sa.json` in the root of this repository (it is gitignored)

## How to run

- `docker compose watch`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- run the example script with `python3 app.py` (change the script if you want to change the input)
- deactivate the virtual environment with `deactivate`
