# models/grammar.py
import json
from collections import deque
from typing import Dict, List, Set, Tuple, Optional

# Comentarios en español, código en inglés

class Grammar:
    
    def __init__(self, nonterminals: Set[str], terminals: Set[str],
                 productions: Dict[str, List[str]], start_symbol: str):
        # Conjuntos y producciones
        self.N: Set[str] = set(nonterminals)
        self.T: Set[str] = set(terminals)
        # productions: mapping left -> list of right strings
        self.P: Dict[str, List[str]] = {k: list(v) for k, v in productions.items()}
        self.S: str = start_symbol
        # Tipo de gramática (0..3)
        self.type = self._classify_grammar()

    def _classify_grammar(self) -> int:
        is_type_3 = True
        is_type_2 = True
        is_type_1 = True

        for left, rights in self.P.items():
            # Lado izquierdo debe ser un único no terminal para tipos 2 y 3
            if len(left) != 1 or left not in self.N:
                is_type_2 = False
                is_type_3 = False

            for prod in rights:
                # Tipo 3 (regular): A -> aB ó A -> a ó A -> ε
                if is_type_3:
                    if prod == 'ε':
                        continue
                    elif len(prod) == 1:
                        if prod not in self.T:
                            is_type_3 = False
                    elif len(prod) == 2:
                        if not ((prod[0] in self.T and prod[1] in self.N) or
                                (prod[0] in self.N and prod[1] in self.T)):
                            is_type_3 = False
                    else:
                        is_type_3 = False

                # Tipo 1 (sensible al contexto): |α| ≤ |β| (excepto S->ε)
                if is_type_1:
                    if prod != 'ε' and len(left) > len(prod):
                        is_type_1 = False
                    elif prod == 'ε' and left != self.S:
                        is_type_1 = False

        if is_type_3:
            return 3
        elif is_type_2:
            return 2
        elif is_type_1:
            return 1
        else:
            return 0

    def get_type_name(self) -> str:
        nombres = {
            3: "Tipo 3 (Regular)",
            2: "Tipo 2 (Libre de Contexto)",
            1: "Tipo 1 (Sensible al Contexto)",
            0: "Tipo 0 (Irrestricta)"
        }
        return nombres[self.type]

    def parse(self, string: str) -> Tuple[bool, Optional[dict]]:
        if self.type == 3:
            return self._parse_type3(string)
        elif self.type == 2:
            return self._parse_type2(string)
        else:
            return self._parse_general(string)

    # ------------------ Type 3 parser (BFS) ------------------
    def _parse_type3(self, string: str) -> Tuple[bool, Optional[dict]]:
        if string == '':
            string = 'ε'

        target = string if string != 'ε' else ''

        # BFS nodes: (current_state, position_in_target, history)
        queue = deque([(self.S, 0, [self.S])])
        visited = set()
        max_steps = 10000
        steps = 0

        while queue and steps < max_steps:
            steps += 1
            state, pos, history = queue.popleft()

            key = (state, pos)
            if key in visited:
                continue
            visited.add(key)

            # Si llegamos al final de la cadena objetivo
            if pos == len(target):
                if state in self.P and 'ε' in self.P[state]:
                    tree = self._build_linear_tree(history + [f"{state}→ε"])
                    return True, tree
                continue

            if state not in self.P:
                continue

            current_symbol = target[pos]

            for prod in self.P[state]:
                if prod == 'ε':
                    if pos == len(target):
                        tree = self._build_linear_tree(history + [f"{state}→ε"])
                        return True, tree
                    continue

                # Regular right-linear: A -> aB or A -> a
                if len(prod) >= 1 and prod[0] == current_symbol:
                    if len(prod) == 1:
                        if pos == len(target) - 1:
                            tree = self._build_linear_tree(history + [f"{state}→{prod}"])
                            return True, tree
                    elif len(prod) == 2 and prod[1] in self.N:
                        new_state = prod[1]
                        new_history = history + [f"{state}→{prod}"]
                        queue.append((new_state, pos + 1, new_history))

                # Left-linear case: A -> Ba or A -> a (handled symmetrically)
                elif len(prod) == 2 and prod[0] in self.N and prod[1] == current_symbol:
                    new_state = prod[0]
                    new_history = history + [f"{state}→{prod}"]
                    queue.append((new_state, pos + 1, new_history))

        return False, None

    # ------------------ Type 2 parser (BFS over sentential forms) ------------------
    def _parse_type2(self, string: str) -> Tuple[bool, Optional[dict]]:
        if string == '':
            string = 'ε'
        return self._parse_bfs_type2(string)

    def _parse_bfs_type2(self, string: str) -> Tuple[bool, Optional[dict]]:
        target = string if string != 'ε' else ''
        queue = deque([(self.S, [(self.S, None, None)])])
        visited = {self.S}
        max_steps = 5000
        steps = 0

        while queue and steps < max_steps:
            steps += 1
            sentential, history = queue.popleft()

            if sentential == target:
                tree = self._build_tree_from_history(history)
                return True, tree

            if len(sentential) > len(target):
                has_nonterm = any(c in self.N for c in sentential)
                if not has_nonterm:
                    continue

            # Buscar primer no-terminal en la forma sentencial
            pos_nt = -1
            nt = None
            for i, ch in enumerate(sentential):
                if ch in self.N:
                    pos_nt = i
                    nt = ch
                    break

            if pos_nt == -1:
                continue

            if nt in self.P:
                for prod in self.P[nt]:
                    if prod == 'ε':
                        new_form = sentential[:pos_nt] + sentential[pos_nt+1:]
                    else:
                        new_form = sentential[:pos_nt] + prod + sentential[pos_nt+1:]

                    if len(new_form) <= len(target) + 10:
                        if new_form not in visited:
                            visited.add(new_form)
                            new_history = history + [(new_form, nt, prod)]
                            queue.append((new_form, new_history))

        return False, None

    def _build_tree_from_history(self, history: List[Tuple]) -> dict:
        derivations = []
        for form, nt, prod in history:
            if nt and prod:
                derivations.append(f"{nt} → {prod}: {form}")
            else:
                derivations.append(form)

        return {
            "symbol": self.S,
            "derivation": derivations,
            "type": "sequential"
        }

    # ------------------ General parser for type 0/1 ------------------
    def _parse_general(self, string: str, max_steps: int = 1000) -> Tuple[bool, Optional[dict]]:
        if string == '':
            string = 'ε'

        queue = deque([(self.S, [self.S])])
        visited = {self.S}
        steps = 0

        while queue and steps < max_steps:
            form, derivation = queue.popleft()
            steps += 1

            if form == string:
                tree = self._build_linear_tree(derivation)
                return True, tree

            # Aplicar todas las producciones posibles
            for left, rights in self.P.items():
                pos = 0
                while pos <= len(form) - len(left):
                    if form[pos:pos+len(left)] == left:
                        for prod in rights:
                            new_form = form[:pos] + prod + form[pos+len(left):]
                            if new_form not in visited and len(new_form) <= len(string) + 5:
                                visited.add(new_form)
                                new_deriv = derivation + [new_form]
                                queue.append((new_form, new_deriv))
                    pos += 1

        return False, None

    # ------------------ Helpers ------------------
    def _build_linear_tree(self, derivation: List[str]) -> dict:
        return {
            "symbol": self.S,
            "derivation": derivation,
            "type": "linear"
        }

    def generate_strings(self, n: int = 10) -> List[str]:
        strings: List[str] = []
        queue = deque([self.S])
        visited = {self.S}

        max_iter = 10000
        it = 0

        while len(strings) < n and queue and it < max_iter:
            it += 1
            current = queue.popleft()

            is_terminal = all(c in self.T or c == 'ε' for c in current)

            if is_terminal and current not in strings:
                cleaned = current.replace('ε', '')
                if cleaned not in strings:
                    strings.append(cleaned if cleaned else 'ε')
                if len(strings) >= n:
                    break

            for left, rights in self.P.items():
                pos = 0
                while pos <= len(current) - len(left):
                    if current[pos:pos+len(left)] == left:
                        for prod in rights:
                            new_form = current[:pos] + prod + current[pos+len(left):]
                            if new_form not in visited and len(new_form) <= 20:
                                visited.add(new_form)
                                queue.append(new_form)
                    pos += 1

        return sorted(strings, key=len)[:n]

    def visualize_tree(self, tree: Optional[dict], level: int = 0) -> str:
        """Genera una representación textual del árbol de derivación"""
        if not tree:
            return "No hay árbol de derivación"

        if tree.get('type') in ['linear', 'sequential']:
            result = "Derivación paso a paso:\n"
            for i, step in enumerate(tree['derivation'], 1):
                result += f"  {i}. {step}\n"
            return result

        indent = "  " * level
        result = f"{indent}{tree['symbol']}"

        if 'production' in tree:
            result += f" -> {tree['production']}"

        result += "\n"

        if 'children' in tree:
            for child in tree['children']:
                result += self.visualize_tree(child, level + 1)

        return result

    # ------------------ Persistence (methods wrapper) ------------------
    def save(self, filename: str):
        data = {
            "nonterminals": list(self.N),
            "terminals": list(self.T),
            "productions": {k: v for k, v in self.P.items()},
            "start_symbol": self.S,
            "type": self.type
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Gramática guardada en {filename}")

    @staticmethod
    def load(filename: str) -> 'Grammar':
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return Grammar(
            set(data['nonterminals']),
            set(data['terminals']),
            data['productions'],
            data['start_symbol']
        )
