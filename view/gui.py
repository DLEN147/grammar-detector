# view/gui.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from models.grammar import Grammar
from data.serializer import save_grammar, load_grammar
from typing import Optional

class GrammarAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Universal de Gramáticas Formales")
        self.root.geometry("400x450")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)
        
        self.grammar: Optional[Grammar] = None
        
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), background='#f0f0f0')
        style.configure('Info.TLabel', font=('Arial', 9), background='#f0f0f0')
        style.configure('TButton', font=('Arial', 10), padding=10)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, 
                                text="ANALIZADOR DE\nGRAMÁTICAS FORMALES", 
                                style='Title.TLabel',
                                justify='center')
        title_label.grid(row=0, column=0, pady=(0, 15))
        
        # Label de estado de gramática
        self.status_label = ttk.Label(main_frame, 
                                      text="No hay gramática cargada", 
                                      style='Info.TLabel', 
                                      foreground='red',
                                      justify='center')
        self.status_label.grid(row=1, column=0, pady=(0, 20))
        
        # Botones principales
        buttons = [
            ("📝 Definir Nueva Gramática", self.define_grammar),
            ("📂 Cargar Gramática", self.load_grammar_file),
            ("💾 Guardar Gramática", self.save_grammar_file),
            ("ℹ️  Mostrar Información", self.show_grammar_info),
            ("🌳 Árbol de Síntesis", self.show_syntax_tree),
            ("✓ Evaluar Cadena", self.evaluate_string),
            ("🔤 Generar Cadenas", self.generate_strings),
        ]
        
        for i, (text, command) in enumerate(buttons, start=2):
            btn = ttk.Button(main_frame, text=text, command=command, width=30)
            btn.grid(row=i, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # Centrar contenido
        main_frame.grid_columnconfigure(0, weight=1)
    
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


class InfoWindow:
    def __init__(self, parent, grammar):
        self.window = tk.Toplevel(parent)
        self.window.title("Información de la Gramática")
        self.window.geometry("600x500")
        self.window.transient(parent)
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        title = ttk.Label(main_frame, text="INFORMACIÓN DE LA GRAMÁTICA", 
                         font=('Arial', 12, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10))
        
        # Área de texto
        text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                              font=('Courier', 10),
                                              bg='#ffffff', fg='#000000')
        text_area.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Contenido
        text_area.insert(tk.END, "═" * 60 + "\n")
        text_area.insert(tk.END, f"Tipo: {grammar.get_type_name()}\n\n")
        text_area.insert(tk.END, f"No terminales (N): {', '.join(sorted(grammar.N))}\n\n")
        text_area.insert(tk.END, f"Terminales (T): {', '.join(sorted(grammar.T))}\n\n")
        text_area.insert(tk.END, f"Símbolo inicial (S): {grammar.S}\n\n")
        text_area.insert(tk.END, "Producciones (P):\n")
        for left, prods in sorted(grammar.P.items()):
            text_area.insert(tk.END, f"  {left} → {' | '.join(prods)}\n")
        text_area.insert(tk.END, "\n" + "═" * 60)
        
        text_area.config(state='disabled')
        
        # Botón cerrar
        ttk.Button(main_frame, text="Cerrar", command=self.window.destroy).grid(
            row=2, column=0, pady=(10, 0))


