# controllers/tool_controller.py
from tools.shape_tool import ShapeTool

class ToolController:
    def __init__(self, app_controller):
        self.app = app_controller
        self.current_tool = None

    def add_shape(self, shape_type, x, y, width, height):
        shape = ShapeTool(shape_type, x, y, width, height)
        self.app.layer_controller.add_layer(shape)