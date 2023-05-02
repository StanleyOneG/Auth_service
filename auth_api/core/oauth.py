from http import HTTPStatus
import secrets, uuid, string
from enum import Enum

from flask_restful import Resource, reqparse, url_for
from flask import request, session, jsonify
from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from authlib.integrations.flask_client import OAuth
from core.login_history import log_user_login_action

import logging

import requests


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


class OAuthProviders(Enum):
    google = 'google'
    mail = 'mail'
    vk = 'vk'
    yandex = 'yandex'


class OAuthLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "provider",
        type=str,
        required=True,
        location='args',
    )

    def get(self):
        """
        OAuth аутентификация и регистрация пользователя
        Запись в базу данных и выдача пары access token и refresh token
        ---
        parameters:
          - in: query
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

        data = self.parser.parse_args()
        provider = data["provider"]
        session['provider'] = provider
        client = oauth.create_client(provider)
        redirect_url = url_for('oauthcallback', _external=True)
        logger.info(
            f'Redirect URL after authorizing provider {provider} {redirect_url}'
        )
        return client.authorize_redirect(redirect_url)


class OAuthCallback(Resource):
    @log_user_login_action(oauth=True)
    def get(self):
        provider = dict(session).get('provider')
        if provider is None:
            return {
                'msg': 'Unknown provider or not supported'
            }, HTTPStatus.BAD_REQUEST
        if provider != OAuthProviders.vk.name:
            client = oauth.create_client(provider)
            token = client.authorize_access_token()
            logger.info(f'Got token {token} for provider {provider}')
            params = {
                'access_token': token.get('access_token'),
                'oauth_token': token.get('access_token'),  # yandex
            }
            me = client.get('', params=params).json()
            logger.info(f'Got info about user {me} for provider {provider}')
            if provider == OAuthProviders.yandex.name:
                email = me['default_email']
            else:
                email = me['email']
            login = email.split('@')[0]
            # me['sub'] for Google, me['id'] for MailRu, Yandex if needed
        if provider == OAuthProviders.vk.name:
            if 'code' in request.args:
                code = request.args.get('code')
                logger.info(f'Got code {code} for provider vk')

                # make a POST request to the VK API's 'access_token' endpoint to retrieve the access token
                params = {
                    'client_id': configs.oauth.get('vk').client_id,
                    'client_secret': configs.oauth.get('vk').client_secret,
                    'redirect_uri': url_for('oauthcallback', _external=True),
                    'code': code,
                }
                response = requests.post(
                    configs.oauth.get('vk').access_token_url, params=params
                )
                logger.info(f'Got token {response.json()} for provider vk')
            email = response.json().get('email')
            login = email.split('@')[0]
        if email is None:
            response = {'message': 'Authentication failed. Empty user email'}
            return response, HTTPStatus.BAD_REQUEST
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            alphabet = string.ascii_letters + string.digits
            password = ''.join(
                secrets.choice(alphabet) for i in range(20)
            )  # for a 20-character password
            user = User()
            user.id = uuid.uuid4()
            user.email = email
            user.login = login
            user.set_password(password)
            db.session.add(user)

            access_token, refresh_token = JWTHandler.create_jwt_tokens(
                user,
            )

            response = jsonify(
                {'message': f'User {email} sign up successfull'}
            )
            set_access_cookies(
                response=response, encoded_access_token=access_token
            )
            set_refresh_cookies(
                response=response, encoded_refresh_token=refresh_token
            )
            db.session.commit()
            return response
        access_token, refresh_token = JWTHandler.create_login_tokens(user=user)
        response = jsonify({'message': f'User {email} logged in successfully'})
        set_access_cookies(
            response=response,
            encoded_access_token=access_token,
        )
        set_refresh_cookies(
            response=response,
            encoded_refresh_token=refresh_token,
        )

        # set email for history logging decorator
        session['email'] = email

        return response
