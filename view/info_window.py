import tkinter as tk
from tkinter import ttk, scrolledtext


class InfoWindow:
    def __init__(self, parent, grammar):
        self.window = tk.Toplevel(parent)
        self.window.title("Información de la Gramática")
        self.window.geometry("600x500")
        self.window.transient(parent)

        self.center_window(self.window, 600, 500)

        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        title = ttk.Label(main_frame, text="INFORMACIÓN DE LA GRAMÁTICA",
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
        text_area.insert(tk.END, f"Tipo: {grammar.get_type_name()}\n\n")
        text_area.insert(tk.END, f"No terminales (N): {', '.join(sorted(grammar.N))}\n\n")
        text_area.insert(tk.END, f"Terminales (T): {', '.join(sorted(grammar.T))}\n\n")
        text_area.insert(tk.END, f"Símbolo inicial (S): {grammar.S}\n\n")
        text_area.insert(tk.END, "Producciones (P):\n")

        for left, prods in sorted(grammar.P.items()):
            text_area.insert(tk.END, f"  {left} → {' | '.join(prods)}\n")

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
