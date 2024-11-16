import time

from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


REQUEST_COUNT = Counter("app_requests_total", "Total number of requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Request latency", ["endpoint"])


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Обновляем счетчик запросов
        REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()

        # Выполняем запрос
        response = await call_next(request)

        # Обновляем гистограмму задержек
        request_latency = time.time() - start_time
        REQUEST_LATENCY.labels(endpoint=request.url.path).observe(request_latency)

        return response
