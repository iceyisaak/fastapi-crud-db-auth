from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from .db import main
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.trustedhost import TrustedHostMiddleware


class middleware:
    def __init__(self, app):
        pass


    @staticmethod
    async def register_middleware(app:FastAPI):
        pass



# app.add_middleware(
#     CORSMiddleware,
#     allow_origins: ["*"],
#     allow_methods=[""],
#     allow_headers=[""],
#     allow_credentials=True
# )


"""
Middleware to attach database session to request state

This middleware ensures that the database session is available in request.state
for the TokenBearer dependency to use when checking revoked tokens.
"""



class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Create a new database session for this request
        async with main.get_session() as session:
            request.state.db = session
            response = await call_next(request)
        return response


# Add this middleware to your FastAPI app in main.py:
"""
from fastapi import FastAPI
from .auth.middleware import DBSessionMiddleware

app = FastAPI()
app.add_middleware(DBSessionMiddleware)
"""
