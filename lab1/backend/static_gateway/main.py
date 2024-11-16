import logging

from fastapi import FastAPI, status, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from middleware.metrics import MetricsMiddleware


app = FastAPI()
app.add_middleware(MetricsMiddleware)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("static_gateway")


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/static")
async def static_handler():
    return FileResponse(path="static/index.html", status_code=status.HTTP_200_OK)


@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
