FROM python:3.12-slim

WORKDIR /app

RUN pip install "fastapi[standard]" httpx pydantic-settings prometheus_client orjson

COPY ./backend/services/remove_duplicates/main.py /app/main.py
COPY ./backend/middleware/ /app/middleware