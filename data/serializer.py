# data/serializer.py
from models.grammar import Grammar


def save_grammar(grammar: Grammar, filename: str):
    grammar.save(filename)

def load_grammar(filename: str) -> Grammar:
    return Grammar.load(filename)
