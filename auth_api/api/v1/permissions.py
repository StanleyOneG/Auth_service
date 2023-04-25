import logging
import uuid
from http import HTTPStatus

from core.log_tracer import trace_this
from db.db_alchemy import db
from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required
from flask_restful import Resource, reqparse
from models.db_models import Permission, User, UserPermission

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_permission(user_permissions, endpoint_permission):
    if endpoint_permission in user_permissions['permissions']:
        return True
    return False


class CreatePermission(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('permission', type=str, required=True, location='form')

    @trace_this
    @jwt_required()
    def post(self):
        """
        Создание права доступа
        ---
        responses:
          200:
            description: Permission created successfully
          404:
            description: Permission already exists
          403:
            description: You are not allowed to do this
        parameters:
          - in: formData
            name: permission
            type: string
            required: true
        tags:
          - Permission
        produces:
          - application/json
        security:
          - JWT: []
        """
        if not check_permission(get_jwt(), 'admin'):
            response = {'message': 'You are not allowed to do this'}
            return response, HTTPStatus.FORBIDDEN
        permission = self.parser.parse_args()['permission']
        permission_in_db = (
            db.session.query(Permission).filter_by(name=permission).first()
        )
        if permission_in_db:
            response = {'message': 'Permission already exists'}
            return response, HTTPStatus.NOT_FOUND
        new_permission = Permission()
        new_permission.name = permission
        new_permission.id = uuid.uuid4()
        db.session.add(new_permission)
        db.session.commit()
        response = {'message': 'Permission created successfully'}
        return response, HTTPStatus.OK


class DeletePermission(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('permission', type=str, required=True, location='form')

    @trace_this
    @jwt_required()
    def delete(self):
        """
        Удаление права доступа
        ---
        responses:
          200:
            description: Permission deleted successfully
          403:
            description: You are not allowed to do this
          404:
            description: Permission does not exists
        parameters:
          - in: formData
            name: permission
            type: string
            required: true
        tags:
          - Permission
        produces:
          - application/json
        security:
          - JWT: []
        """
        if not check_permission(get_jwt(), 'admin'):
            response = {'message': 'You are not allowed to do this'}
            return response, HTTPStatus.FORBIDDEN
        permission = self.parser.parse_args()['permission']
        permission_in_db = (
            db.session.query(Permission).filter_by(name=permission).first()
        )
        if not permission_in_db:
            response = {'message': 'Permission does not exists'}
            return response, HTTPStatus.NOT_FOUND

        # Remove the permission from the user_permission table
        user_permission_list = (
            db.session.query(UserPermission)
            .filter_by(permission_id=permission_in_db.id)
            .all()
        )
        for user_permission in user_permission_list:
            db.session.delete(user_permission)

        db.session.commit()

        # Remove the permission from the Permission table
        db.session.delete(permission_in_db)
        db.session.commit()

        response = {'message': 'Permission deleted successful'}
        return response, HTTPStatus.OK


class SetUserPermission(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('permission', type=str, required=True, location='form')
    parser.add_argument('user_login', type=str, required=True, location='form')

    @trace_this
    @jwt_required()
    def post(self):
        """
        Добавление пользователю права доступа
        ---
        responses:
          200:
            description: User permission added successfully
          403:
            description: You are not allowed to do this
          404:
            description: Permission or User does not exists
        parameters:
          - in: formData
            name: permission
            type: string
            required: true
          - in: formData
            name: user_login
            type: string
            required: true
        tags:
          - User
        produces:
          - application/json
        security:
          - JWT: []
        """
        if not check_permission(get_jwt(), 'admin'):
            response = {'message': 'You are not allowed to do this'}
            return response, HTTPStatus.FORBIDDEN
        permission = self.parser.parse_args()['permission']
        user_login = self.parser.parse_args()['user_login']
        permission_in_db = (
            db.session.query(Permission).filter_by(name=permission).first()
        )
        user_in_db = db.session.query(User).filter_by(login=user_login).first()
        if not permission_in_db:
            response = {'message': 'Permission does not exists'}
            return response, HTTPStatus.NOT_FOUND
        if not user_in_db:
            response = {'message': 'User does not exists'}
            return response, HTTPStatus.NOT_FOUND
        user_permission = (
            db.session.query(UserPermission)
            .filter_by(
                permission_id=permission_in_db.id, user_id=user_in_db.id
            )
            .first()
        )
        if user_permission:
            response = {'message': 'User already has the specified permission'}
            return response, HTTPStatus.NOT_FOUND
        new_user_permission = UserPermission()
        new_user_permission.id = uuid.uuid4()
        new_user_permission.permission_id = permission_in_db.id
        new_user_permission.user_id = user_in_db.id
        db.session.add(new_user_permission)
        db.session.commit()
        response = {'message': 'User permission added successfully'}
        return response, HTTPStatus.OK


class DeleteUserPermission(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('permission', type=str, required=True, location='form')
    parser.add_argument('user_login', type=str, required=True, location='form')

    @jwt_required()
    def delete(self):
        """
        Удаление права доступа
        ---
        responses:
          200:
            description: User permission deleted successfully
          403:
            description: You are not allowed to do this
          404:
            description: Permission or User does not exists
        parameters:
          - in: formData
            name: permission
            type: string
            required: true
          - in: formData
            name: user_login
            type: string
            required: true
        tags:
          - User
        produces:
          - application/json
        security:
          - JWT: []
        """
        if not check_permission(get_jwt(), 'admin'):
            response = {'message': 'You are not allowed to do this'}
            return response, HTTPStatus.FORBIDDEN
        permission = self.parser.parse_args()['permission']
        user_login = self.parser.parse_args()['user_login']
        permission_in_db = (
            db.session.query(Permission).filter_by(name=permission).first()
        )
        user_in_db = db.session.query(User).filter_by(login=user_login).first()
        if not permission_in_db:
            response = {'message': 'Permission does not exist'}
            return response, HTTPStatus.NOT_FOUND
        if not user_in_db:
            response = {'message': 'User does not exist'}
            return response, HTTPStatus.NOT_FOUND
        user_permission = (
            db.session.query(UserPermission)
            .filter_by(
                permission_id=permission_in_db.id, user_id=user_in_db.id
            )
            .first()
        )
        if not user_permission:
            response = {
                'message': 'User does not have the specified permission'
            }
            return response, HTTPStatus.NOT_FOUND
        db.session.delete(user_permission)
        db.session.commit()
        response = {'message': 'User permission deleted successfully'}
        return response, HTTPStatus.OK


class ChangePermission(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'old_permission', type=str, required=True, location='form'
    )
    parser.add_argument(
        'new_permission', type=str, required=True, location='form'
    )

    @trace_this
    @jwt_required()
    def patch(self):
        """
        Изменение права доступа
        ---
        responses:
          200:
            description: Permission updated successfully
          403:
            description: You are not allowed to do this
          404:
            description: Permission does not exists
        parameters:
          - in: formData
            name: old_permission
            type: string
            required: true
          - in: formData
            name: new_permission
            type: string
            required: true
        tags:
          - Permission
        produces:
          - application/json
        security:
          - JWT: []
        """
        if not check_permission(get_jwt(), 'admin'):
            response = {'message': 'You are not allowed to do this'}
            return response, HTTPStatus.FORBIDDEN
        permission = self.parser.parse_args()['old_permission']
        new_permission = self.parser.parse_args()['new_permission']

        permission_in_db = (
            db.session.query(Permission).filter_by(name=permission).first()
        )
        if not permission_in_db:
            response = {'message': 'Permission does not exist'}
            return response, HTTPStatus.NOT_FOUND

        # Update the permission in the Permission table
        permission_in_db.name = new_permission
        db.session.commit()

        response = {'message': 'Permission updated successfully'}
        return response, HTTPStatus.OK


class ShowUserPermissions(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_login', type=str, required=True, location='args')

    @jwt_required()
    def get(self):
        """
        Показать права доступа пользователя
        ---
        responses:
          200:
            description: permissions
          403:
            description: You are not allowed to do this
          404:
            description: User not found
        parameters:
          - in: formData
            name: user_login
            type: string
            required: true
        tags:
          - User
        produces:
          - application/json
        security:
          - JWT: []
        """
        if not check_permission(get_jwt(), 'admin'):
            response = {'message': 'You are not allowed to do this'}
            return response, HTTPStatus.FORBIDDEN
        user_login = self.parser.parse_args()['user_login']

        user = db.session.query(User).filter_by(login=user_login).first()
        if not user:
            return "User not found", HTTPStatus.NOT_FOUND
        user_id = user.id

        permissions = (
            db.session.query(Permission)
            .join(
                UserPermission, UserPermission.permission_id == Permission.id
            )
            .filter(UserPermission.user_id == user_id)
            .all()
        )

        permission_names = [permission.name for permission in permissions]
        print(permission_names)
        print(type(permission_names))
        response_data = {'permissions': permission_names}
        return jsonify(response_data)


class ShowPermissions(Resource):
    @jwt_required()
    def get(self):
        """
        Показать права доступа
        ---
        responses:
          200:
            description: permissions
          403:
           description: You are not allowed to do this
        tags:
          - Permission
        produces:
          - application/json
        security:
          - JWT: []
        """
        if not check_permission(get_jwt(), 'admin'):
            response = {'message': 'You are not allowed to do this'}
            return response, HTTPStatus.FORBIDDEN
        permissions = db.session.query(Permission).all()
        permission_names = [permission.name for permission in permissions]

        response_data = {'permissions': permission_names}
        return jsonify(response_data)
