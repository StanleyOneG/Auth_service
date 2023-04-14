from flask import jsonify
from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from flask_restful import Resource, reqparse
from core.jwt_management import JWTHandler
from models.db_models import User
import logging
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from db.db_alchemy import db


class UserLogIn(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=True, location='form')
        parser.add_argument(
            "password", type=str, required=True, location='form'
        )
        data = parser.parse_args()
        email = data["email"]
        password = data["password"]
        user = db.session.query(User).filter_by(email=email).scalar()
        if user is None:
            return jsonify({"msg": "Bad email or password"}), 401
        if not user.check_password(password):
            return jsonify({"msg": "Bad email or password"}), 401
        access_token, refresh_token = JWTHandler.create_login_access_token(
            user=user
        )
        response = jsonify({'message': 'User logged in successfully'})
        set_access_cookies(
            response=response, encoded_access_token=access_token
        )
        set_refresh_cookies(
            response=response, encoded_refresh_token=refresh_token
        )
        return response