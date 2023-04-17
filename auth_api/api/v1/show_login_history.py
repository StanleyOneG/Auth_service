from datetime import datetime

from flask import jsonify
from flask_jwt_extended import current_user, get_current_user, jwt_required
from flask_restful import Resource
from models.db_models import User, UserLoginHistory
from flask_jwt_extended.exceptions import FreshTokenRequired


class ShowUserLogInHistory(Resource):
    @jwt_required(fresh=True)
    def get(self):
        """
        Получение пользователем истории входов в аккаунт (5 последних входов)
        Для получения истории входов требуется "свежий" jwt access token (необходимо выполнить login)
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
        user: User = current_user
        user_history: list(UserLoginHistory) = user.login_history
        login_time = []
        login_user_agent = []
        for item in user_history:
            login_time.append(
                datetime.strftime(item.login_at, '%Y-%m-%d %H:%M:%S')
            )
            login_user_agent.append(item.user_agent)
        last_five_logins = []
        for time, agent in zip(login_time[:5], login_user_agent[:5]):
            last_five_logins.append({'login_time': time, 'login_agent': agent})
        return {'Last five logins': f'{last_five_logins}'}, 200