class SyntaxTreeWindow:
    def __init__(self, parent, grammar):
        self.window = tk.Toplevel(parent)
        self.window.title("Árbol de Síntesis")
        self.window.geometry("700x600")
        self.window.transient(parent)
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        title = ttk.Label(main_frame, text="ÁRBOL DE SÍNTESIS DE LA GRAMÁTICA", 
                         font=('Arial', 12, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10))
        
        # Área de texto
        text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                              font=('Courier', 9),
                                              bg='#ffffff', fg='#000000')
        text_area.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Contenido
        text_area.insert(tk.END, "═" * 70 + "\n")
        text_area.insert(tk.END, f"Gramática: {grammar.get_type_name()}\n")
        text_area.insert(tk.END, f"Símbolo inicial: {grammar.S}\n\n")
        text_area.insert(tk.END, "Estructura de producciones:\n\n")
        
        # Generar árbol
        self._print_syntax_tree(grammar, text_area, grammar.S, "", set())
        
        text_area.insert(tk.END, "\n" + "═" * 70)
        text_area.config(state='disabled')
        
        # Botón cerrar
        ttk.Button(main_frame, text="Cerrar", command=self.window.destroy).grid(
            row=2, column=0, pady=(10, 0))
    
    def _print_syntax_tree(self, grammar, text_area, symbol, prefix, visited):
        """Imprime recursivamente el árbol de síntesis de la gramática"""
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
                
                # Analizar símbolos en la producción
                symbols_in_prod = []
                for char in prod:
                    if char in grammar.N or char in grammar.T:
                        if char not in symbols_in_prod:
                            symbols_in_prod.append(char)
                
                # Expandir símbolos no terminales recursivamente
                for j, sym in enumerate(symbols_in_prod):
                    if sym in grammar.N:
                        symbol_prefix = new_prefix + ("   " if is_last else "│  ")
                        text_area.insert(tk.END, f"{symbol_prefix}│\n")
                        self._print_syntax_tree(grammar, text_area, sym, symbol_prefix, visited.copy())


class EvaluateResultWindow:
    def __init__(self, parent, grammar, string):
        self.window = tk.Toplevel(parent)
        self.window.title("Resultado de Evaluación")
        self.window.geometry("650x550")
        self.window.transient(parent)
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        title = ttk.Label(main_frame, text="EVALUACIÓN DE CADENA", 
                         font=('Arial', 12, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10))
        
        # Cadena evaluada
        cadena_label = ttk.Label(main_frame, 
                                text=f"Cadena: '{string}'", 
                                font=('Arial', 10))
        cadena_label.grid(row=1, column=0, pady=(0, 10))
        
        # Área de texto
        text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                              font=('Courier', 10),
                                              bg='#ffffff', fg='#000000')
        text_area.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Evaluar
        text_area.insert(tk.END, "═" * 60 + "\n")
        text_area.insert(tk.END, "Analizando...\n\n")
        
        try:
            accepted, tree = grammar.parse(string)
            
            if accepted:
                text_area.insert(tk.END, "✓ CADENA ACEPTADA\n\n")
                text_area.insert(tk.END, "Árbol de derivación:\n")
                text_area.insert(tk.END, "-" * 60 + "\n")
                text_area.insert(tk.END, grammar.visualize_tree(tree))
            else:
                text_area.insert(tk.END, "✗ CADENA RECHAZADA\n\n")
                text_area.insert(tk.END, "La cadena no pertenece al lenguaje generado por la gramática.\n")
        except Exception as e:
            text_area.insert(tk.END, f"✗ Error durante el análisis: {e}\n")
        
        text_area.insert(tk.END, "═" * 60)
        text_area.config(state='disabled')
        
        # Botón cerrar
        ttk.Button(main_frame, text="Cerrar", command=self.window.destroy).grid(
            row=3, column=0, pady=(10, 0))


class GenerateResultWindow:
    def __init__(self, parent, grammar, n):
        self.window = tk.Toplevel(parent)
        self.window.title("Cadenas Generadas")
        self.window.geometry("550x500")
        self.window.transient(parent)
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        title = ttk.Label(main_frame, text=f"GENERACIÓN DE {n} CADENAS MÁS CORTAS", 
                         font=('Arial', 12, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10))
        
        # Área de texto
        text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                              font=('Courier', 10),
                                              bg='#ffffff', fg='#000000')
        text_area.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Generar cadenas
        text_area.insert(tk.END, "═" * 60 + "\n")
        text_area.insert(tk.END, f"Generando las {n} cadenas más cortas del lenguaje...\n\n")
        
        try:
            strings = grammar.generate_strings(n)
            text_area.insert(tk.END, f"Cadenas generadas ({len(strings)}):\n\n")
            for i, s in enumerate(strings, 1):
                length = len(s) if s != 'ε' else 0
                text_area.insert(tk.END, f"  {i:2d}. '{s}' (longitud: {length})\n")
        except Exception as e:
            text_area.insert(tk.END, f"✗ Error al generar cadenas: {e}\n")
        
        text_area.insert(tk.END, "\n" + "═" * 60)
        text_area.config(state='disabled')
        
        # Botón cerrar
        ttk.Button(main_frame, text="Cerrar", command=self.window.destroy).grid(
            row=2, column=0, pady=(10, 0))


