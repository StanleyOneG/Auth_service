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
REDIS_REFRESH_TOKEN_EXPIRE = configs.redis.refresh_token_expire
REDIS_ACCESS_TOKEN_EXPIRE = configs.redis.access_token_expire
REDIS_PORT = configs.redis.port

PGADMIN_DEFAULT_EMAIL = configs.pgadmin.default_email
PGADMIN_DEFAULT_PASSWORD = configs.pgadmin.default_password

SUPERUSER_LOGIN = configs.superuser.login
SUPERUSER_EMAIL = configs.superuser.email
SUPERUSER_PASSWORD = configs.superuser.password

SERVER_HOST = configs.server.host
SERVER_PORT = configs.server.port
SERVER_DEBUG = configs.server.debug
