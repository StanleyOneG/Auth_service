import os
from datetime import timedelta

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
from core.config import (
    DB_URI,
    REDIS_ACCESS_TOKEN_EXPIRE,
    REDIS_REFRESH_TOKEN_EXPIRE,
)
from core.jwt_management import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from db.db_alchemy import db
from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import jwt_required
from gevent import monkey

monkey.patch_all()

import logging
import uuid

from core.config import (
    SUPERUSER_EMAIL,
    SUPERUSER_LOGIN,
    SUPERUSER_PASSWORD,
    SERVER_HOST,
    SERVER_PORT,
    SERVER_DEBUG,
)
from flask_restful import Api, Resource
from models.db_models import Permission, User, UserPermission, engine
from sqlalchemy.orm import sessionmaker

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
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.before_first_request
def create_superuser():
    logger.info("============= Superuser creation ===============")
    Session = sessionmaker(bind=engine)
    session = Session()
    if (
        session.query(User).filter_by(email=SUPERUSER_EMAIL).first()
        is not None
    ):
        logger.info(
            "Superuser with provided email already exists. Abort creating"
        )
        return
    db_user = User(
        login=SUPERUSER_LOGIN,
        email=SUPERUSER_EMAIL,
        password=SUPERUSER_PASSWORD,
    )
    db_user.id = uuid.uuid4()
    db_user.login = SUPERUSER_LOGIN
    db_user.email = SUPERUSER_EMAIL
    db_user.set_password(SUPERUSER_PASSWORD)
    session.add(db_user)
    session.commit()
    logger.info("Superuser added")
    db_permission = Permission()
    db_permission.id = uuid.uuid4()
    db_permission.name = "admin"
    session.add(db_permission)
    session.commit()
    logger.info("Permission 'admin' created")

    db_user_permission = UserPermission()
    db_user_permission.id = uuid.uuid4()
    db_user_permission.permission_id = db_permission.id
    db_user_permission.user_id = db_user.id
    session.add(db_user_permission)
    session.commit()
    logger.info("Permission 'admin' atached to superuser")
    logger.info("============= Superuser creation ===============")


class TestHelloWorld(Resource):
    @jwt_required()
    def get(self):
        return {'message': 'Hello, World!'}


api.add_resource(TestHelloWorld, '/hello')
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

if __name__ == "__main__":
    app.run(debug=SERVER_DEBUG, host=SERVER_HOST, port=SERVER_PORT)
