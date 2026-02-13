from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from . import schemas,services,utils,dependencies
from ..sessions import services as session_services
from ...db import main

from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta,datetime,timezone


router=APIRouter()
REFRESH_TOKEN_EXPIRY=2
refresh_token_bearer=dependencies.RefreshTokenBearer()
access_token_bearer=dependencies.AccessTokenBearer()
role_checker=dependencies.RoleChecker(["admin","user"])


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
async def login(
    login_data: schemas.UserLogin,
    session: AsyncSession = Depends(main.get_session)
):
    email = login_data.email
    password = login_data.password
    user = await services.User.get_user_by_email(email, session)

    if user is not None:
        password_valid = utils.verify_password(password, user.password_hash)
        if password_valid:
            # Create tokens
            access_token = utils.create_access_token(
                user_data={
                    'email': user.email,
                    'uid': str(user.uid),
                    'role': user.role
                },
            )
            refresh_token = utils.create_access_token(
                user_data={
                    'email': user.email,
                    'uid': str(user.uid)
                },
                expiry_delta=timedelta(days=REFRESH_TOKEN_EXPIRY),
                refresh=True
            )

            # Decode tokens to get JTI and expiry
            access_token_data = utils.decode_token(access_token)
            refresh_token_data = utils.decode_token(refresh_token)
            
            # Create session in database
            session_service = session_services.Session()
            await session_service.create_session(
                user_uid=str(user.uid),
                access_token=access_token,
                refresh_token=refresh_token,
                access_jti=access_token_data['jti'],
                refresh_jti=refresh_token_data['jti'],
                expires_at=datetime.fromtimestamp(refresh_token_data['exp']),
                created_at=datetime.now(timezone.utc),
                session=session
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "uid": str(user.uid),
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




@router.post("/logout")
async def revoke_token(
    token_details: dict = Depends(access_token_bearer),
    session: AsyncSession = Depends(main.get_session),
    logout_all: bool = False
):
    """
    Revoke the current session or all user sessions
    
    Args:
        logout_all: If True, revoke all sessions for the user. If False, revoke only current session.
    
    Body (optional):
        {
            "logout_all": true  // Set to true to logout from all devices
        }
    """
    jti = token_details['jti']
    user_uid = token_details['user']['uid']
    
    session_service = session_services.Session()
    
    if logout_all:
        # Revoke all sessions for the user
        revoked_count = await session_service.revoke_all_user_sessions(
            user_uid=user_uid,
            session=session
        )
        return JSONResponse(
            content={
                "message": f"Successfully logged out from {revoked_count} device(s)."
            },
            status_code=status.HTTP_200_OK
        )
    else:
        # Revoke only the current session
        revoked = await session_service.revoke_session(jti=jti, session=session)
        
        if revoked:
            return JSONResponse(
                content={"message": "Successfully logged out."},
                status_code=status.HTTP_200_OK
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )


@router.get("/me",response_model=schemas.UserBooks)
async def get_current_user(user=Depends(dependencies.get_current_user),_:bool=Depends(role_checker)):
    return user