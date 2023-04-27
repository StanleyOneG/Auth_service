from core.jwt_management import JWTHandler, check_if_token_is_revoked
from core.log_tracer import trace_this
from flask import jsonify
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt
from flask_restful import Resource
from http import HTTPStatus


class CheckToken(Resource):
    @trace_this
    @jwt_required(verify_type=False)
    def get(self):
        """
        Проверка токена на наличие в blacklist
        ---
        responses:
          200:
            description: Token прошел проверку
        tags:
          - Token
        produces:
          - application/json
        security:
          - JWT: []
        """
        return HTTPStatus.OK
