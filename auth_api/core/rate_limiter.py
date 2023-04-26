from functools import wraps
from db.db_redis import redis
from http import HTTPStatus
from flask import request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def rate_limit(limit: int = 10, per: int = 60):
    """
    Rate limiter for user.
    """

    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            user_ip = str(request.remote_addr)
            user_agent = str(request.user_agent)
            user_id = ' - '.join([user_ip, user_agent])

            pipe = redis.pipeline()
            redis_set_name = '-'.join(
                [args[0].__class__.__name__, func.__name__]
            )
            pipe.zadd(
                name=redis_set_name,
                mapping={user_id: 1},
                incr=True,
            )
            pipe.expire(redis_set_name, per)
            pipe.execute()
            rate_limit_count = redis.zrange(
                redis_set_name,
                0,
                -1,
                withscores=True,
            )
            logger.info('===  %s  ===', *rate_limit_count)
            logger.info(
                '===   Time till expiry %s seconds  ===',
                redis.ttl(redis_set_name),
            )
            if rate_limit_count[0][1] > limit:
                return {
                    "message": "Too many requests"
                }, HTTPStatus.TOO_MANY_REQUESTS
            return func(*args, **kwargs)

        return inner_wrapper

    return wrapper
