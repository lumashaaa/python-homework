class Author:
    def __init__(self, name: str, group: str) -> None:
        self.name = name
        self.group = group

    def __str__(self) -> str:
        return f"{self.name} ({self.group})"
