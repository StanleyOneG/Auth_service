from core.config import DB_URI, POSTGRES_SCHEMA_NAME
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    String,
    Text,
    UniqueConstraint,
    create_engine,
    schema,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

engine = create_engine(DB_URI)

with engine.connect() as conn:
    if not conn.dialect.has_schema(conn, POSTGRES_SCHEMA_NAME):
        conn.execute(schema.CreateSchema(POSTGRES_SCHEMA_NAME, True))
        conn.commit()

metadata_obj = MetaData(schema=POSTGRES_SCHEMA_NAME)
Base = declarative_base(metadata=metadata_obj)


class UserPermission(Base):
    __tablename__ = 'user_permission'
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False,
    )
    permission_id = Column(
        UUID(as_uuid=True),
        ForeignKey('permission.id', ondelete='CASCADE'),
        nullable=False,
    )
    permission = relationship('Permission')

    __table_args__ = (UniqueConstraint('user_id', 'permission_id'),)


class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True)
    login = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    password = Column(String, nullable=False)
    user_info = relationship('UserInfo', back_populates='user', uselist=False)
    permissions = relationship('UserPermission')
    login_history = relationship(
        'UserLoginHistory',
        back_populates='user',
        order_by='UserLoginHistory.login_at.desc()',
    )

    __table_args__ = (UniqueConstraint('login', 'email'),)

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False,
    )
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    age = Column(Integer)
    user = relationship('User', back_populates='user_info', uselist=False)


class Permission(Base):
    __tablename__ = 'permission'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(Text, nullable=False, unique=True)



class UserLoginHistory(Base):
    __tablename__ = 'user_login_history'
    __table_args__ = (
        UniqueConstraint('id', 'login_at', 'user_agent', name='uq_user_login_history_id_login_at_user_agent'),
        {
            'postgresql_partition_by': 'RANGE (login_at)',
        }
    )
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False,
    )
    login_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, primary_key=True
    )
    user_agent = Column(Text, nullable=False)
    user = relationship('User', back_populates='login_history')


# Base.metadata.create_all(engine)
