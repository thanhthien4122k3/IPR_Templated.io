# UILogic/add_shape.py
import sys
import pygame
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage, QPixmap
from BackEnd.controllers.layer_controller import LayerController
from BackEnd.controllers.shape_controller import ShapeController
from BackEnd.models.layer_model import LayerModel
from BackEnd.models.layerList_model import LayerList
from BackEnd.models.shape_model import ShapeModel
from BackEnd.tools.shape_tool import ShapeTool

class AddShapeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file
        uic.loadUi("GUI/addShape.ui", self)

        # Initialize backend components
        self.layer_list = LayerList()
        self.layer_controller = LayerController(self.layer_list)
        self.shape_controller = ShapeController(self.layer_controller)
        self.shape_tool = ShapeTool()

        # Initialize Pygame for drawing shapes
        pygame.init()
        self.canvas_size = (self.widgetCanvas.width(), self.widgetCanvas.height())
        self.canvas_surface = pygame.Surface(self.canvas_size, pygame.SRCALPHA)
        self.canvas_surface.fill((255, 255, 255, 0))  # Transparent background

        # Replace the placeholder QLabel with a custom QLabel to display Pygame surface
        self.canvas_label = QLabel(self.widgetCanvas)
        self.canvas_label.setGeometry(0, 0, self.canvas_size[0], self.canvas_size[1])
        self.canvas_label.setStyleSheet("background-color: white;")

        # Connect events
        self.Shapes.itemClicked.connect(self.add_shape_to_canvas)

        # Initial render
        self.update_canvas()

    def add_shape_to_canvas(self, item):
        """Add a new shape to the canvas when a shape is selected from the list."""
        shape_name = item.text().lower()
        shape_type = self.map_shape_name_to_type(shape_name)

        if shape_type:
            # Create a new shape model
            shape = ShapeModel(shape_type, 100, 100)  # Default size: 100x100
            if "filled" in shape_name:
                shape.fill_color = (255, 0, 0)  # Default fill color (red) for filled shapes
            else:
                shape.fill_color = None  # No fill for outline shapes

            # Add the shape as a layer
            layer = self.layer_controller.add_layer(shape, name=shape_name)
            layer.x = self.canvas_size[0] // 2 - 50  # Center the shape
            layer.y = self.canvas_size[1] // 2 - 50
            self.layer_controller.select_layer(layer)

            # Redraw the canvas
            self.update_canvas()

    def map_shape_name_to_type(self, shape_name):
        """Map the shape name from the UI to the shape type used by ShapeTool."""
        mapping = {
            "square_filled": "square",
            "square_not filled": "outline_square",
            "circle_filled": "circle",
            "circle_not filled": "outline_circle",
            "triangle_filled": "triangle",
            "triangle_not filled": "outline_triangle",
            "star_filled": "star",
            "star_not filled": "outline_star",
            "heart_filled": "heart",
            "heart_not filled": "outline_heart",
            "polygon_filled": "polygon",
            "polygon_not filled": "outline_polygon",
        }
        return mapping.get(shape_name.lower(), None)

    def update_canvas(self):
        """Update the canvas by drawing all visible layers."""
        # Clear the canvas
        self.canvas_surface.fill((255, 255, 255, 0))

        # Draw all visible layers
        for layer in self.layer_controller.get_visible_layers():
            if isinstance(layer.object, ShapeModel):
                shape = layer.object
                # Create a temporary surface for the shape
                temp_surface = pygame.Surface((shape.width, shape.height), pygame.SRCALPHA)
                temp_surface.fill((0, 0, 0, 0))  # Transparent background

                # Use ShapeTool to draw the shape
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

                # Blit the shape onto the canvas at the layer's position
                self.canvas_surface.blit(temp_surface, (layer.x, layer.y))

        # Convert Pygame surface to QImage for display in Qt
        pygame_image = pygame.image.tostring(self.canvas_surface, "RGBA")
        qimage = QImage(pygame_image, self.canvas_size[0], self.canvas_size[1], QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimage)
        self.canvas_label.setPixmap(pixmap)

    def closeEvent(self, event):
        """Clean up Pygame when the window is closed."""
        pygame.quit()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AddShapeWindow()
    window.show()
    sys.exit(app.exec_())