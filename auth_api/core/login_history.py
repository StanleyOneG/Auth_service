import uuid
from datetime import datetime
from functools import wraps

from db.db_alchemy import db
from flask import Response, request, session
from models.db_models import User, UserLoginHistory


def log_user_login_action(oauth: bool = False):
    """
    User login action decorator.

    Params:
        oauth (bool): True if user is logged in via OAuth, False otherwise.

    Returns:
        inner_wrapper: Decorated function.

    Note:
        If function recieves user email from form, set `oauth` parameter to `False` so decorator will log user login
        action.

        If function realises authentication via OAuth, it must set `email` parameter to `session` \n
        ex: `session['email'] = {user's email}`

    """

    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            response: Response = func(*args, **kwargs)
            try:
                if response.status_code == 200:
                    if oauth:
                        email = session.get('email')
                    else:
                        email = request.form.get('email')
                    user = (
                        db.session.query(User).filter_by(email=email).first()
                    )
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

        return inner_wrapper

    return wrapper
