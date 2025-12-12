from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("uvicorn.access")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger.info(f"request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"response: {response.status_code}")
        return response
