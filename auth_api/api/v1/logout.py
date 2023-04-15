from flask import jsonify
from flask_jwt_extended import (
    jwt_required,
    unset_jwt_cookies,
)
from flask_restful import Resource
from core.jwt_management import JWTHandler


class UserLogOut(Resource):
    @jwt_required(verify_type=False)
    def delete(self):
        """
        Выход пользователя из аккаунта
        Отзыв access token и refresh token
        ---
        responses:
          200:
            description: Выход из аккаунта выполнен успешно
        """
        JWTHandler.revoke_refresh_token()
        response = jsonify({'message': 'Successfully logged out'})
        unset_jwt_cookies(response=response)
        return response
