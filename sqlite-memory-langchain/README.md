# SQLite x Langchain memory

Embedded systems databases at the service of a long-term chat conversation history. This also respects your privacy since we run Mistral locally using `ollama` 😎.

## Prerequisites

- a working Python environment with `python3-venv` installed
- [`ollama`](https://ollama.com/) installed

## How to run

- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- talk to the bot with `python3 app.py "my interaction"`
- deactivate the virtual environment with `deactivate`
- you can come back a few days later (provided that you didn't kill the database file), the bot will remember you!

Try to spice things up by telling the bot to remember a keyword for instance 😉 Kill `ollama` entirely and try to make it output the keyword again.
