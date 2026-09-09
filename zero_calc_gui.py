import sys
import gi
import os
import math
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango

class ZeroCalc(Gtk.Window):
    def __init__(self):
        super().__init__(title="Zero Calc - Ultimate Studio")
        self.set_default_size(800, 600)
        
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = ""
        self.header.get_style_context().add_class("hidden-header")
        self.set_titlebar(self.header)
        
        self.setup_css()
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(main_box)
        
        # ================= CALCULATOR AREA =================
        calc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        calc_box.get_style_context().add_class("calc-box")
        main_box.pack_start(calc_box, True, True, 0)
        
        # Display
        display_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        display_box.get_style_context().add_class("display-box")
        
        self.lbl_history = Gtk.Label(label="")
        self.lbl_history.set_halign(Gtk.Align.END)
        self.lbl_history.get_style_context().add_class("display-history")
        
        self.lbl_main = Gtk.Label(label="0")
        self.lbl_main.set_halign(Gtk.Align.END)
        self.lbl_main.get_style_context().add_class("display-main")
        
        display_box.pack_start(self.lbl_history, True, True, 0)
        display_box.pack_start(self.lbl_main, True, True, 0)
        calc_box.pack_start(display_box, False, False, 0)
        
        # Keypad Grid
        grid = Gtk.Grid(column_spacing=15, row_spacing=15)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_valign(Gtk.Align.CENTER)
        grid.set_margin_top(30)
        grid.set_margin_bottom(30)
        calc_box.pack_start(grid, True, True, 0)
        
        buttons = [
            ("AC", "act"), ("(", "act"), (")", "act"), ("/", "op"),
            ("7", "num"), ("8", "num"), ("9", "num"), ("*", "op"),
            ("4", "num"), ("5", "num"), ("6", "num"), ("-", "op"),
            ("1", "num"), ("2", "num"), ("3", "num"), ("+", "op"),
            ("0", "num"), (".", "num"), ("=", "eq")
        ]
        
        row, col = 0, 0
        for text, cls in buttons:
            btn = Gtk.Button(label=text)
            btn.get_style_context().add_class("calc-btn")
            btn.get_style_context().add_class(f"btn-{cls}")
            btn.set_size_request(80, 80)
            btn.connect("clicked", self.on_btn_clicked, text)
            
            if text == "0":
                grid.attach(btn, col, row, 2, 1)
                col += 2
            elif text == "=":
                btn.set_size_request(80, 175)
                grid.attach(btn, col, row - 1, 1, 2)
                col += 1
            else:
                grid.attach(btn, col, row, 1, 1)
                col += 1
                
            if col > 3:
                col = 0
                row += 1
                
        # ================= SIDEBAR (TAPE / GRAPH) =================
        self.sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sidebar.set_size_request(280, -1)
        self.sidebar.get_style_context().add_class("sidebar")
        main_box.pack_start(self.sidebar, False, False, 0)
        
        logo = Gtk.Label(label="Z E R O C A L C")
        logo.get_style_context().add_class("sidebar-logo")
        logo.set_margin_top(20)
        logo.set_margin_bottom(20)
        self.sidebar.pack_start(logo, False, False, 0)
        
        lbl_tape = Gtk.Label(label="CALCULATION TAPE")
        lbl_tape.get_style_context().add_class("section-label")
        lbl_tape.set_halign(Gtk.Align.START)
        lbl_tape.set_margin_start(20)
        lbl_tape.set_margin_bottom(10)
        self.sidebar.pack_start(lbl_tape, False, False, 0)
        
        self.tape_list = Gtk.ListBox()
        self.tape_list.get_style_context().add_class("transparent-list")
        
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.tape_list)
        self.sidebar.pack_start(scroll, True, True, 0)
        
        self.current_expr = ""
        self.new_input = True
        
    def add_to_tape(self, expr, res):
        row = Gtk.ListBoxRow()
        row.get_style_context().add_class("tape-row")
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        l_exp = Gtk.Label(label=expr)
        l_exp.set_halign(Gtk.Align.END)
        l_exp.get_style_context().add_class("tape-exp")
        l_res = Gtk.Label(label=f"= {res}")
        l_res.set_halign(Gtk.Align.END)
        l_res.get_style_context().add_class("tape-res")
        vbox.pack_start(l_exp, False, False, 2)
        vbox.pack_start(l_res, False, False, 2)
        vbox.set_margin_start(15)
        vbox.set_margin_end(15)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        row.add(vbox)
        self.tape_list.add(row)
        self.tape_list.show_all()

    def on_btn_clicked(self, btn, text):
        if text == "AC":
            self.current_expr = ""
            self.lbl_history.set_text("")
            self.lbl_main.set_text("0")
            self.new_input = True
        elif text == "=":
            try:
                res = str(eval(self.current_expr))
                self.lbl_history.set_text(self.current_expr + " =")
                self.lbl_main.set_text(res)
                self.add_to_tape(self.current_expr, res)
                self.current_expr = res
                self.new_input = True
            except:
                self.lbl_main.set_text("Error")
                self.current_expr = ""
                self.new_input = True
        else:
            if self.new_input and text.isdigit():
                self.current_expr = ""
            self.new_input = False
            self.current_expr += text
            self.lbl_main.set_text(self.current_expr)

    def setup_css(self):
        css = b'''
            window { background-color: #030305; }
            .hidden-header { background: #030305; min-height: 0px; padding: 0px; border: none; box-shadow: none; }
            .calc-box { background: radial-gradient(circle at top left, #10141E, #030305); }
            .display-box { padding: 40px; }
            .display-history { color: #8B94A5; font-size: 24px; margin-bottom: 10px; font-weight: bold; }
            .display-main { color: #FFFFFF; font-size: 72px; font-weight: 200; text-shadow: 0 0 20px rgba(0, 229, 255, 0.4); letter-spacing: -2px; }
            .calc-btn { border-radius: 20px; font-size: 28px; font-weight: bold; border: none; box-shadow: 0 10px 20px rgba(0,0,0,0.3); transition: all 0.2s ease; margin: 5px; }
            .calc-btn:hover { transform: translateY(-3px); box-shadow: 0 15px 30px rgba(0,0,0,0.5); }
            .btn-num { background: rgba(255,255,255,0.05); color: #FFFFFF; }
            .btn-num:hover { background: rgba(255,255,255,0.1); }
            .btn-op { background: rgba(0, 229, 255, 0.1); color: #00E5FF; }
            .btn-op:hover { background: rgba(0, 229, 255, 0.2); }
            .btn-act { background: rgba(255, 51, 102, 0.1); color: #FF3366; }
            .btn-act:hover { background: rgba(255, 51, 102, 0.2); }
            .btn-eq { background: linear-gradient(45deg, #00E5FF, #0099FF); color: #000000; }
            .btn-eq:hover { box-shadow: 0 15px 30px rgba(0, 229, 255, 0.4); }
            .sidebar { background-color: rgba(8, 10, 16, 0.98); border-left: 1px solid rgba(255, 255, 255, 0.05); }
            .sidebar-logo { color: #FFFFFF; font-size: 20px; font-weight: 900; letter-spacing: 5px; text-shadow: 0 0 15px rgba(0, 229, 255, 0.6); }
            .section-label { color: #4A5568; font-size: 11px; font-weight: 900; letter-spacing: 2px; }
            .transparent-list { background: transparent; }
            .tape-row { background: transparent; border-bottom: 1px solid rgba(255,255,255,0.02); }
            .tape-exp { color: #8B94A5; font-size: 14px; }
            .tape-res { color: #00E5FF; font-size: 18px; font-weight: bold; }
        '''
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

if __name__ == "__main__":
    win = ZeroCalc()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
