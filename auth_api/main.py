from datetime import timedelta

from api.v1.sign_up import UserSignUp
from api.v1.login import UserLogIn
from core.config import DB_URI
from core.jwt_management import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from db.db_alchemy import db
from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required
from flask_sqlalchemy import SQLAlchemy
from gevent import monkey

monkey.patch_all()

import logging

from flask_restful import Api, Resource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)
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
    # "json",
]


app.config["JWT_ALGORITHM"] = "RS256"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=10)
app.config["JWT_PUBLIC_KEY"] = public_key
app.config["JWT_PRIVATE_KEY"] = private_key


class TestHelloWorld(Resource):
    @jwt_required()
    def get(self):
        return {'message': 'Hello, World!'}


api.add_resource(TestHelloWorld, '/hello')
api.add_resource(UserSignUp, '/register')
api.add_resource(UserLogIn, '/login')

if __name__ == "__main__":
    app.run(
        debug=True, host='sprint06_auth_api', port='8000'
    )  # TODO: вынести host в env файл
