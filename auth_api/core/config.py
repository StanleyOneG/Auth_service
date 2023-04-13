from core.api_conf import Settings


configs = Settings()

DB_ENGINE = configs.database.engine
POSTGRES_DB = configs.postgres.db
POSTGRES_SCHEMA_NAME = configs.postgres.schema_name
POSTGRES_PASSWORD = configs.postgres.password
POSTGRES_USER = configs.postgres.user
POSTGRES_HOST = configs.postgres.host
POSTGRES_PORT = configs.postgres.port
POSTGRES_OPTIONS = configs.postgres.options
DB_URI = f"{DB_ENGINE}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

REDIS_HOST = configs.redis.host
REDIS_EXPIRE = configs.redis.expire
REDIS_PORT = configs.redis.port

PGADMIN_DEFAULT_EMAIL = configs.pgadmin.default_email
PGADMIN_DEFAULT_PASSWORD = configs.pgadmin.default_password
