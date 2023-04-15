import uuid
from flask import jsonify
from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from flask_restful import Resource, reqparse
from core.jwt_management import JWTHandler
from models.db_models import User
import logging
from flask_wtf.csrf import generate_csrf

from db.db_alchemy import db


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserSignUp(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, location='form')
    parser.add_argument('password', type=str, required=True, location='form')
    parser.add_argument('login', type=str, required=True, location='form')

    def post(self):
        data = self.parser.parse_args()
        email = data['email']
        login = data['login']
        password = data['password']

        user = db.session.query(User).filter_by(email=email).first()
        if user:
            response = {'message': 'User with this email already exists'}
            return response, 401
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
        # csrf = generate_csrf()
        # response.set_cookie(
        #     'csfrtoken', csrf, httponly=True, samesite='Strict'
        # )
        return response
