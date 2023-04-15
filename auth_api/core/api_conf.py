"""Module for validating configuration parameters."""

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


def to_upper(value: str) -> str:
    """Helper to convert env variables to upper case

    Args:
        value: str - string to be converted to upper case

    Returns:
        converted to upper case value
    """
    return value.upper()


class DatabaseSettings(BaseSettings):
    engine: str

    class Config:
        """Configuration class for correct env variables insertion."""

        env_prefix = 'DB_'
        alias_generator = to_upper


class PgAdminSettings(BaseSettings):
    default_email: str
    default_password: str

    class Config:
        """Configuration class for correct env variables insertion."""

        env_prefix = 'PGADMIN_'
        alias_generator = to_upper


class PostgresSettings(BaseSettings):
    """Configuration for Postgresql."""

    host: str
    port: int
    user: str
    password: str
    db: str
    schema_name: str
    options: str

    class Config:
        """Configuration class for correct env variables insertion."""

        env_prefix = 'POSTGRES_'
        alias_generator = to_upper


class RedisSettings(BaseSettings):
    """Configuration for Redis."""

    host: str
    port: int
    refresh_token_expire: int
    access_token_expire: int

    class Config:
        """Configuration class for correct env variables insertion."""

        env_prefix = 'REDIS_'
        alias_generator = to_upper


class Settings(BaseSettings):
    """Helper class for configuration access."""

    database = DatabaseSettings()
    redis = RedisSettings()
    pgadmin = PgAdminSettings()
    postgres = PostgresSettings()
