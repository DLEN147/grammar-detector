import tkinter as tk
from tkinter import ttk, scrolledtext


class SyntaxTreeWindow:
    def __init__(self, parent, grammar):
        self.window = tk.Toplevel(parent)
        self.window.title("Árbol de Síntesis")
        self.window.geometry("800x650")
        self.window.transient(parent)

        self.center_window(self.window, 800, 650)

        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Título con más información
        title = ttk.Label(main_frame, text="ÁRBOL DE SÍNTESIS DE LA GRAMÁTICA",
                          font=('Arial', 13, 'bold'))
        title.grid(row=0, column=0, pady=(0, 5))

        # Info adicional
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Label(info_frame, text=f"Tipo: {grammar.get_type_name()}", 
                  font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        ttk.Label(info_frame, text=f"│", 
                  font=('Arial', 9), foreground='gray').pack(side=tk.LEFT)
        ttk.Label(info_frame, text=f"Inicio: {grammar.S}", 
                  font=('Arial', 9, 'bold'), foreground='blue').pack(side=tk.LEFT, padx=5)
        ttk.Label(info_frame, text=f"│", 
                  font=('Arial', 9), foreground='gray').pack(side=tk.LEFT)
        
        # Calcular total de producciones
        total_prods = sum(len(p.rights) for p in grammar.productions)
        ttk.Label(info_frame, text=f"Producciones: {total_prods}", 
                  font=('Arial', 9)).pack(side=tk.LEFT, padx=5)

        # Área de texto con mejor fuente y colores
        text_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.NONE,
            font=('Consolas', 10),
            bg='#f8f9fa',
            fg='#212529',
            padx=10,
            pady=10,
            relief=tk.FLAT,
            borderwidth=2
        )
        text_area.grid(row=2, column=0, sticky="nsew")

        # Configurar tags para colores
        text_area.tag_configure('header', foreground='#0d6efd', font=('Consolas', 10, 'bold'))
        text_area.tag_configure('nonterminal', foreground='#0d6efd', font=('Consolas', 10, 'bold'))
        text_area.tag_configure('terminal', foreground='#198754', font=('Consolas', 10))
        text_area.tag_configure('epsilon', foreground='#6c757d', font=('Consolas', 10, 'italic'))
        text_area.tag_configure('production', foreground='#495057')
        text_area.tag_configure('visited', foreground='#dc3545', font=('Consolas', 10, 'italic'))
        text_area.tag_configure('connector', foreground='#6c757d')

        # Encabezado
        text_area.insert(tk.END, "╔" + "═" * 76 + "╗\n", 'header')
        text_area.insert(tk.END, "║ ", 'header')
        text_area.insert(tk.END, f"{'ESTRUCTURA DE PRODUCCIONES':^74}", 'header')
        text_area.insert(tk.END, " ║\n", 'header')
        text_area.insert(tk.END, "╚" + "═" * 76 + "╝\n\n", 'header')

        # Generar el árbol mejorado
        self._print_syntax_tree(grammar, text_area, grammar.S, "", set(), True)

        text_area.insert(tk.END, "\n\n" + "─" * 78 + "\n", 'connector')
        text_area.insert(tk.END, "Leyenda: ", 'header')
        text_area.insert(tk.END, "No terminal", 'nonterminal')
        text_area.insert(tk.END, " | ", 'connector')
        text_area.insert(tk.END, "terminal", 'terminal')
        text_area.insert(tk.END, " | ", 'connector')
        text_area.insert(tk.END, "ε (vacío)", 'epsilon')
        text_area.insert(tk.END, " | ", 'connector')
        text_area.insert(tk.END, "(ciclo)", 'visited')
        
        text_area.config(state='disabled')

        # Frame de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=(10, 0))
        
        ttk.Button(button_frame, text="Cerrar", command=self.window.destroy).pack()

    def center_window(self, window, width, height):
        window.update_idletasks()
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')

    def _print_syntax_tree(self, grammar, text_area, symbol, prefix, visited, is_root=False):
        """Versión mejorada del árbol con mejor visualización y colores"""
        
        # Detectar ciclos
        if symbol in visited:
            text_area.insert(tk.END, f"{prefix}└─ ", 'connector')
            text_area.insert(tk.END, f"{symbol}", 'nonterminal')
            text_area.insert(tk.END, f" (ya visitado)\n", 'visited')
            return

        # Símbolo terminal
        if symbol not in grammar.symbols.nonterminals:
            text_area.insert(tk.END, f"{prefix}└─ ", 'connector')
            text_area.insert(tk.END, f"'{symbol}'", 'terminal')
            text_area.insert(tk.END, f" (terminal)\n", 'connector')
            return

        # FIX: Marcar como visitado ANTES de continuar
        new_visited = visited.copy()
        new_visited.add(symbol)

        # Buscar producciones de este símbolo
        productions = []
        for prod in grammar.productions:
            if prod.left == symbol:
                productions.extend(prod.rights)
                break

        # Sin producciones
        if not productions:
            text_area.insert(tk.END, f"{prefix}└─ ", 'connector')
            text_area.insert(tk.END, f"{symbol}", 'nonterminal')
            text_area.insert(tk.END, f" (sin producciones)\n", 'visited')
            return
        
        # Símbolo raíz o no terminal
        if is_root:
            text_area.insert(tk.END, "◉ ", 'header')
            text_area.insert(tk.END, f"{symbol}", 'nonterminal')
            text_area.insert(tk.END, f" [inicio]\n", 'connector')
        else:
            text_area.insert(tk.END, f"{prefix}├─ ", 'connector')
            text_area.insert(tk.END, f"{symbol}", 'nonterminal')
            text_area.insert(tk.END, f" ({len(productions)} prod.)\n", 'connector')

        # Procesar cada producción
        for i, prod in enumerate(productions):
            is_last_prod = (i == len(productions) - 1)
            prod_connector = "└─" if is_last_prod else "├─"
            new_prefix = prefix + ("   " if is_last_prod else "│  ")

            # Mostrar la producción
            text_area.insert(tk.END, f"{prefix}│  {prod_connector} ", 'connector')
            text_area.insert(tk.END, f"{symbol} → ", 'production')

            # Producción vacía
            if prod == 'ε':
                text_area.insert(tk.END, f"ε", 'epsilon')
                text_area.insert(tk.END, f" (cadena vacía)\n", 'connector')
                continue

            # Mostrar la producción completa
            for char in prod:
                if char in grammar.symbols.nonterminals:
                    text_area.insert(tk.END, f"{char}", 'nonterminal')
                elif char in grammar.symbols.terminals:
                    text_area.insert(tk.END, f"{char}", 'terminal')
                else:
                    text_area.insert(tk.END, f"{char}", 'production')
            
            text_area.insert(tk.END, "\n")

            # Expandir símbolos no terminales únicos en la producción
            symbols_seen = set()
            nonterminals_in_prod = []
            
            for char in prod:
                if char in grammar.symbols.nonterminals and char not in symbols_seen:
                    symbols_seen.add(char)
                    nonterminals_in_prod.append(char)

            # Expandir cada no terminal
            for j, sym in enumerate(nonterminals_in_prod):
                is_last_sym = (j == len(nonterminals_in_prod) - 1) and is_last_prod
                
                if not is_last_sym:
                    text_area.insert(tk.END, f"{new_prefix}│\n", 'connector')
                
                symbol_prefix = new_prefix + ("   " if is_last_prod else "│  ")
                # FIX: Usar new_visited en lugar de visited.copy()
                self._print_syntax_tree(grammar, text_area, sym, symbol_prefix, new_visited)