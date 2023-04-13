import uuid
from flask import jsonify
from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from flask_restful import Resource, reqparse
from core.jwt_management import JWTHandler
from models.db_models import User
import logging


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
        try:
            user = db.session.execute(
                db.one_or_404(
                    db.select(User).filter_by(email=data['email']),
                )
            )
            response = {'message': 'User with this email already exists'}
            return response, 401
        except:
            new_user = User()
            new_user.id = uuid.uuid4()
            new_user.email = data['email']
            new_user.set_password(data['password'])
            new_user.login = data['login']
            db.session.add(new_user)
            db.session.commit()
            access_token, refresh_token = JWTHandler.create_jwt_tokens(
                new_user
            )
            response = jsonify({'message': 'User sign up successfull'})
            set_access_cookies(
                response=response, encoded_access_token=access_token
            )
            set_refresh_cookies(
                response=response, encoded_refresh_token=refresh_token
            )
            return response
