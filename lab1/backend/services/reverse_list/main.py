from typing import Any

from fastapi import FastAPI, Response, status
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from middleware.metrics import MetricsMiddleware


app = FastAPI()


class DoRequest(BaseModel):
    values: list[Any]


app.add_middleware(MetricsMiddleware)


@app.post("/v1/do")
async def do(body: DoRequest):
    response = {
        "result": body.values[::-1]
    }
    return ORJSONResponse(content=response, status_code=status.HTTP_200_OK)


@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)