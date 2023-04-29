"""Class with flask resources for OAuth providers and services"""

from http import HTTPStatus
import secrets
import string
import uuid

from flask_restful import Resource, url_for
from flask import redirect, jsonify
from flask_jwt_extended import set_access_cookies, set_refresh_cookies

from .services import OAuthSignIn
from models.db_models import User
from db.db_alchemy import db
from core.jwt_management import JWTHandler


class GoogleOAuth(Resource):
    def get(self):
        oauth = OAuthSignIn.get_provider('google')
        return oauth.authorize()


class GoogleOAuthCallback(Resource):
    def get(self):
        oauth = OAuthSignIn.get_provider('google')
        id, login, email = oauth.callback()
        if id is None:
            response = {'message': 'Authentication failed. Empty id'}
            return response, HTTPStatus.BAD_REQUEST
        return {
            'id': id,
            'login': login,
            'email': email
        }


# class GoogleOAuth(Resource):
#     def get(self):
#         oauth = OAuthSignIn.get_provider('google')
#         return oauth.authorize()


# class GoogleOAuthCallback(Resource):
#     def get(self):
#         oauth = OAuthSignIn.get_provider('google')
#         id, login, email = oauth.callback()
#         if id is None:
#             response = {'message': 'Authentication failed. Empty user id'}
#             return response, HTTPStatus.BAD_REQUEST
#         user = db.session.query(User).filter_by(email=email).first()
#         if not user:
#             alphabet = string.ascii_letters + string.digits
#             password = ''.join(secrets.choice(alphabet) for i in range(20))  # for a 20-character password
#             # The code below is duplicate from class: UserSignUp
#             user = User()
#             user.id = uuid.uuid4()
#             user.email = email
#             user.login = login
#             user.set_password(password)
#             db.session.add(user)
            
#             access_token, refresh_token = JWTHandler.create_jwt_tokens(
#                 user,
#         )

#             response = jsonify({'message': 'User sign up successfull'})
#             set_access_cookies(
#                 response=response, encoded_access_token=access_token
#             )
#             set_refresh_cookies(
#                 response=response, encoded_refresh_token=refresh_token
#             )
#             db.session.commit()
#             return response
#         access_token, refresh_token = JWTHandler.create_login_tokens(user=user)
#         response = jsonify({'message': f'User logged in successfully'})
#         set_access_cookies(
#             response=response,
#             encoded_access_token=access_token,
#         )
#         set_refresh_cookies(
#             response=response,
#             encoded_refresh_token=refresh_token,
#         )

#         return response


# class MailOAuth(Resource):
#     def get(self):
#         oauth = OAuthSignIn.get_provider('mail')
#         return oauth.authorize()


# class MailOAuthCallback(Resource):
#     def get(self):
#         oauth = OAuthSignIn.get_provider('mail')
#         id, login, email = oauth.callback()
#         if id is None:
#             response = {'message': 'Authentication failed. Empty user id'}
#             return response, HTTPStatus.BAD_REQUEST
#         user = db.session.query(User).filter_by(email=email).first()
#         if not user:
#             alphabet = string.ascii_letters + string.digits
#             password = ''.join(secrets.choice(alphabet) for i in range(20))  # for a 20-character password
#             # The code below is duplicate from class: UserSignUp
#             user = User()
#             user.id = uuid.uuid4()
#             user.email = email
#             user.login = login
#             user.set_password(password)
#             db.session.add(user)
            
#             access_token, refresh_token = JWTHandler.create_jwt_tokens(
#                 user,
#         )

#             response = jsonify({'message': 'User sign up successfull'})
#             set_access_cookies(
#                 response=response, encoded_access_token=access_token
#             )
#             set_refresh_cookies(
#                 response=response, encoded_refresh_token=refresh_token
#             )
#             db.session.commit()
#             return response
#         access_token, refresh_token = JWTHandler.create_login_tokens(user=user)
#         response = jsonify({'message': f'User logged in successfully'})
#         set_access_cookies(
#             response=response,
#             encoded_access_token=access_token,
#         )
#         set_refresh_cookies(
#             response=response,
#             encoded_refresh_token=refresh_token,
#         )

#         return response
