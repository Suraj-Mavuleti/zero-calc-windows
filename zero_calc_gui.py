import customtkinter as ctk
import math

ctk.set_appearance_mode("dark")

class ZeroCalc(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Zero Scientific - Premium Edition")
        self.geometry("400x680")
        self.configure(fg_color="#1C1C1E") # Deep iOS-style dark background
        
        self.result_var = ctk.StringVar(value="0")
        
        # Display Area (Large, borderless, clean)
        display_frame = ctk.CTkFrame(self, fg_color="transparent")
        display_frame.pack(fill=ctk.BOTH, padx=20, pady=(40, 20))
        
        display = ctk.CTkEntry(display_frame, textvariable=self.result_var, 
                               font=("Helvetica Neue", 54, "bold"), justify="right", 
                               state="readonly", fg_color="transparent", border_width=0, 
                               text_color="#FFFFFF")
        display.pack(fill=ctk.BOTH, expand=True)
        
        # Buttons Frame
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill=ctk.BOTH, expand=True, padx=15, pady=(0, 20))
        
        buttons = [
            ('sin', 'cos', 'tan', 'C', 'DEL'),
            ('log', 'sqrt', '(', ')', '^'),
            ('7', '8', '9', '/', '*'),
            ('4', '5', '6', '-', '+'),
            ('1', '2', '3', '0', '.')
        ]
        
        # Premium iOS Colors
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
                
                # Determine styling
                fg_color = color_num
                hover_color = color_num_hover
                text_color = "#FFFFFF"
                font = ("Helvetica Neue", 22)
                
                if text in ['/', '*', '-', '+', '^']:
                    fg_color = color_op
                    hover_color = color_op_hover
                    font = ("Helvetica Neue", 26, "bold")
                elif text in ['sin', 'cos', 'tan', 'log', 'sqrt', '(', ')']:
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
                                    corner_radius=20)
                btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=6, pady=6)

        # Equal button spanning bottom
        buttons_frame.rowconfigure(5, weight=1)
        eq_btn = ctk.CTkButton(buttons_frame, text="=", font=("Helvetica Neue", 32, "bold"),
                               command=lambda: self.on_button('='),
                               fg_color=color_op, hover_color=color_op_hover, text_color="#FFFFFF", 
                               corner_radius=20)
        eq_btn.grid(row=5, column=0, columnspan=5, sticky="nsew", padx=6, pady=6)

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
