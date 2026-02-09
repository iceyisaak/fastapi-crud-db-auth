from redis import asyncio as aioredis
from ..config import Config

JTI_EXPIRY=3600 # 1 hour in seconds


# Using from_url is often cleaner for async connections
token_blocklist = aioredis.from_url(
    f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/0",
    decode_responses=True # This returns strings instead of bytes (recommended)
)


# token_blocklist=aioredis.StrictRedis(
#     host=Config.REDIS_HOST,
#     port=Config.REDIS_PORT,
#     db=0
# )

async def add_jti_to_blocklist(jti:str)->None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY, # 1 hour in seconds
    )


async def token_in_blocklist(jti:str)->bool:
    await token_blocklist.get(jti)
    return True if jti else False