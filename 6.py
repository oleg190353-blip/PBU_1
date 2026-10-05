import tkinter as tk


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title()

        self.pen_width = 10

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()

        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)

        self.width_entry = tk.Entry(control_frame, width=10)
        self.width_entry.insert(0, str(self.pen_width))
        self.width_entry.pack(side=tk.LEFT, padx=5)

        set_width_btn = tk.Button(control_frame, command=self.set_pen_width)
        set_width_btn.pack(side=tk.LEFT, padx=5)

        self.last_x, self.last_y = None, None

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_position)

    def set_pen_width(self):
        value = self.width_entry.get().strip()
        try:
            new_width = int(value)
            if new_width <= 0:
                return
            self.pen_width = new_width
        except ValueError:
            return

    def draw(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(
                self.last_x,
                self.last_y,
                event.x,
                event.y,
                width=self.pen_width,
                capstyle=tk.ROUND,
                smooth=True,
                splinesteps=12)

        self.last_x = event.x
        self.last_y = event.y

    def reset_position(self):
        self.last_x = None
        self.last_y = None


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
