# controllers/shape_controller.py
from models.shape_model import ShapeModel

class ShapeController:
    def __init__(self, layer_controller):
        """Initialize the shape controller with a reference to the layer controller."""
        self.layer_controller = layer_controller

    def set_line_color(self, layer, color):
        """Set the line color of a shape in the layer."""
        if layer in self.layer_controller.layers and isinstance(layer.object, ShapeModel):
            layer.object.set_line_color(color)

    def set_fill_color(self, layer, color):
        """Set the fill color of a shape in the layer."""
        if layer in self.layer_controller.layers and isinstance(layer.object, ShapeModel):
            layer.object.set_fill_color(color)

    def set_border_radius(self, layer, radius):
        """Set the border radius of a shape in the layer."""
        if layer in self.layer_controller.layers and isinstance(layer.object, ShapeModel):
            layer.object.set_border_radius(radius)

    def set_alpha(self, layer, alpha):
        """Set the transparency of a shape in the layer."""
        if layer in self.layer_controller.layers and isinstance(layer.object, ShapeModel):
            layer.object.set_alpha(alpha)