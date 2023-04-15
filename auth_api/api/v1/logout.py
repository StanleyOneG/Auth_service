from flask import jsonify
from flask_jwt_extended import (
    jwt_required,
    unset_access_cookies,
    unset_jwt_cookies,
    unset_refresh_cookies,
)
from flask_restful import Resource
from core.jwt_management import JWTHandler


class UserLogOut(Resource):
    @jwt_required(verify_type=False)
    def delete(self):
        JWTHandler.revoke_refresh_token()
        response = jsonify({'message': 'Successfully logged out'})
        unset_jwt_cookies(response=response)
        return response
