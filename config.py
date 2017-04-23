import os
from json import loads

SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey')
REDIS_URL = os.environ.get('REDIS_URL')
