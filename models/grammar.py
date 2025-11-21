import json
from collections import deque
from typing import Dict, List, Set, Tuple, Optional, Any

from models.symbols import SymbolSets
from models.production import Production

# Comentarios en español, código en inglés

class Grammar:
    
    def __init__(self, nonterminals: Set[str], terminals: Set[str],
                 productions: Dict[str, List[str]], start_symbol: str,
                 max_derivation_length: int = 100):
        """
        Inicializa una gramática formal.
        
        Args:
            nonterminals: Conjunto de símbolos no terminales
            terminals: Conjunto de símbolos terminales
            productions: Diccionario de producciones {left: [right1, right2, ...]}
            start_symbol: Símbolo inicial de la gramática
            max_derivation_length: Longitud máxima para derivaciones
        """
        # Crear conjuntos de símbolos con validación
        self.symbols = SymbolSets(nonterminals, terminals)
        
        # Validar símbolo inicial
        if start_symbol not in self.symbols.nonterminals:
            raise ValueError(f"El símbolo inicial '{start_symbol}' debe ser un no terminal")
        
        self.S: str = start_symbol
        
        # Crear objetos Production y validar
        self.productions: List[Production] = []
        self._load_productions(productions)
        
        # Crear diccionario de acceso rápido
        self.P: Dict[str, List[str]] = {p.left: p.rights for p in self.productions}
        
        # Configuración
        self.max_derivation_length = max_derivation_length
        
        # Clasificar tipo de gramática
        self.type = self._classify_grammar()
        self.grammar_style = self._detect_grammar_style()
    
    def _load_productions(self, productions: Dict[str, List[str]]):
        """Carga y valida las producciones"""
        for left, rights in productions.items():
            # FIX: Validar que rights no esté vacío
            if not rights:
                raise ValueError(f"La producción '{left}' debe tener al menos un lado derecho")
            
            prod = Production(left, rights)
            
            # Validar símbolos
            error = prod.validate_symbols(self.symbols)
            if error:
                raise ValueError(error)
            
            self.productions.append(prod)
    
    def _detect_grammar_style(self) -> Optional[str]:
        """Detecta si es gramática regular right-linear o left-linear"""
        if self.type != 3:
            return None
        
        has_right = False
        has_left = False
        
        for prod in self.productions:
            for right in prod.rights:
                if right == 'ε' or len(right) == 1:
                    continue
                
                if len(right) == 2:
                    if (self.symbols.is_terminal(right[0]) and 
                        self.symbols.is_nonterminal(right[1])):
                        has_right = True
                    elif (self.symbols.is_nonterminal(right[0]) and 
                          self.symbols.is_terminal(right[1])):
                        has_left = True
        
        if has_right and not has_left:
            return 'right'
        elif has_left and not has_right:
            return 'left'
        elif not has_right and not has_left:
            return 'right'  # Default
        else:
            return 'mixed'  # Debería ser imposible si type==3
    
    def _classify_grammar(self) -> int:
        """Clasifica la gramática según jerarquía de Chomsky"""
        is_type_3_right = True
        is_type_3_left = True
        is_type_2 = True
        is_type_1 = True
        
        for prod in self.productions:
            # Type 2 y 3 requieren lado izquierdo = único no terminal
            if not prod.is_type_2_compliant(self.symbols):
                is_type_2 = False
                is_type_3_right = False
                is_type_3_left = False
            
            # Verificar Type 3
            if is_type_3_right and not prod.is_type_3_compliant(self.symbols, 'right'):
                is_type_3_right = False
            
            if is_type_3_left and not prod.is_type_3_compliant(self.symbols, 'left'):
                is_type_3_left = False
            
            # Verificar Type 1
            if not prod.is_type_1_compliant(self.S):
                is_type_1 = False
        
        # Verificar que S no aparezca en lados derechos si S→ε existe
        if is_type_1:
            s_produces_epsilon = any(
                p.left == self.S and p.has_epsilon() 
                for p in self.productions
            )
            if s_produces_epsilon:
                for prod in self.productions:
                    for right in prod.rights:
                        if self.S in right and right != 'ε':
                            is_type_1 = False
                            break
        
        # Retornar el tipo más específico
        if is_type_3_right or is_type_3_left:
            return 3
        elif is_type_2:
            return 2
        elif is_type_1:
            return 1
        else:
            return 0
    
    def get_type_name(self) -> str:
        """Obtiene nombre descriptivo del tipo de gramática"""
        nombres = {
            3: "Tipo 3 (Regular)",
            2: "Tipo 2 (Libre de Contexto)",
            1: "Tipo 1 (Sensible al Contexto)",
            0: "Tipo 0 (Irrestricta)"
        }
        name = nombres[self.type]
        if self.type == 3 and self.grammar_style:
            name += f" - {self.grammar_style}-linear"
        return name
    
    def parse(self, string: str) -> Tuple[bool, Optional[dict]]:
        """
        Intenta parsear una cadena según el tipo de gramática.
        
        Returns:
            (accepted, derivation_tree_or_info)
        """
        if self.type == 3:
            return self._parse_type3(string)
        elif self.type == 2:
            # Usar Earley para CFGs (Type 2)
            return self._parse_type2(string)
        else:
            return self._parse_general(string)
    
    # ------------------ Type 3 parser (BFS con autómata) ------------------
    def _parse_type3(self, string: str) -> Tuple[bool, Optional[dict]]:
        """Parser optimizado para gramáticas regulares"""
        target = string if string else ''
        
        # FIX: Para left-linear, procesar de derecha a izquierda
        if self.grammar_style == 'left':
            return self._parse_type3_left(target)
        else:
            return self._parse_type3_right(target)
    
    def _parse_type3_right(self, target: str) -> Tuple[bool, Optional[dict]]:
        """Parser para gramáticas right-linear"""
        # BFS: (estado_actual, posición_en_target, historial_derivaciones)
        queue = deque([(self.S, 0, [f"Inicio: {self.S}"])])
        visited = set()
        max_steps = 50000
        steps = 0
        
        while queue and steps < max_steps:
            steps += 1
            state, pos, history = queue.popleft()
            
            # Evitar ciclos
            key = (state, pos)
            if key in visited:
                continue
            visited.add(key)
            
            # ¿Estado no tiene producciones?
            if state not in self.P:
                continue
            
            # ¿Llegamos al final del input?
            if pos == len(target):
                # Necesitamos producción a epsilon
                if 'ε' in self.P[state]:
                    final_history = history + [f"{state} → ε"]
                    tree = self._build_linear_tree(final_history)
                    return True, tree
                continue
            
            current_symbol = target[pos]
            
            for prod_right in self.P[state]:
                if prod_right == 'ε':
                    # Epsilon solo válido al final
                    continue
                
                # FIX: A → a (terminal único) - puede estar en cualquier posición
                if len(prod_right) == 1 and self.symbols.is_terminal(prod_right):
                    if prod_right == current_symbol:
                        # Si consumimos el símbolo y estamos al final, aceptamos
                        if pos == len(target) - 1:
                            final_history = history + [f"{state} → {prod_right}"]
                            tree = self._build_linear_tree(final_history)
                            return True, tree
                
                # Right-linear: A → aB
                elif (len(prod_right) == 2 and 
                      self.symbols.is_terminal(prod_right[0]) and
                      self.symbols.is_nonterminal(prod_right[1])):
                    
                    if prod_right[0] == current_symbol:
                        new_state = prod_right[1]
                        new_history = history + [f"{state} → {prod_right}"]
                        queue.append((new_state, pos + 1, new_history))
        
        return False, None
    
    def _parse_type3_left(self, target: str) -> Tuple[bool, Optional[dict]]:
        """Parser para gramáticas left-linear (procesa de derecha a izquierda)"""
        # BFS: (estado_actual, posición_desde_final, historial_derivaciones)
        queue = deque([(self.S, len(target), [f"Inicio: {self.S}"])])
        visited = set()
        max_steps = 50000
        steps = 0
        
        while queue and steps < max_steps:
            steps += 1
            state, pos, history = queue.popleft()
            
            # Evitar ciclos
            key = (state, pos)
            if key in visited:
                continue
            visited.add(key)
            
            if state not in self.P:
                continue
            
            # ¿Llegamos al principio del input?
            if pos == 0:
                if 'ε' in self.P[state]:
                    final_history = history + [f"{state} → ε"]
                    tree = self._build_linear_tree(final_history)
                    return True, tree
                continue
            
            current_symbol = target[pos - 1]
            
            for prod_right in self.P[state]:
                if prod_right == 'ε':
                    continue
                
                # A → a (terminal único)
                if len(prod_right) == 1 and self.symbols.is_terminal(prod_right):
                    if prod_right == current_symbol and pos == 1:
                        final_history = history + [f"{state} → {prod_right}"]
                        tree = self._build_linear_tree(final_history)
                        return True, tree
                
                # Left-linear: A → Ba
                elif (len(prod_right) == 2 and 
                      self.symbols.is_nonterminal(prod_right[0]) and
                      self.symbols.is_terminal(prod_right[1])):
                    
                    if prod_right[1] == current_symbol:
                        new_state = prod_right[0]
                        new_history = history + [f"{state} → {prod_right}"]
                        queue.append((new_state, pos - 1, new_history))
        
        return False, None
    
    # ------------------ Type 2 parser (Earley) ------------------
    def _parse_type2(self, string: str) -> Tuple[bool, Optional[dict]]:
        """Parser para gramáticas libres de contexto usando algoritmo Earley"""
        accepted, chart = self._earley_parse(string)
        
        # FIX: Generar derivaciones para visualización
        derivations = []
        if accepted:
            derivations = self._build_earley_derivations(string, chart)
        
        # Recolectar estados completados
        completed_states = []
        if len(chart) > len(string):
            for st in chart[len(string)]:
                lhs, rhs, dot, start_pos = st
                if dot == len(rhs):
                    completed_states.append({
                        "lhs": lhs,
                        "rhs": "".join(rhs) if rhs else "ε",
                        "start": start_pos,
                        "end": len(string)
                    })
        
        info = {
            "type": "earley",
            "input": string,
            "accepted": accepted,
            "chart_sizes": [len(s) for s in chart],
            "completed": completed_states[:30],
            "derivations": derivations  # FIX: Agregar derivaciones
        }
        return accepted, info
    
    def _build_earley_derivations(self, string: str, chart: List[Set[Tuple[str, Tuple[str, ...], int, int]]]) -> List[str]:
        """Construye una lista de derivaciones a partir del chart de Earley"""
        derivations = [f"Inicio: {self.S}"]
        
        # Buscar un estado completado de S que cubra toda la entrada
        final_states = []
        n = len(string)
        
        for st in chart[n]:
            lhs, rhs, dot, start_pos = st
            if lhs == self.S and dot == len(rhs) and start_pos == 0:
                final_states.append(st)
        
        if not final_states:
            return derivations
        
        # Tomar el primer estado final
        final_state = final_states[0]
        
        # Reconstruir derivación de forma simplificada
        # Mostrar las producciones principales aplicadas
        production_sequence = self._trace_earley_derivation(final_state, chart, string)
        
        for i, prod in enumerate(production_sequence, 1):
            derivations.append(f"Paso {i}: {prod}")
        
        derivations.append(f"Resultado final: {string if string else 'ε'}")
        
        return derivations
    
    def _trace_earley_derivation(self, state: Tuple[str, Tuple[str, ...], int, int], 
                                  chart: List[Set[Tuple[str, Tuple[str, ...], int, int]]], 
                                  string: str) -> List[str]:
        """Traza las producciones aplicadas (versión simplificada)"""
        lhs, rhs, dot, start_pos = state
        productions = []
        
        # Mostrar la producción principal
        rhs_str = "".join(rhs) if rhs else "ε"
        productions.append(f"{lhs} → {rhs_str}")
        
        # Buscar producciones de los no terminales en rhs
        pos = start_pos
        for symbol in rhs:
            if self.symbols.is_nonterminal(symbol):
                # Buscar estados completados de este símbolo
                for end_pos in range(pos + 1, len(string) + 1):
                    if end_pos < len(chart):
                        for st in chart[end_pos]:
                            st_lhs, st_rhs, st_dot, st_start = st
                            if (st_lhs == symbol and st_dot == len(st_rhs) and 
                                st_start == pos):
                                st_rhs_str = "".join(st_rhs) if st_rhs else "ε"
                                productions.append(f"{st_lhs} → {st_rhs_str}")
                                pos = end_pos
                                break
            elif self.symbols.is_terminal(symbol):
                pos += 1
        
        return productions
    
    def _earley_parse(self, input_string: str) -> Tuple[bool, List[Set[Tuple[str, Tuple[str, ...], int, int]]]]:
        """
        FIX: Simplificación del algoritmo Earley
        Estado representado como tupla: (lhs, rhs_tuple, dot, start_pos)
        """
        # Preparar producciones
        grammar_productions: Dict[str, List[Tuple[str, ...]]] = {}
        for prod in self.productions:
            rhs_list = []
            for r in prod.rights:
                if r == 'ε':
                    rhs_list.append(tuple())
                else:
                    rhs_list.append(tuple(r))
            grammar_productions.setdefault(prod.left, []).extend(rhs_list)
        
        tokens = list(input_string) if input_string else []
        n = len(tokens)
        chart: List[Set[Tuple[str, Tuple[str, ...], int, int]]] = [set() for _ in range(n + 1)]
        
        def add_state(i: int, state: Tuple[str, Tuple[str, ...], int, int]) -> bool:
            if state not in chart[i]:
                chart[i].add(state)
                return True
            return False
        
        # Inicializar con producciones de S
        for rhs in grammar_productions.get(self.S, []):
            add_state(0, (self.S, rhs, 0, 0))
        
        # Main loop
        for i in range(n + 1):
            changed = True
            while changed:
                changed = False
                states = list(chart[i])
                
                for state in states:
                    lhs, rhs, dot, start_pos = state
                    
                    if dot < len(rhs):
                        next_sym = rhs[dot]
                        
                        # PREDICT
                        if self.symbols.is_nonterminal(next_sym):
                            for prod_rhs in grammar_productions.get(next_sym, []):
                                if add_state(i, (next_sym, prod_rhs, 0, i)):
                                    changed = True
                        
                        # SCAN
                        elif i < n and self.symbols.is_terminal(next_sym) and tokens[i] == next_sym:
                            add_state(i + 1, (lhs, rhs, dot + 1, start_pos))
                    
                    else:
                        # COMPLETE
                        for st2 in list(chart[start_pos]):
                            lhs2, rhs2, dot2, start2 = st2
                            if dot2 < len(rhs2) and rhs2[dot2] == lhs:
                                if add_state(i, (lhs2, rhs2, dot2 + 1, start2)):
                                    changed = True
        
        # Verificar aceptación
        accepted = any(
            st[0] == self.S and st[2] == len(st[1]) and st[3] == 0
            for st in chart[n]
        )
        
        return accepted, chart
    
    # ------------------ General parser for type 0/1 ------------------
    def _parse_general(self, string: str, max_steps: int = 10000) -> Tuple[bool, Optional[dict]]:
        """FIX: Parser general mejorado para Type 0 y Type 1"""
        target = string if string else ''
        
        queue = deque([(self.S, [f"Inicio: {self.S}"])])
        visited = {self.S}
        steps = 0
        
        # FIX: Poda menos agresiva
        max_form_length = max(len(target) * 3 + 50, 100)
        
        while queue and steps < max_steps:
            steps += 1
            form, derivation = queue.popleft()
            
            if form == target:
                tree = self._build_linear_tree(derivation)
                return True, tree
            
            # Aplicar todas las producciones posibles
            for prod in self.productions:
                left = prod.left
                pos = 0
                
                while pos <= len(form) - len(left):
                    if form[pos:pos + len(left)] == left:
                        for right in prod.rights:
                            if right == 'ε':
                                new_form = form[:pos] + form[pos + len(left):]
                            else:
                                new_form = form[:pos] + right + form[pos + len(left):]
                            
                            # Poda mejorada
                            if len(new_form) <= max_form_length:
                                if new_form not in visited:
                                    visited.add(new_form)
                                    new_deriv = derivation + [f"{left} → {right} ⇒ {new_form}"]
                                    queue.append((new_form, new_deriv))
                    pos += 1
        
        return False, None
    
    # ------------------ Helpers ------------------
    def _build_linear_tree(self, derivation: List[str]) -> dict:
        """Construye representación simple de derivación lineal"""
        return {
            "symbol": self.S,
            "derivations": derivation,
            "type": "linear"
        }
    
    def generate_strings(self, n: int = 10, max_length: int = 30) -> List[str]:
        """
        FIX: Generación mejorada de cadenas válidas
        """
        strings: Set[str] = set()
        queue = deque([self.S])
        visited = {self.S}
        max_iter = 50000
        it = 0
        
        while len(strings) < n and queue and it < max_iter:
            it += 1
            current = queue.popleft()
            
            # Si es terminal o epsilon, agregar
            if self.symbols.all_terminals(current) or current == 'ε':
                cleaned = current.replace('ε', '')
                if not cleaned:
                    cleaned = 'ε'
                strings.add(cleaned)
                if len(strings) >= n:
                    break
                continue
            
            # Aplicar producciones
            for prod in self.productions:
                left = prod.left
                pos = 0
                
                while pos <= len(current) - len(left):
                    if current[pos:pos + len(left)] == left:
                        for right in prod.rights:
                            if right == 'ε':
                                new_form = current[:pos] + current[pos + len(left):]
                            else:
                                new_form = current[:pos] + right + current[pos + len(left):]
                            
                            # FIX: Evitar duplicados y controlar longitud
                            if new_form not in visited and len(new_form) <= max_length:
                                visited.add(new_form)
                                queue.append(new_form)
                                break  # Solo una sustitución por iteración
                    pos += 1
                    break  # Solo primera ocurrencia
        
        # Convertir a lista ordenada
        result = sorted(list(strings), key=lambda x: (len(x), x))
        return result[:n]
    
    def visualize_tree(self, tree: Optional[dict], level: int = 0) -> str:
        """Genera una representación textual del árbol de derivación"""
        if not tree:
            return "No hay árbol de derivación"
        
        result = f"Tipo de gramática: {self.get_type_name()}\n\n"
        result += "Derivación:\n"
        result += "=" * 50 + "\n"
        
        derivations = tree.get('derivations', [])
        if derivations:
            for i, step in enumerate(derivations, 1):
                result += f"{i}. {step}\n"
        else:
            result += "(No se pudo generar el historial de derivación)\n"
        
        return result
    
    # ------------------ Persistence ------------------
    def save(self, filename: str):
        """Guarda la gramática en formato JSON"""
        data = {
            "nonterminals": list(self.symbols.nonterminals),
            "terminals": list(self.symbols.terminals),
            "productions": {p.left: p.rights for p in self.productions},
            "start_symbol": self.S,
            "type": self.type,
            "grammar_style": self.grammar_style
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Gramática guardada en {filename}")
    
    @staticmethod
    def load(filename: str) -> 'Grammar':
        """Carga una gramática desde archivo JSON"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return Grammar(
            set(data['nonterminals']),
            set(data['terminals']),
            data['productions'],
            data['start_symbol']
        )
    
    def __str__(self) -> str:
        """Representación en string de la gramática"""
        result = f"Gramática {self.get_type_name()}\n"
        result += f"Símbolo inicial: {self.S}\n"
        result += f"No terminales: {self.symbols.nonterminals}\n"
        result += f"Terminales: {self.symbols.terminals}\n"
        result += "Producciones:\n"
        for prod in self.productions:
            result += f"  {prod}\n"
        return result