class DefineGrammarDialog:
    def __init__(self, parent):
        self.result = None
        self.top = tk.Toplevel(parent)
        self.top.title("Definir Gramática")
        self.top.geometry("700x600")
        self.top.transient(parent)
        self.top.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(self.top, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.top.columnconfigure(0, weight=1)
        self.top.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # No terminales
        ttk.Label(main_frame, text="No terminales (separados por comas):").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.nonterm_entry = ttk.Entry(main_frame, width=40)
        self.nonterm_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        self.nonterm_entry.insert(0, "S,A,B")
        
        # Terminales
        ttk.Label(main_frame, text="Terminales (separados por comas):").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.term_entry = ttk.Entry(main_frame, width=40)
        self.term_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        self.term_entry.insert(0, "a,b")
        
        # Símbolo inicial
        ttk.Label(main_frame, text="Símbolo inicial:").grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.start_entry = ttk.Entry(main_frame, width=40)
        self.start_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        self.start_entry.insert(0, "S")
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        # Sección de producciones
        ttk.Label(main_frame, text="PRODUCCIONES", font=('Arial', 10, 'bold')).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Frame para agregar producciones
        prod_frame = ttk.LabelFrame(main_frame, text="Agregar Producción", padding="10")
        prod_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        prod_frame.columnconfigure(1, weight=1)
        prod_frame.columnconfigure(3, weight=1)
        
        ttk.Label(prod_frame, text="Lado izquierdo:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.left_entry = ttk.Entry(prod_frame, width=15)
        self.left_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 15))
        
        ttk.Label(prod_frame, text="→").grid(row=0, column=2, padx=5)
        
        ttk.Label(prod_frame, text="Lado derecho:").grid(row=0, column=3, sticky=tk.W, padx=(15, 5))
        self.right_entry = ttk.Entry(prod_frame, width=20)
        self.right_entry.grid(row=0, column=4, sticky=(tk.W, tk.E))
        
        ttk.Button(prod_frame, text="Agregar", command=self.add_production).grid(
            row=0, column=5, padx=(10, 0))
        
        info_label = ttk.Label(prod_frame, 
                               text="Usa 'ε' para producción vacía. Ejemplo: S → aSb",
                               font=('Arial', 8, 'italic'))
        info_label.grid(row=1, column=0, columnspan=6, sticky=tk.W, pady=(5, 0))
        
        # Lista de producciones agregadas
        list_frame = ttk.LabelFrame(main_frame, text="Producciones Definidas", padding="10")
        list_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Scrolled text para mostrar producciones
        self.prod_display = scrolledtext.ScrolledText(list_frame, height=12, width=60,
                                                       font=('Courier', 10), state='disabled')
        self.prod_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botón para eliminar última producción
        ttk.Button(list_frame, text="Eliminar Última", command=self.remove_last_production).grid(
            row=1, column=0, pady=(5, 0))
        
        main_frame.rowconfigure(6, weight=1)
        
        # Diccionario para almacenar producciones
        self.productions = {}
        
        # Botones finales
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Crear Gramática", command=self.create).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.top.destroy).grid(row=0, column=1, padx=5)
        
        # Bindings
        self.left_entry.bind('<Return>', lambda e: self.right_entry.focus())
        self.right_entry.bind('<Return>', lambda e: self.add_production())
        
        self.left_entry.focus()
    
    def add_production(self):
        left = self.left_entry.get().strip()
        right = self.right_entry.get().strip()
        
        if not left:
            messagebox.showwarning("Advertencia", "Debe ingresar el lado izquierdo")
            return
        
        if not right:
            messagebox.showwarning("Advertencia", "Debe ingresar el lado derecho")
            return
        
        # Agregar producción al diccionario
        if left in self.productions:
            if right not in self.productions[left]:
                self.productions[left].append(right)
        else:
            self.productions[left] = [right]
        
        # Actualizar display
        self.update_production_display()
        
        # Limpiar campos
        self.right_entry.delete(0, tk.END)
        self.right_entry.focus()
    
    def remove_last_production(self):
        if not self.productions:
            return
        
        # Obtener la última clave
        last_key = list(self.productions.keys())[-1]
        
        # Eliminar la última producción de esa clave
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
                prod_str = f"{left} → {' | '.join(rights)}\n"
                self.prod_display.insert(tk.END, prod_str)
        
        self.prod_display.config(state='disabled')
    
    def create(self):
        try:
            # Procesar no terminales
            nonterminals = set(x.strip() for x in self.nonterm_entry.get().split(',') if x.strip())
            
            # Procesar terminales
            terminals = set(x.strip() for x in self.term_entry.get().split(',') if x.strip())
            
            # Símbolo inicial
            start_symbol = self.start_entry.get().strip()
            
            if not nonterminals:
                messagebox.showerror("Error", "Debe definir al menos un no terminal")
                return
            
            if not terminals:
                messagebox.showerror("Error", "Debe definir al menos un terminal")
                return
            
            if start_symbol not in nonterminals:
                messagebox.showerror("Error", "El símbolo inicial debe estar en los no terminales")
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


