import datetime
from abc import abstractmethod

import jwt
from django.conf import settings


class BaseToken:
    """
    Абстракция токена
    """

    @abstractmethod
    def encode(self, **kwargs) -> str: ...

    @abstractmethod
    def decode(self, payload: dict): ...


class ConfirmationToken(BaseToken):
    """
    Токен подтверждения аккаунта по email
    """

    def encode(self, **kwargs) -> str:
        payload = {
            "email": kwargs.get("email"),
            "exp": datetime.datetime.now() + datetime.timedelta(days=1),
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    def decode(self, token: str) -> dict:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])


class AccessToken(BaseToken):
    """
    Access токен для авторизации
    """

    def encode(self, **kwargs) -> str:
        payload = {
            "email": kwargs.get("email"),
            "exp": datetime.datetime.now() + datetime.timedelta(hours=2),
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    def decode(self, payload: dict): ...
