from redis import asyncio as aioredis
from ..config import Config

JTI_EXPIRY=3600 # 1 hour in seconds


# Using from_url is often cleaner for async connections
token_blocklist = aioredis.from_url(
    f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/0",
    decode_responses=True # This returns strings instead of bytes (recommended)
)

async def add_jti_to_blocklist(jti:str)->None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY, # 1 hour in seconds
    )


async def token_in_blocklist(jti:str)->bool:
    jti=await token_blocklist.get(jti)
    return jti is not None


async def remove_user_from_blocklist(user_uid: str) -> None:
    await token_blocklist.delete(f"user_blocked:{user_uid}")



async def add_user_to_blocklist(user_uid: str, expiry: int = 3600) -> None:
    await token_blocklist.set(
        name=f"user_blocked:{user_uid}",
        value="",
        ex=expiry
    )

async def user_is_blocked(user_uid: str) -> bool:
    result = await token_blocklist.get(f"user_blocked:{user_uid}")
    return result is not None



# admin_role=[
#     "adding users",
#     "changing roles",
#     "crud on users",
#     "book submissions",
#     "crud on reviews",
#     "revoking access",
# ]