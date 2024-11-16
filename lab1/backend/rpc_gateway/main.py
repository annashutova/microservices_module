import httpx
import logging
from typing import Any

from fastapi import FastAPI, HTTPException, status, Response
from fastapi.responses import ORJSONResponse
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from middleware.metrics import MetricsMiddleware


app = FastAPI()
app.add_middleware(MetricsMiddleware)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rpc_gateway")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    REMOVE_DUPLICATES: str = 'http://remove_duplicates:8000/v1/do'
    REVERSE_LIST: str = 'http://reverse_list:8000/v1/do'


settings = Settings()


METHOD_TO_SERVICE = {
    'remove_duplicates': settings.REMOVE_DUPLICATES,
    'reverse_list': settings.REVERSE_LIST,
}


class RpcRequest(BaseModel):
    method: str
    data: dict[str, Any]
    requestId: str


@app.post("/rpc")
async def rpc_handler(body: RpcRequest):
    logger.info(f"Received RPC request: {body.requestId}")

    url = METHOD_TO_SERVICE.get(body.method)
    if not url:
        raise HTTPException(detail={"error": "Unknown method"}, status_code=status.HTTP_404_NOT_FOUND)

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=body.data)

    return ORJSONResponse(content=response.json(), status_code=response.status_code)


@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
