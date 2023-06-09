from core.jwt_management import JWTHandler
from flask import jsonify
from flask_jwt_extended import (
    get_current_user,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
)
from flask_restful import Resource


class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        Обновление токенов access token и refresh token
        ---
        responses:
          200:
            description: A single user item
        tags:
          - User
        security:
          - JWT: []
        responses:
          200:
            description: access token и refresh token успешно обновлены
        """
        user = get_current_user()
        JWTHandler.revoke_refresh_token()
        # unset_jwt_cookies(response=jsonify({'message': 'Cookies revoked'}))
        access_token, refresh_token = JWTHandler.create_jwt_tokens(user=user)
        response = jsonify({'message': 'Tokens refreshed successfully'})
        set_access_cookies(
            response=response, encoded_access_token=access_token
        )
        set_refresh_cookies(
            response=response, encoded_refresh_token=refresh_token
        )
        return response
