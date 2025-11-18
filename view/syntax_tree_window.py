import tkinter as tk
from tkinter import ttk, scrolledtext


class SyntaxTreeWindow:
    def __init__(self, parent, grammar):
        self.window = tk.Toplevel(parent)
        self.window.title("Árbol de Síntesis")
        self.window.geometry("700x600")
        self.window.transient(parent)

        self.center_window(self.window, 700, 600)

        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        title = ttk.Label(main_frame, text="ÁRBOL DE SÍNTESIS DE LA GRAMÁTICA",
                          font=('Arial', 12, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10))

        text_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=('Courier', 9),
            bg='#ffffff',
            fg='#000000'
        )
        text_area.grid(row=1, column=0, sticky="nsew")

        text_area.insert(tk.END, "═" * 70 + "\n")
        text_area.insert(tk.END, f"Gramática: {grammar.get_type_name()}\n")
        text_area.insert(tk.END, f"Símbolo inicial: {grammar.S}\n\n")
        text_area.insert(tk.END, "Estructura de producciones:\n\n")

        self._print_syntax_tree(grammar, text_area, grammar.S, "", set())

        text_area.insert(tk.END, "\n" + "═" * 70)
        text_area.config(state='disabled')

        ttk.Button(main_frame, text="Cerrar", command=self.window.destroy).grid(
            row=2, column=0, pady=(10, 0))

    def center_window(self, window, width, height):
        window.update_idletasks()
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')

    def _print_syntax_tree(self, grammar, text_area, symbol, prefix, visited):
        if symbol in visited:
            text_area.insert(tk.END, f"{prefix}├─ {symbol} (ya visitado)\n")
            return

        if symbol not in grammar.N:
            text_area.insert(tk.END, f"{prefix}└─ {symbol} (terminal)\n")
            return

        visited.add(symbol)

        if symbol not in grammar.P:
            text_area.insert(tk.END, f"{prefix}└─ {symbol} (sin producciones)\n")
            return

        productions = grammar.P[symbol]
        text_area.insert(tk.END, f"{prefix}├─ {symbol}\n")

        for i, prod in enumerate(productions):
            is_last = (i == len(productions) - 1)
            connector = "└─" if is_last else "├─"
            new_prefix = prefix + ("   " if is_last else "│  ")

            if prod == 'ε':
                text_area.insert(tk.END, f"{prefix}│  {connector} ε (vacío)\n")
            else:
                text_area.insert(tk.END, f"{prefix}│  {connector} {prod}\n")

                symbols = []
                for char in prod:
                    if char in grammar.N or char in grammar.T:
                        if char not in symbols:
                            symbols.append(char)

                for j, sym in enumerate(symbols):
                    if sym in grammar.N:
                        symbol_prefix = new_prefix + ("   " if is_last else "│  ")
                        text_area.insert(tk.END, f"{symbol_prefix}│\n")
                        self._print_syntax_tree(grammar, text_area, sym, symbol_prefix, visited.copy())
