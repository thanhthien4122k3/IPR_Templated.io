class LayoutModel:
    def __init__(self, canvas):
        self.canvas = canvas

    def apply_layout(self, layout_type, width, height):
        self.canvas.delete("all")
        if layout_type == "basic":
            self.canvas.create_rectangle(0, 0, width, 100, fill="#f0f0f0")
            self.canvas.create_text(20, 30, text="HEADER", anchor="nw", font=("Arial", 24))
            self.canvas.create_rectangle(0, height - 100, width, height, fill="#f0f0f0")
            self.canvas.create_text(20, height - 70, text="FOOTER", anchor="nw", font=("Arial", 20))
