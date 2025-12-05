from typing import Any


class User:
    """Модель пользователя."""

    def __init__(self, id_: int, name: str) -> None:
        self.id = id_
        self.name = name

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, v: int) -> None:
        if not isinstance(v, int) or v < 0:
            raise ValueError("id must be non-negative int")
        self._id = v

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, v: str) -> None:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("name must be non-empty str")
        self._name = v.strip()
