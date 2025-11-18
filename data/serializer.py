# data/serializer.py
from models.grammar import Grammar

# Funciones wrapper para serializar/deserialize usando los métodos de la clase Grammar

def save_grammar(grammar: Grammar, filename: str):
    """Guarda la gramática en archivo (wrapper)."""
    grammar.save(filename)

def load_grammar(filename: str) -> Grammar:
    """Carga la gramática desde archivo (wrapper)."""
    return Grammar.load(filename)
