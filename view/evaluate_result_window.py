import tkinter as tk
from tkinter import ttk, scrolledtext


class EvaluateResultWindow:
    def __init__(self, parent, grammar, string):
        self.window = tk.Toplevel(parent)
        self.window.title("Resultado de Evaluación")
        self.window.geometry("650x550")
        self.window.transient(parent)

        self.center_window(self.window, 650, 550)

        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        title = ttk.Label(main_frame, text="EVALUACIÓN DE CADENA",
                          font=('Arial', 12, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10))

        cadena_label = ttk.Label(main_frame,
                                 text=f"Cadena: '{string}'",
                                 font=('Arial', 10))
        cadena_label.grid(row=1, column=0, pady=(0, 10))

        text_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=('Courier', 10),
            bg='#ffffff',
            fg='#000000'
        )
        text_area.grid(row=2, column=0, sticky="nsew")

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
                text_area.insert(tk.END,
                                 "La cadena no pertenece al lenguaje generado por la gramática.\n")
        except Exception as e:
            text_area.insert(tk.END, f"✗ Error durante el análisis: {e}\n")

        text_area.insert(tk.END, "═" * 60)
        text_area.config(state='disabled')

        ttk.Button(main_frame, text="Cerrar", command=self.window.destroy).grid(
            row=3, column=0, pady=(10, 0))

    def center_window(self, window, width, height):
        window.update_idletasks()
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')
