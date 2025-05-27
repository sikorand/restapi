from fastapi import Request
from fastapi_limiter.depends import RateLimiter
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis

async def init_redis():
    r = redis.Redis(host="localhost", port=6379, db=0)
    await FastAPILimiter.init(r)

def get_user_key(request: Request):
    auth = request.headers.get("authorization")
    if auth and auth.startswith("Bearer "):
        token = auth[7:]
        return f"user:{token}"
    return f"anon:{request.client.host}"

def rate_limiter(limit: str):
    return RateLimiter(times=int(limit.split("/")[0]), seconds=60, identifier=get_user_key)
