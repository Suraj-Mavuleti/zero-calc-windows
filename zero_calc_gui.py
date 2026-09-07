import customtkinter as ctk
import math

ctk.set_appearance_mode("dark")

class ZeroCalc(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Zero Scientific - God Tier Edition")
        self.geometry("680x550")
        self.configure(fg_color="#1C1C1E") 
        
        self.result_var = ctk.StringVar(value="0")
        
        display_frame = ctk.CTkFrame(self, fg_color="transparent")
        display_frame.pack(fill=ctk.BOTH, padx=20, pady=(20, 10))
        
        display = ctk.CTkEntry(display_frame, textvariable=self.result_var, 
                               font=("Helvetica Neue", 48, "bold"), justify="right", 
                               state="readonly", fg_color="transparent", border_width=0, 
                               text_color="#FFFFFF")
        display.pack(fill=ctk.BOTH, expand=True)
        
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill=ctk.BOTH, expand=True, padx=15, pady=(0, 20))
        
        buttons = [
            ('sin',  'cos',  'tan',  'C',   'DEL', '/'),
            ('asin', 'acos', 'atan', '7',   '8',   '9'),
            ('sinh', 'cosh', 'tanh', '4',   '5',   '6'),
            ('ln',   'log',  'sqrt', '1',   '2',   '3'),
            ('pi',   'e',    'fact', '.',   '0',   '='),
            ('(',    ')',    '^',    '+',   '-',   '*')
        ]
        
        color_num = "#333333"
        color_num_hover = "#444444"
        color_op = "#FF9F0A" 
        color_op_hover = "#FFB340"
        color_sci = "#555555"
        color_sci_hover = "#666666"
        color_danger = "#FF453A"
        color_danger_hover = "#FF6961"

        for row_idx, row in enumerate(buttons):
            buttons_frame.rowconfigure(row_idx, weight=1)
            for col_idx, text in enumerate(row):
                buttons_frame.columnconfigure(col_idx, weight=1)
                
                fg_color = color_num
                hover_color = color_num_hover
                text_color = "#FFFFFF"
                font = ("Helvetica Neue", 20)
                
                if text in ['/', '*', '-', '+', '^']:
                    fg_color = color_op
                    hover_color = color_op_hover
                    font = ("Helvetica Neue", 22, "bold")
                elif text == '=':
                    fg_color = "#32D74B" # iOS Green
                    hover_color = "#34C759"
                    font = ("Helvetica Neue", 26, "bold")
                elif text in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'ln', 'log', 'sqrt', 'fact', 'pi', 'e', '(', ')']:
                    fg_color = color_sci
                    hover_color = color_sci_hover
                    font = ("Helvetica Neue", 16)
                elif text == 'C':
                    fg_color = color_danger
                    hover_color = color_danger_hover
                    font = ("Helvetica Neue", 18, "bold")
                elif text == 'DEL':
                    fg_color = color_sci
                    hover_color = color_sci_hover
                    font = ("Helvetica Neue", 16, "bold")
                    
                btn = ctk.CTkButton(buttons_frame, text=text, font=font, text_color=text_color,
                                    command=lambda t=text: self.on_button(t),
                                    fg_color=fg_color, hover_color=hover_color, 
                                    corner_radius=12)
                btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=4, pady=4)

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
                
                # Math degree wrappers
                def d_sin(x): return math.sin(math.radians(x))
                def d_cos(x): return math.cos(math.radians(x))
                def d_tan(x): return math.tan(math.radians(x))
                def d_asin(x): return math.degrees(math.asin(x))
                def d_acos(x): return math.degrees(math.acos(x))
                def d_atan(x): return math.degrees(math.atan(x))
                
                safe_dict = {
                    "__builtins__": None, 
                    "sin": d_sin, "cos": d_cos, "tan": d_tan, 
                    "asin": d_asin, "acos": d_acos, "atan": d_atan,
                    "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
                    "ln": math.log, "log": math.log10, "sqrt": math.sqrt,
                    "fact": math.factorial, "pi": math.pi, "e": math.e
                }
                res = eval(eval_str, safe_dict)
                
                # Clean up floating point errors
                if isinstance(res, float):
                    res = round(res, 10)
                    if res.is_integer():
                        res = int(res)
                        
                self.result_var.set(str(res))
            except Exception:
                self.result_var.set("Error")
        else:
            append_val = char
            if char in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'ln', 'log', 'sqrt', 'fact']:
                append_val = char + '('
                
            if current == "0" or current == "Error":
                self.result_var.set(append_val)
            else:
                self.result_var.set(current + append_val)

if __name__ == "__main__":
    app = ZeroCalc()
    app.mainloop()
