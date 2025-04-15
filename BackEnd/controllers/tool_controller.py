# controllers/tool_controller.py

from tools.shape_tool import ShapeTool
from tools.drag_tool import DragTool
from tools.resize_tool import ResizeTool
from tools.rotate_tool import RotateTool


class ToolController:
    def __init__(self, app_controller, canvas, elements, update_handle_callback):
        self.app = app_controller
        self.current_tool = None
        self.drag_tool = DragTool(canvas, elements, update_handle_callback)
        self.resize_tool = ResizeTool(canvas, elements, update_handle_callback)
        self.rotate_tool = RotateTool(canvas, elements)

    def add_shape(self, shape_type, x, y, width, height):
        shape = ShapeTool(shape_type, x, y, width, height)
        self.app.layer_controller.add_layer(shape)

    def handle_drag(self, selected, event):
        self.drag_tool.drag(selected, event)

    def handle_resize(self, selected, event):
        self.resize_tool.resize(selected, event)

    def handle_rotate(self, selected):
        self.rotate_tool.rotate(selected)

