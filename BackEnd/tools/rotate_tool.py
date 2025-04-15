from PIL import ImageTk

class RotateTool:
    def __init__(self, canvas, elements):
        self.canvas = canvas
        self.elements = elements

    def rotate(self, selected):
        for element in self.elements:
            if element.get("item") == selected and element["type"] == "image":
                element["angle"] = (element.get("angle", 0) + 45) % 360
                rotated = element["img"].rotate(element["angle"], expand=True)
                tk_img = ImageTk.PhotoImage(rotated)
                self.canvas.itemconfig(selected, image=tk_img)
                self.canvas.image = tk_img
                element["tk_img"] = tk_img
                break
