import logging
import uuid

from core.jwt_management import JWTHandler
from core.login_history import log_user_login_action
from db.db_alchemy import db
from flask import jsonify
from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from flask_restful import Resource, reqparse
from models.db_models import User
from http import HTTPStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserSignUp(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, location='form')
    parser.add_argument('password', type=str, required=True, location='form')
    parser.add_argument('login', type=str, required=True, location='form')

    @log_user_login_action
    def post(self):
        """
        Регистрация нового пользователя
        Запись в базу данных и выдача пары access token и refresh token
        ---
        parameters:
          - in: formData
            name: email
            type: string
            required: true
          - in: formData
            name: login
            type: string
            required: true
          - in: formData
            name: password
            type: string
            required: true
        tags:
          - User
        produces:
          - application/json
        security:
          - JWT: []
        responses:
          200:
            description: Пользователь успешно зарегистрирован
        """
        data = self.parser.parse_args()
        email = data['email']
        login = data['login']
        password = data['password']

        user = db.session.query(User).filter_by(email=email).first()
        if user:
            response = {'message': 'User with this email already exists'}
            return response, HTTPStatus.UNAUTHORIZED
        new_user = User()
        new_user.id = uuid.uuid4()
        new_user.email = email
        new_user.set_password(password)
        new_user.login = login
        db.session.add(new_user)
        access_token, refresh_token = JWTHandler.create_jwt_tokens(
            new_user,
        )
        response = jsonify({'message': 'User sign up successfull'})
        set_access_cookies(
            response=response, encoded_access_token=access_token
        )
        set_refresh_cookies(
            response=response, encoded_refresh_token=refresh_token
        )
        db.session.commit()
        return response
