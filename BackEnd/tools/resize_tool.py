from PIL import Image, ImageTk

class ResizeTool:
    def __init__(self, canvas, elements, update_handle_callback):
        self.canvas = canvas
        self.elements = elements
        self.update_handle_callback = update_handle_callback

    def resize(self, selected, event):
        for element in self.elements:
            if element.get("item") == selected and element["type"] == "image":
                x, y = element["x"], element["y"]
                new_w = max(10, event.x - x)
                new_h = max(10, event.y - y)
                resized = element["img"].resize((new_w, new_h))
                tk_img = ImageTk.PhotoImage(resized)
                self.canvas.itemconfig(selected, image=tk_img)
                self.canvas.image = tk_img
                element["tk_img"] = tk_img
                element["img"] = resized
                self.update_handle_callback(x, y, new_w, new_h)
                break
