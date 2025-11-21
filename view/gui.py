import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from models.grammar import Grammar
from data.serializer import save_grammar, load_grammar

from view.info_window import InfoWindow
from view.syntax_tree_window import SyntaxTreeWindow
from view.evaluate_result_window import EvaluateResultWindow
from view.generate_result_window import GenerateResultWindow
from view.define_grammar_dialog import DefineGrammarDialog
from view.evaluate_string_dialog import EvaluateStringDialog
from view.generate_strings_dialog import GenerateStringsDialog

from typing import Optional


class GrammarAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Gramáticas Formales")
        self.root.geometry("400x550")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)

        self.center_window(self.root, 400, 550)
        self.grammar: Optional[Grammar] = None

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), background='#f0f0f0')
        style.configure('Info.TLabel', font=('Arial', 9), background='#f0f0f0')
        style.configure('TButton', font=('Arial', 10), padding=10)

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        title_label = ttk.Label(
            main_frame,
            text="ANALIZADOR DE\nGRAMÁTICAS FORMALES",
            style='Title.TLabel',
            justify='center'
        )
        title_label.grid(row=0, column=0, pady=(0, 15))

        self.status_label = ttk.Label(
            main_frame,
            text="No hay gramática cargada",
            style='Info.TLabel',
            foreground='red',
            justify='center'
        )
        self.status_label.grid(row=1, column=0, pady=(0, 20))

        buttons = [
            ("Definir Nueva Gramática", self.define_grammar),
            ("Cargar Gramática", self.load_grammar_file),
            ("Guardar Gramática", self.save_grammar_file),
            ("Mostrar Información", self.show_grammar_info),
            ("Árbol de Síntesis", self.show_syntax_tree),
            ("Evaluar Cadena", self.evaluate_string),
            ("Generar Cadenas", self.generate_strings),
        ]

        for i, (text, command) in enumerate(buttons, start=2):
            ttk.Button(main_frame, text=text, command=command, width=30).grid(
                row=i, column=0, pady=5, sticky="ew"
            )

        main_frame.grid_columnconfigure(0, weight=1)

    def center_window(self, window, width, height):
        window.update_idletasks()
        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')

    def update_status(self):
        if self.grammar:
            self.status_label.config(
                text=f"✓ {self.grammar.get_type_name()}",
                foreground='green'
            )
        else:
            self.status_label.config(
                text="No hay gramática cargada",
                foreground='red'
            )

    def define_grammar(self):
        dialog = DefineGrammarDialog(self.root)
        self.root.wait_window(dialog.top)
        if dialog.result:
            try:
                self.grammar = Grammar(
                    dialog.result['nonterminals'],
                    dialog.result['terminals'],
                    dialog.result['productions'],
                    dialog.result['start_symbol']
                )
                self.update_status()
                messagebox.showinfo("Éxito",
                                    f"Gramática creada exitosamente\n\n{self.grammar.get_type_name()}")
            except ValueError as e:
                # Mostrar errores de validación de manera amigable
                messagebox.showerror("Error de Validación", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear gramática: {e}")

    def load_grammar_file(self):
        filename = filedialog.askopenfilename(
            title="Cargar Gramática",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.grammar = load_grammar(filename)
                self.update_status()
                messagebox.showinfo("Éxito",
                                    f"Gramática cargada exitosamente\n\n{self.grammar.get_type_name()}")
            except ValueError as e:
                messagebox.showerror("Error de Validación", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar: {e}")

    def save_grammar_file(self):
        if not self.grammar:
            messagebox.showwarning("Advertencia", "Primero debe definir o cargar una gramática")
            return

        filename = filedialog.asksaveasfilename(
            title="Guardar Gramática",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                save_grammar(self.grammar, filename)
                messagebox.showinfo("Éxito", f"Gramática guardada en:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {e}")

    def show_grammar_info(self):
        if not self.grammar:
            messagebox.showwarning("Advertencia", "Primero debe definir o cargar una gramática")
            return
        InfoWindow(self.root, self.grammar)

    def show_syntax_tree(self):
        if not self.grammar:
            messagebox.showwarning("Advertencia", "Primero debe definir o cargar una gramática")
            return
        SyntaxTreeWindow(self.root, self.grammar)

    def evaluate_string(self):
        if not self.grammar:
            messagebox.showwarning("Advertencia", "Primero debe definir o cargar una gramática")
            return

        dialog = EvaluateStringDialog(self.root)
        self.root.wait_window(dialog.top)

        if dialog.result is not None:
            EvaluateResultWindow(self.root, self.grammar, dialog.result)

    def generate_strings(self):
        if not self.grammar:
            messagebox.showwarning("Advertencia", "Primero debe definir o cargar una gramática")
            return

        dialog = GenerateStringsDialog(self.root)
        self.root.wait_window(dialog.top)

        if dialog.result:
            GenerateResultWindow(self.root, self.grammar, dialog.result)


def run_gui():
    root = tk.Tk()
    app = GrammarAnalyzerGUI(root)

    root.mainloop()
