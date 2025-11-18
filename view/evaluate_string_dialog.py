import tkinter as tk
from tkinter import ttk, messagebox


class EvaluateStringDialog:
    def __init__(self, parent):
        self.result = None
        self.top = tk.Toplevel(parent)
        self.top.title("Evaluar Cadena")
        self.top.geometry("400x150")
        self.top.transient(parent)
        self.top.grab_set()

        self.center_window(self.top, 400, 150)

        main_frame = ttk.Frame(self.top, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(main_frame, text="Ingrese la cadena a evaluar:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        ttk.Label(main_frame, text="(Use 'ε' para cadena vacía)",
                  font=('Arial', 8, 'italic')).grid(row=1, column=0, sticky=tk.W)

        self.string_entry = ttk.Entry(main_frame, width=40, font=('Courier', 11))
        self.string_entry.grid(row=2, column=0, sticky="ew", pady=10)
        self.string_entry.focus()

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=10)

        ttk.Button(button_frame, text="Evaluar", command=self.evaluate).grid(
            row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.top.destroy).grid(
            row=0, column=1, padx=5)

        self.string_entry.bind('<Return>', lambda e: self.evaluate())

    def evaluate(self):
        self.result = self.string_entry.get()
        self.top.destroy()

    def center_window(self, window, width, height):
        window.update_idletasks()
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')