class EvaluateStringDialog:
    def __init__(self, parent):
        self.result = None
        self.top = tk.Toplevel(parent)
        self.top.title("Evaluar Cadena")
        self.top.geometry("400x150")
        self.top.transient(parent)
        self.top.grab_set()
        
        main_frame = ttk.Frame(self.top, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Ingrese la cadena a evaluar:").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(main_frame, text="(Use 'ε' para cadena vacía)",
                  font=('Arial', 8, 'italic')).grid(row=1, column=0, sticky=tk.W)
        
        self.string_entry = ttk.Entry(main_frame, width=40, font=('Courier', 11))
        self.string_entry.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        self.string_entry.focus()
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=10)
        
        ttk.Button(button_frame, text="Evaluar", command=self.evaluate).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.top.destroy).grid(row=0, column=1, padx=5)
        
        self.string_entry.bind('<Return>', lambda e: self.evaluate())
    
    def evaluate(self):
        self.result = self.string_entry.get()
        self.top.destroy()


class GenerateStringsDialog:
    def __init__(self, parent):
        self.result = None
        self.top = tk.Toplevel(parent)
        self.top.title("Generar Cadenas")
        self.top.geometry("350x150")
        self.top.transient(parent)
        self.top.grab_set()
        
        main_frame = ttk.Frame(self.top, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="¿Cuántas cadenas generar?").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        
        self.n_entry = ttk.Entry(main_frame, width=20)
        self.n_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        self.n_entry.insert(0, "10")
        self.n_entry.focus()
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10)
        
        ttk.Button(button_frame, text="Generar", command=self.generate).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.top.destroy).grid(row=0, column=1, padx=5)
        
        self.n_entry.bind('<Return>', lambda e: self.generate())
    
    def generate(self):
        try:
            n = int(self.n_entry.get())
            if n <= 0:
                raise ValueError("Debe ser un número positivo")
            self.result = n
            self.top.destroy()
        except ValueError as e:
            messagebox.showerror("Error", f"Número inválido: {e}")


def run_gui():
    root = tk.Tk()
    app = GrammarAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()