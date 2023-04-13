import logging

from core.base_jwt import BaseJWT
from db.db_alchemy import db
from flask import jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    current_user,
    jwt_required,
)
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


class JWTHandler(BaseJWT):
    @staticmethod
    def create_jwt_tokens(user: User, *args, **kwargs):
        role = [permission.name for permission in user.permissions]
        additional_claims = {'role': role}
        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims,
        )
        refresh_token = create_refresh_token(identity=user.id)
        return access_token, refresh_token

    @staticmethod
    @jwt_required(refresh=True)
    def refresh_access_jwt_token(*args, **kwargs):
        role = [permission.name for permission in current_user.permissions]
        additional_claims = {'role': role}
        access_token = create_access_token(
            identity=current_user,
            additional_claims=additional_claims,
            fresh=False,
        )
        # response = jsonify({'message': 'Access token refreshed successfully'})
        # set_access_cookies(response, access_token)
        return access_token
