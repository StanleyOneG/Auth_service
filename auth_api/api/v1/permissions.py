from flask import Flask, request, Blueprint, jsonify
import logging
from flask_restful import Resource, reqparse
import uuid
from flask_jwt_extended import jwt_required, get_jwt
from core.jwt_management import JWTHandler

from models.db_models import User, Permission, UserPermission

from db.db_alchemy import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_permission(user_permissions, endpoint_permission):
    if endpoint_permission in user_permissions['permissions']:
        return True
    return False


class CreatePermission(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('permission', type=str, required=True, location='form')

    @jwt_required()
    def post(self):
        if not check_permission(get_jwt(), 'admin'):
            response = {'message': 'You are not allowed to do this'}
            return response, 403
        permission = self.parser.parse_args()['permission']
        permission_in_db = db.session.query(Permission).filter_by(name=permission).first()
        if permission_in_db:
            response = {'message': 'Permission already exists'}
            return response, 401
        new_permission = Permission()
        new_permission.name = permission
        new_permission.id = uuid.uuid4()
        db.session.add(new_permission)
        db.session.commit()
        response = {'message': 'Permission created successful'}
        return response, 200


class DeletePermission(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('permission', type=str, required=True, location='form')

    @jwt_required()
    def delete(self):
        if not check_permission(get_jwt(), 'admin'):
            response = {'message': 'You are not allowed to do this'}
            return response, 403
        permission = self.parser.parse_args()['permission']
        permission_in_db = db.session.query(Permission).filter_by(name=permission).first()
        if not permission_in_db:
            response = {'message': 'Permission does not exists'}
            return response, 401

        # Remove the permission from the user_permission table
        user_permission_list = db.session.query(UserPermission).filter_by(permission_id=permission_in_db.id).all()
        for user_permission in user_permission_list:
            db.session.delete(user_permission)

        db.session.commit()

        # Remove the permission from the Permission table
        db.session.delete(permission_in_db)
        db.session.commit()

        response = {'message': 'Permission deleted successful'}
        return response, 200


class SetUserPermission(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('permission', type=str, required=True, location='form')
    parser.add_argument('user_login', type=str, required=True, location='form')

    @jwt_required()
    def post(self):
        if not check_permission(get_jwt(), 'admin'):
            response = {'message': 'You are not allowed to do this'}
            return response, 403
        permission = self.parser.parse_args()['permission']
        user_login = self.parser.parse_args()['user_login']
        permission_in_db = db.session.query(Permission).filter_by(name=permission).first()
        user_in_db = db.session.query(User).filter_by(login=user_login).first()
        if not permission_in_db:
            response = {'message': 'Permission does not exists'}
            return response, 401
        if not user_in_db:
            response = {'message': 'User does not exists'}
            return response, 401
        user_permission = db.session.query(UserPermission).filter_by(permission_id=permission_in_db.id,
                                                                     user_id=user_in_db.id).first()
        if user_permission:
            response = {'message': 'User already has the specified permission'}
            return response, 401
        new_user_permission = UserPermission()
        new_user_permission.id = uuid.uuid4()
        new_user_permission.permission_id = permission_in_db.id
        new_user_permission.user_id = user_in_db.id
        db.session.add(new_user_permission)
        db.session.commit()
        response = {'message': 'User permission added successful'}
        return response, 200


class DeleteUserPermission(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('permission', type=str, required=True, location='form')
    parser.add_argument('user_login', type=str, required=True, location='form')

    @jwt_required()
    def delete(self):
        if not check_permission(get_jwt(), 'admin'):
            response = {'message': 'You are not allowed to do this'}
            return response, 403
        permission = self.parser.parse_args()['permission']
        user_login = self.parser.parse_args()['user_login']
        permission_in_db = db.session.query(Permission).filter_by(name=permission).first()
        user_in_db = db.session.query(User).filter_by(login=user_login).first()
        if not permission_in_db:
            response = {'message': 'Permission does not exist'}
            return response, 401
        if not user_in_db:
            response = {'message': 'User does not exist'}
            return response, 401
        user_permission = db.session.query(UserPermission).filter_by(permission_id=permission_in_db.id,
                                                                     user_id=user_in_db.id).first()
        if not user_permission:
            response = {'message': 'User does not have the specified permission'}
            return response, 401
        db.session.delete(user_permission)
        db.session.commit()
        response = {'message': 'User permission deleted successfully'}
        return response, 200


class ChangePermission(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('old_permission', type=str, required=True, location='form')
    parser.add_argument('new_permission', type=str, required=True, location='form')

    @jwt_required()
    def patch(self):
        if not check_permission(get_jwt(), 'admin'):
            response = {'message': 'You are not allowed to do this'}
            return response, 403
        permission = self.parser.parse_args()['old_permission']
        new_permission = self.parser.parse_args()['new_permission']

        permission_in_db = db.session.query(Permission).filter_by(name=permission).first()
        if not permission_in_db:
            response = {'message': 'Permission does not exist'}
            return response, 401

        # Update the permission in the Permission table
        permission_in_db.name = new_permission
        db.session.commit()

        response = {'message': 'Permission updated successfully'}
        return response, 200


class ShowUserPermissions(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_login', type=str, required=True, location='args')

    @jwt_required()
    def get(self):
        if not check_permission(get_jwt(), 'admin'):
            response = {'message': 'You are not allowed to do this'}
            return response, 403
        user_login = self.parser.parse_args()['user_login']

        user = db.session.query(User).filter_by(login=user_login).first()
        if not user:
            return "User not found", 404
        user_id = user.id

        permissions = (
            db.session.query(Permission)
            .join(UserPermission, UserPermission.permission_id == Permission.id)
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
        if not check_permission(get_jwt(), 'admin'):
            response = {'message': 'You are not allowed to do this'}
            return response, 403
        permissions = db.session.query(Permission).all()
        permission_names = [permission.name for permission in permissions]

        response_data = {'permissions': permission_names}
        return jsonify(response_data)
