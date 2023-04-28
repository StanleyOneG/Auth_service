from http import HTTPStatus
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
from core.jwt_management import jwt
from db.db_alchemy import db
from flasgger import Swagger
from flask_migrate import Migrate
from flask_jwt_extended import jwt_required
from gevent import monkey

monkey.patch_all()

import logging

from core.config import SERVER_HOST, SERVER_PORT, SERVER_DEBUG

# from commands import superuser_bp
from flask_restful import Api, Resource
from core.app_config import TestingConfig, ProductionConfig
from werkzeug.exceptions import HTTPException
from models.db_models import User
import secrets
import string
from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from core.jwt_management import JWTHandler
from flask import jsonify
from core.oauth import OAuthSignIn
from flask import Flask, redirect, url_for
import uuid
# from flask_login import current_user


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(TestingConfig())
api = Api(app)
swagger = Swagger(app)

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

@app.route('/api/v1/authorize/<provider>')
def oauth_authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/api/v1/callback/<provider>')
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    id, login, email = oauth.callback()
    if id is None:
        response = {'message': 'Authentication failed. Empty id'}
        return response, HTTPStatus.BAD_REQUEST
    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        user = User()
        user.id = uuid.uuid4()
        user.email = email
        user.login = login
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(20))  # for a 20-character password
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


if __name__ == "__main__":
    app.run(debug=SERVER_DEBUG, host=SERVER_HOST, port=SERVER_PORT)
