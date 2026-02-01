import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Python Calculator")
        self.root.geometry("600x500")
        self.root.configure(bg="#333")

        # Colors
        self.colors = {
            "bg": "#333",
            "display_bg": "#fff",
            "btn_default": "#eee",
            "btn_operator": "#ff9500",
            "btn_equal": "#4CAF50",
            "btn_clear": "#f44336",
            "text_dark": "#333",
            "text_light": "#fff"
        }

        # Main Layout
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Display
        self.display = tk.Entry(root, font=("Arial", 28), borderwidth=0, relief="flat", justify="right", bg=self.colors["display_bg"], fg=self.colors["text_dark"])
        self.display.grid(row=0, column=0, columnspan=2, padx=10, pady=20, sticky="nsew")
        self.display.bind("<Return>", lambda e: self.calculate())

        # Buttons Frame
        self.btn_frame = tk.Frame(root, bg=self.colors["bg"])
        self.btn_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # History Frame
        self.history_frame = tk.Frame(root, bg="#444", padx=10, pady=10)
        self.history_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        tk.Label(self.history_frame, text="History", font=("Arial", 14, "bold"), bg="#444", fg="#fff").pack()
        
        self.history_list = tk.Listbox(self.history_frame, font=("Arial", 10), bg="#444", fg="#fff", borderwidth=0, highlightthickness=0)
        self.history_list.pack(fill="both", expand=True, pady=5)
        self.history_list.bind("<Double-Button-1>", self.reuse_history)

        self.clear_hist_btn = tk.Button(self.history_frame, text="Clear All", command=self.clear_history, bg=self.colors["btn_clear"], fg="#fff", relief="flat")
        self.clear_hist_btn.pack(fill="x")

        self.create_buttons()
        self.setup_keyboard()

    def create_buttons(self):
        buttons = [
            ('C', self.colors["btn_clear"]), ('⌫', self.colors["btn_clear"]), ('sqrt', self.colors["btn_operator"]), ('/', self.colors["btn_operator"]),
            ('7', self.colors["btn_default"]), ('8', self.colors["btn_default"]), ('9', self.colors["btn_default"]), ('*', self.colors["btn_operator"]),
            ('4', self.colors["btn_default"]), ('5', self.colors["btn_default"]), ('6', self.colors["btn_default"]), ('-', self.colors["btn_operator"]),
            ('1', self.colors["btn_default"]), ('2', self.colors["btn_default"]), ('3', self.colors["btn_default"]), ('+', self.colors["btn_operator"]),
            ('0', self.colors["btn_default"]), ('.', self.colors["btn_default"]), ('^', self.colors["btn_operator"]), ('=', self.colors["btn_equal"])
        ]

        for i in range(5):
            self.btn_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.btn_frame.grid_columnconfigure(i, weight=1)

        row, col = 0, 0
        for text, color in buttons:
            cmd = lambda t=text: self.handle_button(t)
            btn = tk.Button(self.btn_frame, text=text, font=("Arial", 14, "bold"), bg=color, 
                          fg=self.colors["text_dark"] if color == self.colors["btn_default"] else "#fff",
                          relief="flat", command=cmd)
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def handle_button(self, text):
        if text == '=': self.calculate()
        elif text == 'C': self.clear_display()
        elif text == '⌫': self.backspace()
        elif text == 'sqrt': self.append_to_display('math.sqrt(')
        elif text == '^': self.append_to_display('**')
        else: self.append_to_display(text)

    def setup_keyboard(self):
        self.root.bind("<Key>", self.key_press)

    def key_press(self, event):
        key = event.char
        if key.isdigit() or key in "+-*/.":
            self.append_to_display(key)
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym == "Escape":
            self.clear_display()
        elif event.keysym == "Return":
            self.calculate()

    def append_to_display(self, value):
        self.display.insert(tk.END, value)

    def calculate(self):
        try:
            expr = self.display.get()
            # Basic security check for eval
            safe_expr = expr.replace('^', '**')
            result = eval(safe_expr, {"math": math, "__builtins__": {}})
            
            self.history_list.insert(tk.END, f"{expr} = {result}")
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero")
        except Exception:
            messagebox.showerror("Error", "Invalid Expression")

    def reuse_history(self, event):
        selection = self.history_list.curselection()
        if selection:
            item = self.history_list.get(selection[0])
            result = item.split('=')[-1].strip()
            self.display.delete(0, tk.END)
            self.display.insert(0, result)

    def clear_display(self):
        self.display.delete(0, tk.END)

    def backspace(self):
        current = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(0, current[:-1])

    def clear_history(self):
        self.history_list.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
