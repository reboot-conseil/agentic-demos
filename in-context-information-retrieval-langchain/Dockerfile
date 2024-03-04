FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY app.py /app/app.py

COPY vertexai-sa.json /app/vertexai-sa.json
COPY .env.example /app/.env
