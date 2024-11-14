import tkinter as tk
from tkinter import messagebox
import math

class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.geometry("350x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Campo de exibição
        self.display = tk.Entry(root, font=("Arial", 24), borderwidth=0, relief="solid", justify="right", bg="#f9f9f9")
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=20)
        self.display.bind("<Key>", lambda e: "break")  # Previne entrada direta pelo teclado

        # Configuração do grid para botões
        root.grid_rowconfigure(0, weight=1)
        for i in range(1, 7):
            root.grid_rowconfigure(i, weight=1)
            root.grid_columnconfigure(i % 4, weight=1)

        # Lista de botões e suas posições
        buttons = [
            ("C", self.clear_display), ("DEL", self.delete_last), ("(", lambda: self.append_to_display("(")), (")", lambda: self.append_to_display(")")),
            ("7", lambda: self.append_to_display("7")), ("8", lambda: self.append_to_display("8")), ("9", lambda: self.append_to_display("9")), ("/", lambda: self.append_to_display("/")),
            ("4", lambda: self.append_to_display("4")), ("5", lambda: self.append_to_display("5")), ("6", lambda: self.append_to_display("6")), ("*", lambda: self.append_to_display("*")),
            ("1", lambda: self.append_to_display("1")), ("2", lambda: self.append_to_display("2")), ("3", lambda: self.append_to_display("3")), ("-", lambda: self.append_to_display("-")),
            ("0", lambda: self.append_to_display("0")), (".", lambda: self.append_to_display(".")), ("+", lambda: self.append_to_display("+")), ("=", self.calculate),
            ("EXP", lambda: self.append_to_display("**")), ("SQR", self.calculate_sqrt), ("%", lambda: self.append_to_display("/100")), ("!", self.calculate_factorial),
            ("sin", lambda: self.calculate_trig("sin")), ("cos", lambda: self.calculate_trig("cos")), ("tan", lambda: self.calculate_trig("tan")), (",", self.add_thousand_separator)
        ]

        # Adiciona botões à interface
        for idx, (text, command) in enumerate(buttons):
            row, col = divmod(idx, 4)
            btn = tk.Button(root, text=text, font=("Arial", 16), bg="#e0e0e0", activebackground="#d0d0d0", command=command)
            btn.grid(row=row + 1, column=col, sticky="nsew", padx=5, pady=5)

    def get_display(self):
        return self.display.get()

    def set_display(self, value):
        formatted_value = "{:,.12f}".format(value).rstrip("0").rstrip(".")  # Formata com separador de milhares e remove zeros finais
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, formatted_value)



    def clear_display(self):
        self.display.delete(0, tk.END)

    def delete_last(self):
        current_text = self.get_display()
        self.display.delete(len(current_text) - 1, tk.END)
        self.add_thousand_separator()

    def append_to_display(self, value):
        self.display.insert(tk.END, value)
        self.add_thousand_separator()

    def calculate(self):
        expression = self.get_display().replace(",", "")
        try:
            result = eval(expression)
            self.set_display(result)
        except Exception:
            messagebox.showerror("Erro", "Expressão inválida")

    def calculate_sqrt(self):
        try:
            result = math.sqrt(float(self.get_display().replace(",", "")))
            self.set_display(result)
        except Exception:
            messagebox.showerror("Erro", "Valor inválido para raiz quadrada")

    def calculate_factorial(self):
        try:
            value = int(self.get_display().replace(",", ""))
            if value < 0:
                raise ValueError
            result = math.factorial(value)
            self.set_display(result)
        except ValueError:
            messagebox.showerror("Erro", "Somente inteiros não-negativos são válidos")

    def calculate_trig(self, func):
        try:
            value = math.radians(float(self.get_display().replace(",", "")))
            result = getattr(math, func)(value)
            self.set_display(result)
        except Exception:
            messagebox.showerror("Erro", f"Valor inválido para {func}")

    def add_thousand_separator(self):
        current_text = self.get_display().replace(",", "")
        if "." in current_text:
            integer_part, decimal_part = current_text.split(".")
            integer_part = "{:,}".format(int(integer_part))
            formatted_value = f"{integer_part}.{decimal_part}"
        else:
            formatted_value = "{:,}".format(int(current_text)) if current_text else ""
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, formatted_value)

# Inicializa a janela principal
root = tk.Tk()
app = Calculadora(root)
root.mainloop()
