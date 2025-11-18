import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


class DefineGrammarDialog:
    def __init__(self, parent):
        self.result = None
        self.top = tk.Toplevel(parent)
        self.top.title("Definir Gramática")
        self.top.geometry("700x600")
        self.top.transient(parent)
        self.top.grab_set()

        self.center_window(self.top, 700, 600)

        main_frame = ttk.Frame(self.top, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.top.columnconfigure(0, weight=1)
        self.top.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # --- Campos iniciales ---
        ttk.Label(main_frame, text="No terminales (separados por comas):").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.nonterm_entry = ttk.Entry(main_frame, width=40)
        self.nonterm_entry.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(main_frame, text="Terminales (separados por comas):").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.term_entry = ttk.Entry(main_frame, width=40)
        self.term_entry.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(main_frame, text="Símbolo inicial:").grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.start_entry = ttk.Entry(main_frame, width=40)
        self.start_entry.grid(row=2, column=1, sticky="ew", pady=5)

        # --- Producciones ---
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=15)

        ttk.Label(main_frame, text="PRODUCCIONES",
                  font=('Arial', 10, 'bold')).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        prod_frame = ttk.LabelFrame(main_frame, text="Agregar Producción", padding="10")
        prod_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)
        prod_frame.columnconfigure(1, weight=1)
        prod_frame.columnconfigure(3, weight=1)

        ttk.Label(prod_frame, text="Lado No Terminal:").grid(row=0, column=0, sticky=tk.W)
        self.left_entry = ttk.Entry(prod_frame, width=15)
        self.left_entry.grid(row=0, column=1, sticky="ew", padx=(0, 15))


        ttk.Label(prod_frame, text="Produce:").grid(row=0, column=2, sticky=tk.W)
        self.right_entry = ttk.Entry(prod_frame, width=40)
        self.right_entry.grid(row=0, column=4, sticky="ew")

        ttk.Button(prod_frame, text="Agregar", command=self.add_production).grid(
            row=0, column=5, padx=(10, 0))


        # --- Lista ---
        list_frame = ttk.LabelFrame(main_frame, text="Producciones Definidas", padding="10")
        list_frame.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.prod_display = scrolledtext.ScrolledText(
            list_frame,
            height=12,
            width=60,
            font=('Courier', 10),
            state='disabled'
        )
        self.prod_display.grid(row=0, column=0, sticky="nsew")

        ttk.Button(list_frame, text="Eliminar Última",
                   command=self.remove_last_production).grid(
            row=1, column=0, pady=(5, 0))

        main_frame.rowconfigure(6, weight=1)

        # --- Diccionario ---
        self.productions = {}

        # --- Botones finales ---
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Crear Gramática",
                   command=self.create).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancelar",
                   command=self.top.destroy).grid(row=0, column=1, padx=5)

        # Bindings
        self.left_entry.bind('<Return>', lambda e: self.right_entry.focus())
        self.right_entry.bind('<Return>', lambda e: self.add_production())

        self.left_entry.focus()

    # ========================= MÉTODOS ===========================

    def add_production(self):
        left = self.left_entry.get().strip()
        right = self.right_entry.get().strip()

        if not left:
            messagebox.showwarning("Advertencia", "Debe ingresar el lado izquierdo")
            return

        if right.strip() == "":
            right = 'ε' # Producción vacía 
        else:
            right = right.strip()

        if left in self.productions:
            if right not in self.productions[left]:
                self.productions[left].append(right)
        else:
            self.productions[left] = [right]

        self.update_production_display()

        self.right_entry.delete(0, tk.END)
        self.right_entry.focus()

    def remove_last_production(self):
        if not self.productions:
            return

        last_key = list(self.productions.keys())[-1]

        if len(self.productions[last_key]) > 1:
            self.productions[last_key].pop()
        else:
            del self.productions[last_key]

        self.update_production_display()

    def update_production_display(self):
        self.prod_display.config(state='normal')
        self.prod_display.delete(1.0, tk.END)

        if not self.productions:
            self.prod_display.insert(1.0, "(No hay producciones definidas)")
        else:
            for left, rights in self.productions.items():
                self.prod_display.insert(tk.END, f"{left} → {' | '.join(rights)}\n")

        self.prod_display.config(state='disabled')

    def create(self):
        try:
            nonterminals = set(
                x.strip() for x in self.nonterm_entry.get().split(',') if x.strip()
            )
            terminals = set(
                x.strip() for x in self.term_entry.get().split(',') if x.strip()
            )
            start_symbol = self.start_entry.get().strip()

            if not nonterminals:
                messagebox.showerror("Error", "Debe definir al menos un no terminal")
                return

            if not terminals:
                messagebox.showerror("Error", "Debe definir al menos un terminal")
                return

            if start_symbol not in nonterminals:
                messagebox.showerror("Error",
                                     "El símbolo inicial debe estar en los no terminales")
                return

            if not self.productions:
                messagebox.showerror("Error", "Debe definir al menos una producción")
                return

            self.result = {
                'nonterminals': nonterminals,
                'terminals': terminals,
                'productions': self.productions,
                'start_symbol': start_symbol
            }

            self.top.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la gramática: {e}")

    def center_window(self, window, width, height):
        window.update_idletasks()
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')
