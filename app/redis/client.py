import redis
from app.config import settings


def get_redis_client():
    return redis.Redis(
                host=settings.redis_host,
                port=19991,
                decode_responses=True,
                username=settings.redis_user_name,
                password=settings.redis_password 
            ) 