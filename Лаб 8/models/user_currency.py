from typing import Any
from .user import User
from .currency import Currency

class UserCurrency:
    """Связь: пользователь — подписка на валюту."""

    def __init__(self, id_: int, user: User, currency: Currency) -> None:
        self.id = id_
        self.user = user
        self.currency = currency

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, v: int) -> None:
        if not isinstance(v, int) or v < 0:
            raise ValueError("id must be non-negative int")
        self._id = v

    @property
    def user(self) -> User:
        return self._user

    @user.setter
    def user(self, v: User) -> None:
        if not isinstance(v, User):
            raise TypeError("user must be User")
        self._user = v

    @property
    def currency(self) -> Currency:
        return self._currency

    @currency.setter
    def currency(self, v: Currency) -> None:
        if not isinstance(v, Currency):
            raise TypeError("currency must be Currency")
        self._currency = v
