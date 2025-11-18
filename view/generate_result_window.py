import tkinter as tk
from tkinter import ttk, scrolledtext


class GenerateResultWindow:
    def __init__(self, parent, grammar, n):
        self.window = tk.Toplevel(parent)
        self.window.title("Cadenas Generadas")
        self.window.geometry("550x500")
        self.window.transient(parent)

        self.center_window(self.window, 550, 500)

        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        title = ttk.Label(main_frame, text=f"GENERACIÓN DE {n} CADENAS MÁS CORTAS",
                          font=('Arial', 12, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10))

        text_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=('Courier', 10),
            bg='#ffffff',
            fg='#000000'
        )
        text_area.grid(row=1, column=0, sticky="nsew")

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

        ttk.Button(main_frame, text="Cerrar", command=self.window.destroy).grid(
            row=2, column=0, pady=(10, 0))

    def center_window(self, window, width, height):
        window.update_idletasks()
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')
