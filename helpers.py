from config import REDIS_URL
from redis import StrictRedis
import string
from random import choice


redis_store = StrictRedis.from_url(REDIS_URL, decode_responses=True)


def random_string(length, numbers=True, letters=True):
    chars = []
    if numbers:
        chars += string.digits
    if letters:
        chars += string.ascii_lowercase
    return ''.join(choice(chars) for x in range(length))
