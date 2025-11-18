# models/production.py
from typing import List

# Comentarios en español; nombres en inglés

class Production:
    def __init__(self, left: str, rights: List[str]):
        self.left = left
        self.rights = list(rights)

    def add_right(self, right: str):
        self.rights.append(right)

    def to_dict(self):
        return {self.left: self.rights}
