from typing import Any

class Currency:
    """Модель валюты."""
    def __init__(
        self,
        id_: str,
        num_code: int,
        char_code: str,
        name: str,
        value: float,
        nominal: int = 1,
    ) -> None:
        self.id = id_
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, v: str) -> None:
        if not isinstance(v, str) or not v:
            raise ValueError("id must be non-empty string")
        self._id = v

    @property
    def num_code(self) -> int:
        return self._num_code

    @num_code.setter
    def num_code(self, v: int) -> None:
        if not isinstance(v, int) or v < 0:
            raise ValueError("num_code must be non-negative int")
        self._num_code = v

    @property
    def char_code(self) -> str:
        return self._char_code

    @char_code.setter
    def char_code(self, v: str) -> None:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("char_code must be non-empty string")
        self._char_code = v.strip()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, v: str) -> None:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("name must be non-empty string")
        self._name = v.strip()

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, v: float) -> None:
        try:
            v2 = float(v)
        except Exception:
            raise ValueError("value must be convertible to float")
        self._value = v2

    @property
    def nominal(self) -> int:
        return self._nominal

    @nominal.setter
    def nominal(self, v: int) -> None:
        if not isinstance(v, int) or v <= 0:
            raise ValueError("nominal must be positive int")
        self._nominal = v

    def effective_rate(self) -> float:
        return self.value / self.nominal
