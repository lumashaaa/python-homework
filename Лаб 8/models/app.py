from .author import Author

class App:
    def __init__(self, name: str, version: str, author: Author) -> None:
        self.name = name
        self.version = version
        self.author = author
