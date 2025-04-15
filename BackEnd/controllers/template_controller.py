from BackEnd.models.canvas_element import CanvasElement


class CanvasController:
    def __init__(self, canvas):
        self.canvas = canvas
        self.elements = []
        self.selected = None

    def add_image(self, path, img, tk_img, x=100, y=100):
        item = self.canvas.create_image(x, y, image=tk_img, anchor="nw")
        element = CanvasElement("image", item, path=path, img=img, tk_img=tk_img, x=x, y=y, angle=0)
        self.elements.append(element)
        return item

    def add_text(self, text, font, size, color, x=150, y=150):
        item = self.canvas.create_text(x, y, text=text, font=(font, size), anchor="nw", fill=color)
        element = CanvasElement("text", item, text=text, font=font, size=size, color=color)
        self.elements.append(element)
        return item

    def get_element_by_item(self, item_id):
        return next((el for el in self.elements if el.item == item_id), None)

    def delete_selected(self):
        if self.selected:
            self.canvas.delete(self.selected.item)
            self.elements.remove(self.selected)
            self.selected = None
