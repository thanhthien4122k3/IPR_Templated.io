class DragTool:
    def __init__(self, canvas, elements, update_handle_callback):
        self.canvas = canvas
        self.elements = elements
        self.update_handle_callback = update_handle_callback

    def drag(self, selected, event):
        self.canvas.coords(selected, event.x, event.y)
        for element in self.elements:
            if element.get("item") == selected and element["type"] == "image":
                element["x"], element["y"] = event.x, event.y
                self.update_handle_callback(event.x, event.y, *element["img"].size)
