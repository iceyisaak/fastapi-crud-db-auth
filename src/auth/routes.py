from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from . import schemas,services,utils,dependencies
from ..db import main,redis

from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta,datetime


router=APIRouter()
REFRESH_TOKEN_EXPIRY=2
refresh_token_bearer=dependencies.RefreshTokenBearer()
access_token_bearer=dependencies.AccessTokenBearer()



@router.post("/signup",response_model=schemas.User,status_code=status.HTTP_201_CREATED)
async def signup(user:schemas.UserCreate,session:AsyncSession=Depends(main.get_session)):
   email=user.email
   user_exists=await services.User.user_exists(email,session)   

   if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists"
        )

   new_user=await services.User.create_user(user,session)   
   return new_user          


@router.post("/login")
async def login(login_data:schemas.UserLogin,session:AsyncSession=Depends(main.get_session)):
    email=login_data.email
    password=login_data.password
    user=await services.User.get_user_by_email(email,session)
    if user is not None:
        password_valid=utils.verify_password(password,user.password_hash)   
        if password_valid:            
            access_token=utils.create_access_token(
                user_data={
                    'email':user.email,
                    'uid':str(user.uid),
                },
            )
            refresh_token=utils.create_access_token(
                user_data={
                    'email':user.email,
                    'uid':str(user.uid)
                },
                expiry_delta=timedelta(days=REFRESH_TOKEN_EXPIRY),
                refresh=True
            )


            return JSONResponse(
                content={
                    "message":"Login successful",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email":user.email,
                        "uid":str(user.uid),
                    }
                },
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid credentials"
    )


@router.get("/refresh_token")
async def get_new_acccess_token(token_details:dict=Depends(refresh_token_bearer)):
    expiry_timestamp=token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp)>datetime.now():
        new_access_token=utils.create_access_token(
            user_data=token_details['user']
        )
        return JSONResponse(content={"access_token": new_access_token})
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Token expired"
    )



@router.get("/logout")
async def revoke_token(token_details:dict=Depends(access_token_bearer)):
    jti=token_details['jti']
    await redis.token_in_blocklist(jti)