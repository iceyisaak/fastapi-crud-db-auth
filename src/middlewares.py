from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from .db import main


class middleware:
    def __init__(self, app):
        pass

    @staticmethod
    async def register_middleware(app: FastAPI):
        pass


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Use the context manager version
        async with main.get_session_context() as session:
            request.state.db = session
            response = await call_next(request)
        return response