from http import HTTPStatus
import secrets, uuid, string

from flask_restful import Resource, reqparse, url_for
from flask import session, jsonify
from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from authlib.integrations.flask_client import OAuth

import logging

from models.db_models import User
from core.jwt_management import JWTHandler
from db.db_alchemy import db
from core.config import configs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

oauth = OAuth()
oauth.register(**configs.oauth.get('google').__dict__)
oauth.register(**configs.oauth.get('mail').__dict__)
oauth.register(**configs.oauth.get('yandex').__dict__)
oauth.register(**configs.oauth.get('vk').__dict__)


class OAuthLogin(Resource):
    """
    OAuth аутентификация и регистрация пользователя
    Запись в базу данных и выдача пары access token и refresh token
    ---
    parameters:
        - in: Args
        name: provider
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

    parser = reqparse.RequestParser()
    parser.add_argument(
        "provider",
        type=str,
        required=True,
        location='args',
    )
    def get(self):
        data = self.parser.parse_args()
        provider = data["provider"]
        session['provider'] = provider
        client = oauth.create_client(provider)
        redirect_url = url_for('oauthcallback', _external=True)
        logger.info(f'Redirect URL after authorizing provider {provider} {redirect_url}')
        return client.authorize_redirect(redirect_url)


class OAuthCallback(Resource):
    def get(self):
        provider = dict(session).get('provider')
        if provider is None:
            return {'msg': 'Unknown provider or not supported'}, HTTPStatus.BAD_REQUEST
        client = oauth.create_client(provider)
        token = client.authorize_access_token()
        logger.info(f'Got token {token} for provider {provider}')
        params = {
            'access_token': token.get('access_token'),
            'oauth_token': token.get('access_token') # yandex
        }
        me = client.get('',params=params).json()
        logger.info(f'Got info about user {me} for provider {provider}')
        if provider == 'yandex':
            email = me['default_email']
        else:
            email = me['email']
        login = email.split('@')[0]
        # me['sub'] for Google, me['id'] for MailRu, Yandex if needed
        if email is None:
            response = {'message': 'Authentication failed. Empty user email'}
            return response, HTTPStatus.BAD_REQUEST
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(20))  # for a 20-character password
            user = User()
            user.id = uuid.uuid4()
            user.email = email
            user.login = login
            user.set_password(password)
            db.session.add(user)
            
            access_token, refresh_token = JWTHandler.create_jwt_tokens(
                user,
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
