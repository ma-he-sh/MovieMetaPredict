import os
from dotenv import load_dotenv
load_dotenv()

APP_CONFIG = {
    'APP_NAME' : os.getenv('APP_NAME'),
    'APP_VERSION': os.getenv('APP_VERSION'),
    'APP_MODE' : os.getenv('APP_MODE'),
    'DB' : {
        'DB_HOST' : os.getenv('DB_HOST'),
        'DB_USER' : os.getenv('DB_USER'),
        'DB_NAME' : os.getenv('DB_NAME'),
        'DB_PASS' : os.getenv('DB_PASS'),
        'DB_PORT' : os.getenv('DB_PORT'),
     },
    'REDIS' : {
        'REDIS_HOST' : os.getenv('REDIS_HOST'),
        'REDIS_PASS' : os.getenv('REDIS_PASS'),
        'REDIS_PORT' : os.getenv('REDIS_PORT'),
    },
    'JWT_PASS' : os.getenv('JWT_PASS'),
    'APP_SALT' : os.getenv('APP_SALT'),
}