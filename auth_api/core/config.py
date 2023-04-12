import os
from dotenv import load_dotenv

load_dotenv()

DB_ENGINE = os.getenv('DB_ENGINE', 'postgresql')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'service_auth')
POSTGRES_SCHEMA_NAME = os.getenv('POSTGRES_SCHEMA_NAME', 'auth')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
POSTGRES_OPTIONS = "-c search_path=auth"
DB_URI = f"{DB_ENGINE}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_EXPIRE = 300
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

PGADMIN_DEFAULT_EMAIL = os.getenv('PGADMIN_DEFAULT_EMAIL', 'test@test.com')
PGADMIN_DEFAULT_PASSWORD = os.getenv('PGADMIN_DEFAULT_PASSWORD', 'postgres')
