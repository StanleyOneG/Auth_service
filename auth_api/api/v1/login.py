import os
from core.jwt_management import JWTHandler
from core.login_history import log_user_login_action
from db.db_alchemy import db
from flask import jsonify
from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from flask_restful import Resource, reqparse
from models.db_models import User
from http import HTTPStatus


class UserLogIn(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email",
        type=str,
        required=True,
        location='form',
    )
    parser.add_argument(
        "password",
        type=str,
        required=True,
        location='form',
    )

    @log_user_login_action
    def post(self):
        """
        Login зарегистрированного пользователя
        Выдача обновленной пары токенов access token и refresh token
        ---
        parameters:
          - in: formData
            name: email
            type: string
            required: true
          - in: formData
            name: password
            type: string
            required: true
        tags:
          - User
        responses:
          200:
            description: Успешный вход в аккаунт
        """
        data = self.parser.parse_args()
        email = data["email"]
        password = data["password"]
        user = db.session.query(User).filter_by(email=email).first()
        if user is None:
            return {"msg": "Bad email or password"}, HTTPStatus.UNAUTHORIZED
        if not user.check_password(password):
            return {"msg": "Bad email or password"}, HTTPStatus.UNAUTHORIZED
        access_token, refresh_token = JWTHandler.create_login_tokens(user=user)
        response = jsonify({'message': f'User logged in successfully'})
        set_access_cookies(
            response=response,
            encoded_access_token=access_token,
        )
        set_refresh_cookies(
            response=response,
            encoded_refresh_token=refresh_token,
        )

        return response
