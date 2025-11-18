# models/symbols.py
from typing import Set

class SymbolSets:
    """Contenedor simple para terminales y no terminales"""
    def __init__(self, nonterminals: Set[str], terminals: Set[str]):
        self.nonterminals = set(nonterminals)
        self.terminals = set(terminals)

    def __contains__(self, item: str) -> bool:
        # Comprueba en no terminales o terminales (útil en algunas comprobaciones)
        return item in self.nonterminals or item in self.terminals
