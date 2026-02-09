from fastapi import HTTPException, status
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from datetime import datetime,timedelta
import jwt
import uuid
from src.config import Config
import logging
from typing import Optional



password_context=PasswordHash((
    Argon2Hasher(),  
))
ACCESS_TOKEN_EXPIRY=3600

def hash_password(password):
    """Hashes a password using Argon2"""
    hash=password_context.hash(password)
    return hash

def verify_password(password,hashed_password)->bool:
    return password_context.verify(password,hashed_password)

def create_access_token(user_data:dict,expiry_delta:Optional[timedelta]=None,refresh:bool=False):
    payload={}
    payload['user']=user_data
    payload['exp']=datetime.now()+(expiry_delta if expiry_delta is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti']=str(uuid.uuid4())
    payload['refresh']=refresh
    
    token=jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    return token


def decode_token(token:str)-> dict | None:
    try:
        token_data=jwt.decode(
            jwt=token, 
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.ExpiredSignatureError:
        logging.warning("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    except jwt.InvalidTokenError:
        logging.warning("Invalid token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    except Exception as e:
        logging.exception(f"Unexpected error decoding token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )