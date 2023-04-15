import logging

from core.base_jwt import BaseJWT
from db.db_alchemy import db
from db.db_redis import redis
from flask_jwt_extended import JWTManager, jwt_required
from models.db_models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return db.session.execute(
        db.select(User).filter_by(id=identity)
    ).scalar_one()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = redis.get(jti)
    return token_in_redis is not None


class JWTHandler(BaseJWT):
    @staticmethod
    def create_jwt_tokens(user: User, *args, **kwargs):
        return super(JWTHandler, JWTHandler).create_token_pair(user=user)

    @staticmethod
    def create_login_tokens(user: User, *args, **kwargs):
        return super(JWTHandler, JWTHandler).create_token_pair(
            user=user, fresh_access_token=True
        )

    @staticmethod
    @jwt_required(verify_type=False)
    def revoke_access_token():
        return super(JWTHandler, JWTHandler).revoke_token()

    @staticmethod
    @jwt_required(refresh=True)
    def revoke_refresh_token():
        return super(JWTHandler, JWTHandler).revoke_token()
