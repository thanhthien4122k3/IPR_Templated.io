import tkinter as tk
from BackEnd.controllers.template_controller import CanvasController
from models.layout_model import LayoutModel

def main():
    root = tk.Tk()
    root.title("Template.io MVC")
    width, height = 800, 1000

    font_var = tk.StringVar(value="Arial")
    main_view = MainWindow(root, width, height)
    canvas = main_view.canvas

    controller = CanvasController(canvas)
    layout = LayoutModel(canvas)

    toolbar = Toolbar(root, font_var, {
        "add_image": lambda: print("Add image"),
        "add_text": lambda: print("Add text"),
        "rotate": lambda: print("Rotate"),
        "delete": lambda: controller.delete_selected(),
        "layout": lambda: layout.apply_layout("basic", width, height),
        "export": lambda: print("Export")
    })

    root.mainloop()

if __name__ == "__main__":
    main()
