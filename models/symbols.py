# models/symbols.py
from typing import Set, Optional

class SymbolSets:
    """
    Clase para gestionar y validar los conjuntos de símbolos terminales y no terminales
    de una gramática formal.
    """
    
    def __init__(self, nonterminals: Set[str], terminals: Set[str]):
        """
        Inicializa los conjuntos de símbolos con validación.
        
        Args:
            nonterminals: Conjunto de símbolos no terminales
            terminals: Conjunto de símbolos terminales
            
        Raises:
            ValueError: Si hay intersección entre terminales y no terminales
        """
        self.nonterminals = set(nonterminals)
        self.terminals = set(terminals)
        self._validate()
    
    def _validate(self):
        """Valida que no haya intersección entre terminales y no terminales"""
        intersection = self.nonterminals & self.terminals
        if intersection:
            raise ValueError(
                f"Los símbolos no pueden ser terminales y no terminales a la vez: {intersection}"
            )
        
        if not self.nonterminals:
            raise ValueError("Debe haber al menos un símbolo no terminal")
    
    def __contains__(self, item: str) -> bool:
        """Verifica si un símbolo existe en alguno de los conjuntos"""
        return item in self.nonterminals or item in self.terminals
    
    def is_nonterminal(self, symbol: str) -> bool:
        """Verifica si un símbolo es no terminal"""
        return symbol in self.nonterminals
    
    def is_terminal(self, symbol: str) -> bool:
        """Verifica si un símbolo es terminal"""
        return symbol in self.terminals
    
    def validate_symbol(self, symbol: str) -> Optional[str]:
        """
        Valida que un símbolo exista en la gramática.
        
        Returns:
            None si es válido, mensaje de error si no
        """
        if symbol == 'ε':
            return None
        if symbol not in self:
            return f"Símbolo '{symbol}' no está declarado en la gramática"
        return None
    
    def validate_string(self, string: str) -> Optional[str]:
        """
        Valida que todos los símbolos de una cadena existan en la gramática.
        
        Returns:
            None si es válido, mensaje de error si no
        """
        if string == 'ε':
            return None
        
        for symbol in string:
            error = self.validate_symbol(symbol)
            if error:
                return error
        return None
    
    def all_terminals(self, string: str) -> bool:
        """Verifica si todos los símbolos de una cadena son terminales"""
        if string == 'ε' or string == '':
            return True
        return all(c in self.terminals for c in string)
    
    def all_nonterminals(self, string: str) -> bool:
        """Verifica si todos los símbolos de una cadena son no terminales"""
        if string == 'ε' or string == '':
            return False
        return all(c in self.nonterminals for c in string)
    
    def has_nonterminal(self, string: str) -> bool:
        """Verifica si una cadena contiene al menos un no terminal"""
        return any(c in self.nonterminals for c in string)
    
    def get_nonterminals_in(self, string: str) -> Set[str]:
        """Obtiene todos los no terminales presentes en una cadena"""
        return {c for c in string if c in self.nonterminals}
    
    def get_terminals_in(self, string: str) -> Set[str]:
        """Obtiene todos los terminales presentes en una cadena"""
        return {c for c in string if c in self.terminals}
    
    def __repr__(self) -> str:
        return f"SymbolSets(N={self.nonterminals}, T={self.terminals})"