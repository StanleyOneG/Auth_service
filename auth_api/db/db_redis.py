from core.config import REDIS_HOST, REDIS_PORT
from redis import Redis

redis = Redis(host=REDIS_HOST, port=REDIS_PORT)
