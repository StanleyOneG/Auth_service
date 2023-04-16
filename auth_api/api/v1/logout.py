from flask import jsonify
from flask_jwt_extended import (
    current_user,
    get_current_user,
    jwt_required,
    unset_jwt_cookies,
)
from flask_restful import Resource
from core.jwt_management import JWTHandler


class UserLogOut(Resource):
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
