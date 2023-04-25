from core.jwt_management import JWTHandler
from core.log_tracer import trace_this
from flask import jsonify
from flask_jwt_extended import jwt_required, unset_jwt_cookies
from flask_restful import Resource


class UserLogOut(Resource):
    @trace_this
    @jwt_required(verify_type=False)
    def patch(self):
        """
        Выход пользователя из аккаунта
        Отзыв access token и refresh token
        ---
        responses:
          200:
            description: Выход из аккаунта выполнен успешно
        tags:
          - User
        produces:
          - application/json
        security:
          - JWT: []
        """
        JWTHandler.revoke_refresh_token()
        response = jsonify({'message': 'Successfully logged out'})
        unset_jwt_cookies(response=response)
        return response
