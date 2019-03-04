from tkinter import Tk, ttk, Toplevel, Canvas, StringVar, TclError, Radiobutton

try:
    from pyautogui import position
except ImportError:
    import ctypes

    class POINT(ctypes.Structure):
        _fields_ = (
            ("x", ctypes.c_ulong),
            ("y", ctypes.c_ulong)
        )

    cursor = POINT()

    def position():
        ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))

        return (ctypes.c_long(cursor.x).value, ctypes.c_long(cursor.y).value)
        
class main(Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Overlay")
        self.geometry("302x178+200+200")
        self.resizable(False, False)

        top = Toplevel()
        top.overrideredirect(True)
        top.attributes("-topmost", True)
        top.attributes("-transparentcolor", "SystemButtonFace")
        top.withdraw()
        
        def toggle(*args):
            if toggle_btn["text"] == "Start":
                toggle_btn["text"] = "Stop"
                top.deiconify()
            else:
                toggle_btn["text"] = "Start"
                top.withdraw()
                      
        def move():
            if top.state() == "normal":
                x, y = position()
                c = int(self.outline_var.get() or 0) + int(self.radius_var.get() or 0)
                top.geometry(f"{c*2+1}x{c*2+1}+{x-c}+{y-c}")
                top.lift()
                    
            self.after(10, move)
            
        def changed(*args):
            o = int(self.outline_var.get() or 0)
            o2 = o//2
            c = o + int(self.radius_var.get() or 0)
            self.cv.configure(width=c*2+1, height=c*2+1)
            self.cv.delete("shape")
            try:
                self.shapes[self.shape.get()](
                    o2, o2, c*2-o2, c*2-o2,
                    outline=self.color_var.get(), width=o, tag="shape"
                )
            except TclError:
                pass
            
        def validate(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
            return (value_if_allowed == "" or text in '0123456789')
            
        vcmd = (self.register(validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
            
        self.cv = Canvas(top, highlightthickness=0)
        self.cv.pack()
        self.shapes = {"circle": self.cv.create_oval, "square": self.cv.create_rectangle}
        self.cv.bind("<Button-1>", lambda *args: self.destroy())
        
        self.radius_var = StringVar()
        self.radius_var.set("50")
        self.radius_var.trace("w", changed)
        ttk.Label(self, text="Radius:").grid(sticky="w", padx=5, pady=5)
        spin = ttk.Spinbox(self, from_=1, to_=float("inf"), textvariable=self.radius_var, validate="key", validatecommand=vcmd)
        spin.grid(column=1, row=0, sticky="we", padx=5, pady=5)
        
        self.outline_var = StringVar()
        self.outline_var.set("5")
        self.outline_var.trace("w", changed)
        label = ttk.Label(self, text="Outline Width:")
        label.grid(column=0, row=1, sticky="w", padx=5, pady=5)
        spin = ttk.Spinbox(self, from_=1, to_=float("inf"), textvariable=self.outline_var, validate="key", validatecommand=vcmd)
        spin.grid(column=1, row=1, sticky="we", padx=5, pady=5)
        
        self.color_var = StringVar()
        self.color_var.set("blue")
        self.color_var.trace("w", changed)
        label = ttk.Label(self, text="Color (name or hex value):")
        label.grid(column=0, row=2, sticky="w", padx=5, pady=5)
        entry = ttk.Entry(self, textvariable=self.color_var)
        entry.grid(column=1, row=2, sticky="we", padx=5, pady=5)
        
        frame = ttk.Frame(self)
        frame.grid(column=0, row=3, sticky="we", padx=5, pady=5)
        
        self.shape = StringVar()
        self.shape.set("circle")
        self.shape.trace("w", changed)
        ttk.Radiobutton(frame, text="Circle", variable=self.shape, value="circle").pack(anchor="w")
        ttk.Radiobutton(frame, text="Square", variable=self.shape, value="square").pack(anchor="w")
            
        toggle_btn = ttk.Button(self, text="Start", command=toggle)
        toggle_btn.grid(column=0, row=4, columnspan=2, padx=5, pady=5)
        
        changed()
        self.after(10, move)
        self.focus()
        self.mainloop()

if __name__ == "__main__":
    x = main()