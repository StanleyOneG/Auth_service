from gevent import monkey

monkey.patch_all()

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

import logging

from core.config import SERVER_HOST, SERVER_PORT, SERVER_DEBUG

from flask_restful import Api
from core.app_config import TestingConfig
from werkzeug.exceptions import HTTPException
from flask import Flask
from core.oauth import oauth, OAuthLogin, OAuthCallback


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(TestingConfig())
api = Api(app)
swagger = Swagger(app)
oauth.init_app(app)

app.register_error_handler(HTTPException, handle_exception)

migrate = Migrate(app, db)

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(superuser_bp)
app.cli.add_command(create_superuser, name="create_superuser")


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
