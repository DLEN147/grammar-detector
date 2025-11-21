# models/production.py
from typing import List, Set, Optional

class Production:
    """
    Representa una producción de gramática formal.
    Una producción tiene la forma: left → right1 | right2 | ... | rightn
    """
    
    def __init__(self, left: str, rights: List[str]):
        """
        Inicializa una producción.
        
        Args:
            left: Lado izquierdo de la producción (α)
            rights: Lista de lados derechos posibles (β1, β2, ...)
        """
        if not left:
            raise ValueError("El lado izquierdo de una producción no puede estar vacío")
        
        self.left = left
        self.rights = list(rights) if rights else []
    
    def add_right(self, right: str):
        """Añade una alternativa al lado derecho de la producción"""
        if right and right not in self.rights:
            self.rights.append(right)
    
    def remove_right(self, right: str):
        """Elimina una alternativa del lado derecho"""
        if right in self.rights:
            self.rights.remove(right)
    
    def has_epsilon(self) -> bool:
        """Verifica si la producción genera epsilon (ε)"""
        return 'ε' in self.rights
    
    def get_symbols_in_left(self) -> Set[str]:
        """Obtiene todos los símbolos únicos del lado izquierdo"""
        return set(self.left)
    
    def get_symbols_in_rights(self) -> Set[str]:
        """Obtiene todos los símbolos únicos de todos los lados derechos"""
        symbols = set()
        for right in self.rights:
            if right != 'ε':
                symbols.update(set(right))
        return symbols
    
    def validate_symbols(self, symbol_sets) -> Optional[str]:
        """
        Valida que todos los símbolos usados estén declarados.
        
        Args:
            symbol_sets: Instancia de SymbolSets con los símbolos válidos
            
        Returns:
            None si es válido, mensaje de error si no
        """
        # Validar lado izquierdo
        error = symbol_sets.validate_string(self.left)
        if error:
            return f"En producción '{self.left}': {error}"
        
        # Validar lados derechos
        for right in self.rights:
            error = symbol_sets.validate_string(right)
            if error:
                return f"En producción '{self.left} → {right}': {error}"
        
        return None
    
    def is_type_3_compliant(self, symbol_sets, style: str = 'right') -> bool:
        """
        Verifica si la producción cumple con gramática Type 3 (Regular).
        
        Args:
            symbol_sets: Instancia de SymbolSets
            style: 'right' para A→aB, 'left' para A→Ba
            
        Returns:
            True si cumple Type 3, False si no
        """
        # Left debe ser un único no terminal
        if len(self.left) != 1 or not symbol_sets.is_nonterminal(self.left):
            return False
        
        for prod in self.rights:
            # ε es válido
            if prod == 'ε':
                continue
            
            # A → a (terminal único)
            if len(prod) == 1 and symbol_sets.is_terminal(prod):
                continue
            
            # A → aB o A → Ba
            if len(prod) == 2:
                if style == 'right':
                    # Right-linear: A → aB
                    if not (symbol_sets.is_terminal(prod[0]) and 
                           symbol_sets.is_nonterminal(prod[1])):
                        return False
                elif style == 'left':
                    # Left-linear: A → Ba
                    if not (symbol_sets.is_nonterminal(prod[0]) and 
                           symbol_sets.is_terminal(prod[1])):
                        return False
                else:
                    return False
            else:
                return False
        
        return True
    
    def is_type_2_compliant(self, symbol_sets) -> bool:
        """
        Verifica si la producción cumple con gramática Type 2 (Libre de Contexto).
        
        Returns:
            True si cumple Type 2, False si no
        """
        # Left debe ser un único no terminal
        return (len(self.left) == 1 and 
                symbol_sets.is_nonterminal(self.left))
    
    def is_type_1_compliant(self, start_symbol: str) -> bool:
        """
        Verifica si la producción cumple con gramática Type 1 (Sensible al Contexto).
        Regla: |α| ≤ |β|, excepto S → ε si S no aparece en ningún lado derecho
        
        Returns:
            True si cumple Type 1, False si no
        """
        for prod in self.rights:
            if prod == 'ε':
                # Solo S puede producir ε
                if self.left != start_symbol:
                    return False
            elif len(self.left) > len(prod):
                return False
        
        return True
    
    def to_dict(self):
        """Convierte la producción a formato diccionario"""
        return {self.left: self.rights}
    
    def __str__(self) -> str:
        """Representación en string legible"""
        rights_str = ' | '.join(self.rights) if self.rights else '∅'
        return f"{self.left} → {rights_str}"
    
    def __repr__(self) -> str:
        return f"Production('{self.left}' → {self.rights})"
    
    def __eq__(self, other) -> bool:
        """Comparación de igualdad entre producciones"""
        if not isinstance(other, Production):
            return False
        return self.left == other.left and set(self.rights) == set(other.rights)