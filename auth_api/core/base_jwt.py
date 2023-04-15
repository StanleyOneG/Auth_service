from abc import abstractmethod
from flask import jsonify

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
)
from core.config import REDIS_REFRESH_TOKEN_EXPIRE, REDIS_ACCESS_TOKEN_EXPIRE


from models.db_models import User
from db.db_redis import redis


class BaseJWT:
    @classmethod
    def create_token_pair(cls, user: User, fresh_access_token: bool = False):
        permissions = [
            permission.permission.name for permission in user.permissions
        ]
        additional_claims = {'permissions': permissions}
        if fresh_access_token:
            access_token = create_access_token(
                identity=user.id,
                additional_claims=additional_claims,
                fresh=True,
            )
        elif not fresh_access_token:
            access_token = create_access_token(
                identity=user.id,
                additional_claims=additional_claims,
            )
        refresh_token = create_refresh_token(identity=user.id)
        return access_token, refresh_token

    @classmethod
    def revoke_token(cls):
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        if ttype == "refresh":
            redis.set(jti, "", ex=REDIS_REFRESH_TOKEN_EXPIRE)
            return jsonify(
                msg=f"{ttype.capitalize()} token successfully revoked"
            )
        # Revoke access token

        redis.set(jti, "", ex=REDIS_ACCESS_TOKEN_EXPIRE)
        # Returns "Access token revoked" or "Refresh token revoked"
        return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")

    @abstractmethod
    def create_jwt_tokens(*args, **kwargs):
        pass

    @abstractmethod
    def create_login_tokens(*args, **kwargs):
        pass

    @abstractmethod
    def revoke_access_token(*args, **kwargs):
        pass

    @abstractmethod
    def revoke_refresh_token(*args, **kwargs):
        pass
