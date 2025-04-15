# UILogic/editor_main.py
import sys
import os
import pygame
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QLabel
from BackEnd.controllers.layer_controller import LayerController
from BackEnd.controllers.shape_controller import ShapeController
from BackEnd.models.layerList_model import LayerList
from BackEnd.tools.shape_tool import ShapeTool
from UILogic.shape_manager import ShapeManager


# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class EditorMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI/EditorMainWindow.ui", self)

        # Initialize backend components
        self.layer_list = LayerList()
        self.layer_controller = LayerController(self.layer_list)
        self.shape_controller = ShapeController(self.layer_controller)
        self.shape_tool = ShapeTool()

        # Initialize Pygame for drawing
        pygame.init()
        self.canvas_size = (self.canvasFrame.width(), self.canvasFrame.height())
        self.canvas_surface = pygame.Surface(self.canvas_size, pygame.SRCALPHA)
        self.canvas_surface.fill((255, 255, 255, 0))  # Transparent background

        # Replace the placeholder QLabel with a custom QLabel to display Pygame surface
        self.canvas_label = QLabel(self.canvasFrame)
        self.canvas_label.setGeometry(0, 0, self.canvas_size[0], self.canvas_size[1])
        self.canvas_label.setStyleSheet("background-color: white;")

        # Initialize managers
        self.shape_manager = ShapeManager(
            self.layer_controller, self.shape_controller, self.shape_tool,
            self.canvas_size, self.canvas_surface, self.canvas_label
        )
        
        # Connect tool buttons to switch pages in the stacked widget
        self.btnText.clicked.connect(lambda: self.toolsStackedWidget.setCurrentWidget(self.pageText))
        self.btnShapes.clicked.connect(lambda: self.toolsStackedWidget.setCurrentWidget(self.pageShapes))
        self.btnUpload.clicked.connect(lambda: self.toolsStackedWidget.setCurrentWidget(self.pageUpload))
        self.btnImages.clicked.connect(lambda: self.toolsStackedWidget.setCurrentWidget(self.pageImages))

        # Connect shape selection buttons
        self.btnSquare.clicked.connect(lambda: self.shape_manager.select_shape("square"))
        self.btnCircle.clicked.connect(lambda: self.shape_manager.select_shape("circle"))
        self.btnTriangle.clicked.connect(lambda: self.shape_manager.select_shape("triangle"))
        self.btnStar.clicked.connect(lambda: self.shape_manager.select_shape("star"))

        # Connect the "Add" button to add the selected shape to the canvas
        self.addButtonShapes.clicked.connect(lambda: self.shape_manager.add_shape_to_canvas(self))

        # Initial render
        self.shape_manager.update_canvas()

    def closeEvent(self, event):
        pygame.quit()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EditorMainWindow()
    window.show()
    sys.exit(app.exec_())