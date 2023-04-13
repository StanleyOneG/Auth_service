"""Module for validating configuration parameters."""

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


def to_lower(value: str) -> str:
    """Helper to convert env variables to lower case

    Args:
        value: str - string to be converted to lower case

    Returns:
        converted to lower case value
    """
    return value.lower()


class DatabaseSettings(BaseSettings):
    ENGINE: str

    class Config:
        """Configuration class for correct env variables insertion."""

        env_prefix = 'DB_'
        alias_generator = to_lower


class PgAdminSettings(BaseSettings):
    DEFAULT_EMAIL: str
    DEFAULT_PASSWORD: str

    class Config:
        """Configuration class for correct env variables insertion."""

        env_prefix = 'PGADMIN_'
        alias_generator = to_lower


class PostgresSettings(BaseSettings):
    """Configuration for Postgresql."""

    HOST: str 
    PORT: int
    USERNAME: str
    PASSWORD: str
    DB_NAME: str
    SCHEMA_NAME: str
    OPTIONS: str

    class Config:
        """Configuration class for correct env variables insertion."""

        env_prefix = 'POSTGRES_'
        alias_generator = to_lower


class RedisSettings(BaseSettings):
    """Configuration for Redis."""

    HOST: str
    PORT: int
    EXPIRE: int

    class Config:
        """Configuration class for correct env variables insertion."""

        env_prefix = 'REDIS_'
        alias_generator = to_lower


class Settings(BaseSettings):
    """Helper class for configuration access."""

    DATABASE = DatabaseSettings()
    REDIS = RedisSettings()
    PGADMIN = PgAdminSettings()
    POSTGRES = PostgresSettings()
