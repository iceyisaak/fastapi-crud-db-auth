from fastapi import Request,Response,status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from typing import Any, Callable, Awaitable



class ErrorException(Exception):
    pass


class NotFoundError(ErrorException):
    pass


class InvalidTokenError(ErrorException):
    pass



def create_exception_handler(status_code:int,exception:Any )->Callable[[Request,Exception],Awaitable[JSONResponse]]:
    async def exception_handler(Request:Request,exception:Exception)->JSONResponse:
        return JSONResponse(
            content=exception,
            status_code=status_code
        )
    return exception_handler