"""Help module for cli commands"""
import uuid
import click
from core.config import (
    SUPERUSER_EMAIL,
    SUPERUSER_LOGIN,
    SUPERUSER_PASSWORD
)
import logging
from sqlalchemy.orm import sessionmaker
from models.db_models import (
    engine,
    User,
    Permission,
    UserPermission
)
from flask import Blueprint

logger = logging.getLogger(__name__)
superuser_bp = Blueprint('superuser', __name__)


@superuser_bp.cli.command("create_superuser")
@click.option('--login')
@click.option('--email')
@click.option('--password')
def create_superuser(login:str=SUPERUSER_LOGIN,
                     email:str=SUPERUSER_EMAIL,
                     password:str=SUPERUSER_PASSWORD):

    logger.info("============= Superuser creation ===============")
    Session = sessionmaker(bind=engine)
    session = Session()
    if (
        session.query(User).filter_by(email=email).first()
        is not None
    ):
        logger.info(
            "Superuser with provided email already exists. Abort creating"
        )
        return
    db_user = User()
    db_user.id = uuid.uuid4()
    db_user.login = login
    db_user.email = email
    db_user.set_password(password)
    session.add(db_user)
    session.commit()
    logger.info("Superuser added")
    db_permission = Permission()
    db_permission.id = uuid.uuid4()
    db_permission.name = "admin"
    session.add(db_permission)
    session.commit()
    logger.info("Permission 'admin' created")

    db_user_permission = UserPermission()
    db_user_permission.id = uuid.uuid4()
    db_user_permission.permission_id = db_permission.id
    db_user_permission.user_id = db_user.id
    session.add(db_user_permission)
    session.commit()
    logger.info("Permission 'admin' atached to superuser")
    logger.info("============= Superuser creation ===============")
