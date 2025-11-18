import tkinter as tk
from tkinter import ttk, messagebox


class GenerateStringsDialog:
    def __init__(self, parent):
        self.result = None
        self.top = tk.Toplevel(parent)
        self.top.title("Generar Cadenas")
        self.top.geometry("350x150")
        self.top.transient(parent)
        self.top.grab_set()

        self.center_window(self.top, 350, 150)

        main_frame = ttk.Frame(self.top, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(main_frame, text="¿Cuántas cadenas generar?").grid(
            row=0, column=0, sticky=tk.W, pady=5)

        self.n_entry = ttk.Entry(main_frame, width=20)
        self.n_entry.grid(row=1, column=0, sticky="ew", pady=10)
        self.n_entry.insert(0, "10")
        self.n_entry.focus()

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10)

        ttk.Button(button_frame, text="Generar", command=self.generate).grid(
            row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.top.destroy).grid(
            row=0, column=1, padx=5)

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

    def center_window(self, window, width, height):
        window.update_idletasks()
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')
