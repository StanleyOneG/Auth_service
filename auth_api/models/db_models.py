from werkzeug.security import (generate_password_hash,
                               check_password_hash)
from sqlalchemy import (create_engine,
                        Column,
                        ForeignKey,
                        Index,
                        Integer,
                        String,
                        Text,
                        UniqueConstraint,
                        DateTime,
                        MetaData,
                        schema)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.config import (DB_URI,
                         POSTGRES_SCHEMA_NAME)

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
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    permission_id = Column(UUID(as_uuid=True), ForeignKey('permission.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'permission_id'),)
class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True)
    login = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    password = Column(String, nullable=False)
    user_info = relationship('UserInfo', back_populates='user', uselist=False)
    permissions = relationship('UserPermission')
    login_history = relationship('UserLoginHistory', back_populates='user', order_by='UserLoginHistory.login_at.desc()')

    __table_args__ = (UniqueConstraint('login', 'email'),)

    def set_password(self, password:str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password:str) -> None:
        return check_password_hash(self.password, password)


class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    age = Column(Integer)
    user = relationship('User', back_populates='user_info')


class Permission(Base):
    __tablename__ = 'permission'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    # user = relationship('User', secondary='user_permission', back_populates='permissions')




class UserLoginHistory(Base):
    __tablename__ = 'user_login_history'
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    login_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_agent = Column(Text, nullable=False)
    user = relationship('User', back_populates='login_history')


Index('user_login_history_login_at_idx', UserLoginHistory.login_at)

Base.metadata.create_all(engine)
