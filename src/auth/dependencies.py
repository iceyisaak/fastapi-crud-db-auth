from fastapi import Request, status,Depends
from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException
from . import utils,services,models
from typing import Any,List
from ..db import redis,main
from sqlmodel.ext.asyncio.session import AsyncSession

user_service=services.User()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request)->Any:
        # 1. Handle potential None from super call
        credentials = await super().__call__(request)


        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )


        
        # if credentials:
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
        

        # NEW: Check if user is blocked
        user_uid = token_data['user']['uid']
        if await redis.user_is_blocked(user_uid):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
        )
        

        self.verify_token_data(token_data)
        return token_data
        

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
        if token_data and token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
                headers={"WWW-Authenticate": "Bearer"},
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )



async def get_current_user(
        token_detail:dict=Depends(AccessTokenBearer()),
        session:AsyncSession=Depends(main.get_session)
    ):
    user_email=token_detail['user']['email']
    user=await user_service.get_user_by_email(user_email,session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user




class RoleChecker:
    def __init__(self,allowed_roles:List[str])->None:
        self.allowed_roles=allowed_roles

    def __call__(self,current_user:models.User=Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
