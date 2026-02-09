from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from . import utils
from typing import Any
from ..db import redis




class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request)->Any:
        # 1. Handle potential None from super call
        credentials = await super().__call__(request)
        
        if credentials:
            token = credentials.credentials
            
            # 2. Corrected method call (added parenthesis)
            if not self.token_valid(token):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid or expired token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            token_data = utils.decode_token(token)
            # 3. Ensure token_data exists before verification
            if token_data is None:
                 raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")




            if await redis.token_in_blocklist(token_data['jti']):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid or expired token",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            

            self.verify_token_data(token_data)

            return token_data
        
        return None

    # Added 'self' and logic check
    def token_valid(self, token: str) -> bool:
        token_data = utils.decode_token(token)
        return token_data is not None

    # Added 'self' so child overrides match the signature
    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Please override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        # Fixed typo: 'token_ata' -> 'token_data'
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
                headers={"WWW-Authenticate": "Bearer"},
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

