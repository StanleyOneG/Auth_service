import os

from api.v1.sign_up import UserSignUp
from api.v1.login import UserLogIn
from api.v1.refresh import Refresh
from api.v1.logout import UserLogOut
from api.v1.change_credentials import ChangeUserCredentials
from core.config import (
    DB_URI,
    REDIS_REFRESH_TOKEN_EXPIRE,
    REDIS_ACCESS_TOKEN_EXPIRE,
)
from core.jwt_management import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from flask_jwt_extended import jwt_required
from datetime import timedelta

from api.v1.permissions import (
    CreatePermission,
    DeletePermission,
    SetUserPermission,
    ChangePermission,
    ShowUserPermissions,
    ShowPermissions,
    DeleteUserPermission,
)
from db.db_alchemy import db
from flask import Flask
from gevent import monkey
from flasgger import Swagger

monkey.patch_all()

import logging

from flask_restful import Api, Resource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI

db.init_app(app)
jwt.init_app(app)

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend(),
)

public_key = private_key.public_key()

app.config["JWT_TOKEN_LOCATION"] = [
    # "headers",
    "cookies",
]

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["JWT_ALGORITHM"] = "RS256"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    minutes=float(REDIS_ACCESS_TOKEN_EXPIRE / 60)
)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
    hours=float(REDIS_REFRESH_TOKEN_EXPIRE / 60 / 60)
)
app.config["JWT_PUBLIC_KEY"] = public_key
app.config["JWT_PRIVATE_KEY"] = private_key
# Disabled for development purposes. Turn on in Production
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config['JWT_REFRESH_COOKIE_PATH'] = '/'


class TestHelloWorld(Resource):
    @jwt_required()
    def get(self):
        return {'message': 'Hello, World!'}


api.add_resource(TestHelloWorld, '/hello')
api.add_resource(UserSignUp, '/api/v1/user/register')
api.add_resource(UserLogIn, '/api/v1/user/login')
api.add_resource(Refresh, '/api/v1/user/refresh')
api.add_resource(UserLogOut, '/api/v1/user/logout')
api.add_resource(ChangeUserCredentials, '/api/v1/user/change_credentials')
api.add_resource(CreatePermission, '/api/v1/permission/create_permission')
api.add_resource(DeletePermission, '/api/v1/permission/delete_permission')
api.add_resource(SetUserPermission, '/api/v1/user/set_permission')
api.add_resource(ChangePermission, '/api/v1/permission/change_permission')
api.add_resource(ShowUserPermissions, '/api/v1/user/show_user_permissions')
api.add_resource(ShowPermissions, '/api/v1/permission/show_permissions')
api.add_resource(DeleteUserPermission, '/api/v1/user/delete_user_permission')

if __name__ == "__main__":
    app.run(
        debug=True, host='sprint06_auth_api', port='8000'
    )  # TODO: вынести host в env файл
