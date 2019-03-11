from math import sin, cos, radians
from pyautogui import position
from tkinter import Tk, ttk, Toplevel, Canvas, StringVar, TclError

class var(StringVar):
    def __init__(self, init_value, trace):
        super().__init__()
        
        self.set(init_value)
        self.trace("w", trace)
        
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
                outline = int(self.outline_var.get() or 0)
                radius = int(self.radius_var.get() or 0)
                center = outline + radius
                
                width = height = center * 2 + 1
                x -= center
                y -= center
                
                top.geometry(f"{width}x{height}+{x}+{y}")
                top.lift()
                    
            self.after(10, move)
            
        cv = Canvas(top, highlightthickness=0)
        cv.bind("<Button-1>", toggle)
        cv.pack()
        def create_circle(x1, y1, x2, y2, **args):
            radius = (x2 - x1) // 2
            center = (x2 + x1) // 2
            cv.create_line(
                [
                    position
                    for angle in range(361)
                    for position in (
                        radius * sin(radians(angle)) + center,
                        radius * cos(radians(angle)) + center
                    )
                ],
                fill=args["outline"],
                tags="shape",
                width=args["width"]
            )
        
        shapes = {
            "circle": create_circle,
            "square": cv.create_rectangle
        }
            
        def changed(*args):
            outline = int(self.outline_var.get() or 0) // 2
            center = outline * 2 + int(self.radius_var.get() or 0)
            
            cv.configure(width=center * 2 + 1, height=center * 2 + 1)
            cv.delete("shape")
            
            x1 = y1 = outline
            x2 = y2 = center * 2 - outline
            
            try:
                shapes[self.shape.get()](
                    x1, y1, x2, y2,
                    outline=self.color_var.get(),
                    width=outline * 2,
                    tag="shape"
                )
            except TclError:
                pass
            
        # Save this for future reference
        # def validate(action, index, value_if_allowed, prior_value, text,
        #     validation_type, trigger_type, widget_name):
        # vcmd = (
        #     self.register(validate),
        #     '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'
        # )
        # widget keyword arguments (
        #     validate="key",
        #     validatecommand=vcmd
        # )
        
        def validate(value_if_allowed, text):
            return value_if_allowed == "" or text in '0123456789'
            
        vcmd = (self.register(validate), '%P', '%S')
        
        self.radius_var = var("50", changed)
        label = ttk.Label(self, text="Radius:")
        label.grid(sticky="w", padx=5, pady=5)
        spin = ttk.Spinbox(
            self, from_=1, to_=float("inf"),
            textvariable=self.radius_var,
            validate="key",
            validatecommand=vcmd
        )
        spin.grid(column=1, row=0, sticky="we", padx=5, pady=5)
        
        self.outline_var = var("5", changed)
        label = ttk.Label(self, text="Outline Width:")
        label.grid(column=0, row=1, sticky="w", padx=5, pady=5)
        spin = ttk.Spinbox(
            self, from_=1, to_=float("inf"),
            textvariable=self.outline_var,
            validate="key",
            validatecommand=vcmd
        )
        spin.grid(column=1, row=1, sticky="we", padx=5, pady=5)
        
        self.color_var = var("blue", changed)
        label = ttk.Label(self, text="Color (name or hex value):")
        label.grid(column=0, row=2, sticky="w", padx=5, pady=5)
        entry = ttk.Entry(self, textvariable=self.color_var)
        entry.grid(column=1, row=2, sticky="we", padx=5, pady=5)
        
        frame = ttk.Frame(self)
        frame.grid(column=0, row=3, sticky="we", padx=5, pady=5)
        
        self.shape = var("circle", changed)
        ttk.Radiobutton(
            frame, text="Circle",
            variable=self.shape, value="circle"
        ).pack(anchor="w")
        ttk.Radiobutton(
            frame, text="Square",
            variable=self.shape, value="square"
        ).pack(anchor="w")
            
        toggle_btn = ttk.Button(self, text="Start", command=toggle)
        toggle_btn.grid(column=0, row=4, columnspan=2, padx=5, pady=5)
        
        changed()
        self.after(10, move)
        self.focus()
        self.mainloop()

if __name__ == "__main__":
    main()
