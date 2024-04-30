
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.infra.config.config import Settings


SETTINGS = Settings().cache


# class Redis(Cacher):
#     def __init__(self, expire: int, host: str = "localhost", port: int = 6379) -> None:
#         self.expire = expire
#         self.__redis_conn = aioredis.Redis(host=host, port=port)
#
#     async def set(self, key: Any, value: Any, expire: Optional[int] = None) -> None:
#         if expire is None:
#             expire = self.expire
#         await self.__redis_conn.set(key, value, ex=expire)
#
#     async def get(self, key: Any) -> Any:
#         return await self.__redis_conn.get(key)
#
#     def get_redis(self) -> aioredis.Redis:
#         return self.__redis_conn


redis = aioredis.from_url(f"redis://{SETTINGS.redis_host}:{SETTINGS.redis_port}")
FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
