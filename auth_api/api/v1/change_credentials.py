from core.jwt_management import JWTHandler
from core.log_tracer import trace_this
from db.db_alchemy import db
from flask import jsonify
from flask_jwt_extended import (
    current_user,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from flask_restful import Resource, reqparse
from models.db_models import User


class ChangeUserCredentials(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=False, location='form')
    parser.add_argument('login', type=str, required=False, location='form')

    @trace_this
    @jwt_required(fresh=True)
    def put(self):
        """
        Изменение логина и пароля
        Запись в базу данных и выдача пары access token и refresh token
        ---
        parameters:
          - in: formData
            name: New login
            type: string
            required: false
          - in: formData
            name: New password
            type: string
            required: false
        tags:
          - User
        produces:
          - application/json
        security:
          - JWT: []
        responses:
          200:
            description: Данные успешно обновлены
        """
        data = self.parser.parse_args()
        if data['login']:
            login = data['login']
        if data['password']:
            password = data['password']
        user: User = db.session.query(User).get_or_404(current_user.id)
        if user:
            if data['login']:
                user.login = login
            if data['password']:
                user.set_password(password)
            unset_jwt_cookies(response=jsonify({'message': 'Cookies revoked'}))
            JWTHandler.revoke_refresh_token()
            access_token, refresh_token = JWTHandler.create_jwt_tokens(
                user,
            )
            response = jsonify(
                {'message': 'Login/password successfully changed'}
            )
            set_access_cookies(
                response=response, encoded_access_token=access_token
            )
            set_refresh_cookies(
                response=response, encoded_refresh_token=refresh_token
            )
            db.session.commit()
            return response

        return {'message': 'User not found'}
