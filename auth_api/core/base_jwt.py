from abc import abstractmethod


class BaseJWT:
    @abstractmethod
    def create_jwt_tokens(*args, **kwargs):
        pass

    @abstractmethod
    def refresh_access_jwt_token(*args, **kwargs):
        pass

    @abstractmethod
    def create_login_access_token(*args, **kwargs):
        pass
