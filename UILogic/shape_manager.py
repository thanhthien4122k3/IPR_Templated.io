# UILogic/shape_manager.py
import pygame
from PyQt5.QtWidgets import QMessageBox
from BackEnd.models.shape_model import ShapeModel

class ShapeManager:
    def __init__(self, layer_controller, shape_controller, shape_tool, canvas_size, canvas_surface, canvas_label):
        self.layer_controller = layer_controller
        self.shape_controller = shape_controller
        self.shape_tool = shape_tool
        self.canvas_size = canvas_size
        self.canvas_surface = canvas_surface
        self.canvas_label = canvas_label
        self.selected_shape_type = None

    def select_shape(self, shape_type):
        """Store the selected shape type."""
        self.selected_shape_type = shape_type
        print(f"Selected shape: {shape_type}")  # For debugging

    def add_shape_to_canvas(self, parent):
        """Add the selected shape to the canvas."""
        if not self.selected_shape_type:
            QMessageBox.warning(parent, "No Shape Selected", "Please select a shape first.")
            return

        # Map the selected shape type to the appropriate type for ShapeTool
        shape_types = {
            "square": "square",
            "circle": "circle",
            "triangle": "triangle",
            "star": "star"
        }
        shape_type = shape_types.get(self.selected_shape_type)

        if shape_type:
            # Create a new shape model
            shape = ShapeModel(shape_type, 100, 100)  # Default size: 100x100
            shape.fill_color = (255, 0, 0)  # Default fill color (red)

            # Add the shape as a layer
            layer = self.layer_controller.add_layer(shape, name=self.selected_shape_type)
            layer.x = self.canvas_size[0] // 2 - 50  # Center the shape
            layer.y = self.canvas_size[1] // 2 - 50
            self.layer_controller.select_layer(layer)

            # Redraw the canvas
            self.update_canvas()

    def update_canvas(self):
        """Update the canvas by drawing all visible layers."""
        self.canvas_surface.fill((255, 255, 255, 0))  # Clear the canvas

        for layer in self.layer_controller.get_visible_layers():
            if isinstance(layer.object, ShapeModel):
                shape = layer.object
                temp_surface = pygame.Surface((shape.width, shape.height), pygame.SRCALPHA)
                temp_surface.fill((0, 0, 0, 0))  # Transparent background

                self.shape_tool.draw(
                    temp_surface,
                    shape.shape_type,
                    shape.width,
                    shape.height,
                    shape.line_color,
                    shape.line_thickness,
                    shape.fill_color,
                    shape.border_radius,
                    shape.alpha,
                    layer.rotation
                )

                self.canvas_surface.blit(temp_surface, (layer.x, layer.y))

        pygame_image = pygame.image.tostring(self.canvas_surface, "RGBA")
        qimage = parent.QtGui.QImage(pygame_image, self.canvas_size[0], self.canvas_size[1], parent.QtGui.QImage.Format_RGBA8888)
        pixmap = parent.QtGui.QPixmap.fromImage(qimage)
        self.canvas_label.setPixmap(pixmap)