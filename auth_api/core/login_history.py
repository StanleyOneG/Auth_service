import uuid
from datetime import datetime
from functools import wraps

from db.db_alchemy import db
from flask import Response, request
from models.db_models import User, UserLoginHistory


def log_user_login_action(func):
    """
    User login action decorator.
    Only applicable when function recieves user email from form.

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        response: Response = func(*args, **kwargs)
        try:
            if response.status_code == 200:
                email = request.form.get('email')
                user = db.session.query(User).filter_by(email=email).first()
                if user:
                    user_agent = request.headers.get('User-Agent')
                    login_time = datetime.utcnow()
                    user_login_log = UserLoginHistory(
                        id=uuid.uuid4(),
                        user_id=user.id,
                        login_at=login_time,
                        user_agent=user_agent,
                    )
                    db.session.add(user_login_log)
                    db.session.commit()
                    return response
        except AttributeError:
            return response

    return wrapper
