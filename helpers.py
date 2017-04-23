from config import REDIS_URL
from redis import StrictRedis


redis_store = StrictRedis.from_url(REDIS_URL, db=1, decode_responses=True)
redis_store_2 = StrictRedis.from_url(REDIS_URL, db=2)
