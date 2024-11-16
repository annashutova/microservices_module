FROM python:3.12-slim

WORKDIR /app

RUN pip install "fastapi[standard]" httpx pydantic-settings prometheus_client orjson

COPY ./backend/static_gateway/main.py /app/main.py
COPY ./static/ /app/static/
COPY ./backend/middleware/ /app/middleware