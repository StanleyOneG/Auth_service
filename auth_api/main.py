from http import HTTPStatus
import string, secrets, uuid
from api.v1.change_credentials import ChangeUserCredentials
from api.v1.login import UserLogIn
from api.v1.logout import UserLogOut
from api.v1.permissions import (
    ChangePermission,
    CreatePermission,
    DeletePermission,
    DeleteUserPermission,
    SetUserPermission,
    ShowPermissions,
    ShowUserPermissions,
)   
from api.v1.refresh import Refresh
from api.v1.show_login_history import ShowUserLogInHistory
from api.v1.sign_up import UserSignUp

from commands import create_superuser, superuser_bp
from core.exception_handler import handle_exception
from core.jwt_management import jwt, JWTHandler
from db.db_alchemy import db
from flasgger import Swagger
from flask_migrate import Migrate
from flask_jwt_extended import jwt_required, set_access_cookies, set_refresh_cookies
from gevent import monkey

monkey.patch_all()

import logging

from core.config import SERVER_HOST, SERVER_PORT, SERVER_DEBUG

from flask_restful import Api, Resource, reqparse, url_for
from core.app_config import TestingConfig
from werkzeug.exceptions import HTTPException
from flask import Flask, session, jsonify
from authlib.integrations.flask_client import OAuth
from core.config import configs
from models.db_models import User


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(TestingConfig())
api = Api(app)
swagger = Swagger(app)
oauth = OAuth(app)
oauth.register(**configs.oauth.get('google').__dict__)
oauth.register(**configs.oauth.get('mail').__dict__)


app.register_error_handler(HTTPException, handle_exception)

migrate = Migrate(app, db)

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(superuser_bp)
app.cli.add_command(create_superuser, name="create_superuser")


class TestHelloWorld(Resource):
    @jwt_required()
    def get(self):
        # return {'message': 'Hello, World!'}
        raise HTTPStatus.BAD_REQUEST


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
        print(f"==== provider {provider} =======")
        session['provider'] = provider
        print(f"==== session provider {session['provider']} =======")
        client = oauth.create_client(provider)
        return client.authorize_redirect(
            url_for('oauthcallback', _external=True)
            )


class OAuthCallback(Resource):
    def get(self):
        provider = dict(session).get('provider')
        print(provider)
        if provider is None:
            return {'msg': 'Unknown provider or not supported'}, HTTPStatus.BAD_REQUEST
        client = oauth.create_client(provider)
        token = client.authorize_access_token()
        params = {
            'access_token': token.get('access_token')
        }
        me = client.get('',params=params).json()
        login_email = me['email'].split('@')
        login = login_email[0]
        # if provider is 'mail':
        #     id = me['id']
        # else:
        #     id = me['sub']
        email = me['email']
        if email is None:
            response = {'message': 'Authentication failed. Empty user email'}
            return response, HTTPStatus.BAD_REQUEST
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(20))  # for a 20-character password
            # The code below is duplicate from class: UserSignUp
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

api.add_resource(TestHelloWorld, '/api/hello')
api.add_resource(UserSignUp, '/api/v1/user/register')
api.add_resource(UserLogIn, '/api/v1/user/login')
api.add_resource(Refresh, '/api/v1/user/refresh')
api.add_resource(UserLogOut, '/api/v1/user/logout')
api.add_resource(ShowUserLogInHistory, '/api/v1/user/show_login_history')
api.add_resource(ChangeUserCredentials, '/api/v1/user/change_credentials')
api.add_resource(CreatePermission, '/api/v1/permission/create_permission')
api.add_resource(DeletePermission, '/api/v1/permission/delete_permission')
api.add_resource(SetUserPermission, '/api/v1/user/set_permission')
api.add_resource(ChangePermission, '/api/v1/permission/change_permission')
api.add_resource(ShowUserPermissions, '/api/v1/user/show_user_permissions')
api.add_resource(ShowPermissions, '/api/v1/permission/show_permissions')
api.add_resource(DeleteUserPermission, '/api/v1/user/delete_user_permission')
api.add_resource(OAuthLogin, '/api/v1/auth')
api.add_resource(OAuthCallback, '/api/v1/callback')


if __name__ == "__main__":
    app.run(debug=SERVER_DEBUG, host=SERVER_HOST, port=SERVER_PORT)
