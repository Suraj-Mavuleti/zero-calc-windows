import customtkinter as ctk
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ZeroCalc(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Zero Scientific Calc - V8 Native GUI")
        self.geometry("450x600")
        
        self.result_var = ctk.StringVar(value="0")
        
        display = ctk.CTkEntry(self, textvariable=self.result_var, font=("Arial", 36), justify="right", state="readonly")
        display.pack(fill=ctk.BOTH, ipadx=8, ipady=20, pady=20, padx=20)
        
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        buttons = [
            ('sin', 'cos', 'tan', 'C', 'DEL'),
            ('log', 'sqrt', '(', ')', '^'),
            ('7', '8', '9', '/', '*'),
            ('4', '5', '6', '-', '+'),
            ('1', '2', '3', '0', '.')
        ]
        
        for row_idx, row in enumerate(buttons):
            buttons_frame.rowconfigure(row_idx, weight=1)
            for col_idx, text in enumerate(row):
                buttons_frame.columnconfigure(col_idx, weight=1)
                
                fg_color = "#4C566A"
                hover_color = "#5E81AC"
                if text in ['/', '*', '-', '+', '^']:
                    fg_color = "#5E81AC"
                    hover_color = "#81A1C1"
                elif text in ['sin', 'cos', 'tan', 'log', 'sqrt', '(', ')']:
                    fg_color = "#434C5E"
                    hover_color = "#4C566A"
                elif text == 'C':
                    fg_color = "#BF616A"
                    hover_color = "#D08770"
                elif text == 'DEL':
                    fg_color = "#D08770"
                    hover_color = "#EBCB8B"
                    
                btn = ctk.CTkButton(buttons_frame, text=text, font=("Arial", 18, "bold"),
                                    command=lambda t=text: self.on_button(t),
                                    fg_color=fg_color, hover_color=hover_color, corner_radius=8)
                btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=4, pady=4)

        # Equal button spans across the bottom
        buttons_frame.rowconfigure(5, weight=1)
        eq_btn = ctk.CTkButton(buttons_frame, text="=", font=("Arial", 24, "bold"),
                               command=lambda: self.on_button('='),
                               fg_color="#A3BE8C", hover_color="#8FBCBB", text_color="#2E3440", corner_radius=8)
        eq_btn.grid(row=5, column=0, columnspan=5, sticky="nsew", padx=4, pady=4)

        self.bind('<Key>', self.key_pressed)
        self.bind('<Return>', lambda e: self.on_button('='))
        self.bind('<BackSpace>', lambda e: self.on_button('DEL'))

    def key_pressed(self, event):
        char = event.char
        if char in '0123456789+-*/.^()':
            self.on_button(char)
        elif char.lower() == 'c':
            self.on_button('C')
        elif char == '=':
            self.on_button('=')

    def on_button(self, char):
        current = self.result_var.get()
        
        if char == 'C':
            self.result_var.set("0")
        elif char == 'DEL':
            if current == "Error" or len(current) == 1:
                self.result_var.set("0")
            else:
                self.result_var.set(current[:-1])
        elif char == '=':
            try:
                eval_str = current.replace('^', '**')
                safe_dict = {
                    "__builtins__": None, 
                    "sin": math.sin, 
                    "cos": math.cos, 
                    "tan": math.tan, 
                    "log": math.log10, 
                    "sqrt": math.sqrt
                }
                res = eval(eval_str, safe_dict)
                if isinstance(res, float) and res.is_integer():
                    res = int(res)
                self.result_var.set(str(res))
            except Exception:
                self.result_var.set("Error")
        else:
            append_val = char
            if char in ['sin', 'cos', 'tan', 'log', 'sqrt']:
                append_val = char + '('
                
            if current == "0" or current == "Error":
                self.result_var.set(append_val)
            else:
                self.result_var.set(current + append_val)

if __name__ == "__main__":
    app = ZeroCalc()
    app.mainloop()
