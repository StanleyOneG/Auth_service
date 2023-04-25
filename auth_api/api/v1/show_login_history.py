from datetime import datetime

from core.log_tracer import trace_this
from db.db_alchemy import db
from flask import jsonify, request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from models.db_models import UserLoginHistory


class ShowUserLogInHistory(Resource):
    @trace_this
    @jwt_required(fresh=True)
    def get(self):
        """
        Получение пользователем истории входов в аккаунт (5 последних входов)
        Для получения истории входов требуется "свежий" jwt access token (необходимо выполнить login)
        ---
        parameters:
          - name: page
            in: query
            description: Номер страницы
            required: false
            type: integer
            format: int64
            default: 1
        responses:
          200:
            description: Список объектов с датой и временем входа и информацией об user-агенте пользователя.
        tags:
          - User
        produces:
          - application/json
        security:
          - JWT: []
        """
        user_history_query = (
            db.session.query(UserLoginHistory)
            .filter_by(user_id=current_user.id)
            .order_by(UserLoginHistory.login_at.desc())
        )

        page = db.paginate(
            user_history_query,
            page=request.args.get('page', 1, type=int),
            per_page=5,
        )

        # Extract the relevant data for each login history item
        logins = []
        for item in page.items:
            login_time = datetime.strftime(item.login_at, '%Y-%m-%d %H:%M:%S')
            login_agent = item.user_agent
            logins.append(
                {'login_time': login_time, 'user_agent': login_agent}
            )

        # Return the last five logins as a JSON response
        return jsonify(logins)
