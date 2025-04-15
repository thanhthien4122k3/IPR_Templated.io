from PyQt6.QtWidgets import QColorDialog
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QPixmap, QIcon, QImage
from PyQt6.QtCore import Qt
from BackEnd.controllers.text_controller import TextController

class TextManager:
    """
    Class that connects the UI text-related elements with the backend TextController.
    Manages text creation, formatting, and transformations.
    """
    def __init__(self, main_window):
        """
        Initialize the TextManager with a reference to the main window.
        
        Args:
            main_window: The main editor window instance with UI elements
        """
        self.main_window = main_window
        self.text_controllers = []  # List to store TextController instances
        self.current_controller = None  # Currently selected TextController
        self.setup_connections()

    def setup_connections(self):
        """Connect UI buttons and widgets to their respective actions."""
        # Connect text tool activation
        self.main_window.btnText.clicked.connect(self.activate_tool)
        
        # Connect formatting buttons
        self.main_window.btnBold.clicked.connect(self.toggle_bold)
        self.main_window.btnItalic.clicked.connect(self.toggle_italic)
        self.main_window.btnUnderline.clicked.connect(self.toggle_underline)
        
        # Connect alignment buttons
        self.main_window.btnAlignLeft.clicked.connect(lambda: self.set_alignment("left"))
        self.main_window.btnAlignCenter.clicked.connect(lambda: self.set_alignment("center"))
        self.main_window.btnAlignRight.clicked.connect(lambda: self.set_alignment("right"))
        
        # Connect font and color selection
        self.main_window.fontComboBox.currentTextChanged.connect(self.change_font)
        self.main_window.btnTextColor.clicked.connect(self.change_color)
        
        # Connect canvas mouse events
        self.main_window.canvasFrame.mousePressEvent = self.canvas_mouse_press
        # TODO: Add mouseMoveEvent and mouseReleaseEvent for dragging

    def activate_tool(self):
        """Activate the text tool and switch to the text page."""
        self.main_window.toolsStackedWidget.setCurrentIndex(0)  # pageText
        self.main_window.btnText.setChecked(True)
        self.main_window.btnShapes.setChecked(False)
        self.main_window.btnImages.setChecked(False)
        self.main_window.btnUpload.setChecked(False)
        print("Text tool activated")

    def add_text(self, text="New Text", x=100, y=100):
        """
        Add a new text object to the canvas.
        
        Args:
            text (str): Initial text content
            x (int): X-coordinate for the text
            y (int): Y-coordinate for the text
        """
        controller = TextController(x, y, text)
        self.text_controllers.append(controller)
        self.select_controller(controller)
        self.render_canvas()
        print(f"Added text: {text}")

    def select_controller(self, controller):
        """Select a text controller and deselect others."""
        if self.current_controller:
            self.current_controller.deselect()
        self.current_controller = controller
        if controller:
            controller.select()
        self.update_ui_for_selection()

    def canvas_mouse_press(self, event):
        """
        Handle mouse press events on the canvas to select text.
        
        Args:
            event: The mouse event
        """
        mouse_x = event.position().x()
        mouse_y = event.position().y()
        
        # Check if any text is clicked
        for controller in reversed(self.text_controllers):
            if controller.is_point_inside(mouse_x, mouse_y):
                self.select_controller(controller)
                # TODO: Enable dragging with controller.toggle_dragging(True)
                return
        
        # If no text is clicked, deselect current text
        self.select_controller(None)

    def toggle_bold(self):
        """Toggle bold formatting for the selected text."""
        if self.current_controller:
            bold = not self.current_controller.model.style.bold
            self.current_controller.set_formatting(bold=bold)
            self.render_canvas()
            print(f"Toggled bold: {bold}")

    def toggle_italic(self):
        """Toggle italic formatting for the selected text."""
        if self.current_controller:
            italic = not self.current_controller.model.style.italic
            self.current_controller.set_formatting(italic=italic)
            self.render_canvas()
            print(f"Toggled italic: {italic}")

    def toggle_underline(self):
        """Toggle underline formatting for the selected text."""
        if self.current_controller:
            underline = not self.current_controller.model.style.underline
            self.current_controller.set_formatting(underline=underline)
            self.render_canvas()
            print(f"Toggled underline: {underline}")

    def set_alignment(self, align):
        """Set text alignment for the selected text."""
        if self.current_controller:
            self.current_controller.set_formatting(align=align)
            self.render_canvas()
            print(f"Set alignment: {align}")

    def change_font(self, font_name):
        """Change the font for the selected text."""
        if self.current_controller:
            self.current_controller.set_formatting(font_name=font_name)
            self.render_canvas()
            print(f"Changed font to: {font_name}")

    def change_color(self):
        """Open a color dialog to change the text color."""
        if self.current_controller:
            color = QColorDialog.getColor(initial=QColor(self.current_controller.model.style.color))
            if color.isValid():
                color_tuple = (color.red(), color.green(), color.blue())
                self.current_controller.set_formatting(color=color_tuple)
                self.render_canvas()
                print(f"Changed color to: {color_tuple}")

    def update_text(self, new_text):
        """Update the content of the selected text."""
        if self.current_controller:
            self.current_controller.update_text(new_text)
            self.render_canvas()
            print(f"Updated text to: {new_text}")

    def move_text(self, dx, dy):
        """Move the selected text by dx, dy."""
        if self.current_controller:
            self.current_controller.move(dx, dy)
            self.render_canvas()
            print(f"Moved text by ({dx}, {dy})")

    def rotate_text(self, angle):
        """Rotate the selected text by the specified angle."""
        if self.current_controller:
            self.current_controller.rotate(angle)
            self.render_canvas()
            print(f"Rotated text by {angle} degrees")

    def flip_text_horizontal(self):
        """Flip the selected text horizontally."""
        if self.current_controller:
            self.current_controller.flip_horizontal()
            self.render_canvas()
            print("Flipped text horizontally")

    def flip_text_vertical(self):
        """Flip the selected text vertically."""
        if self.current_controller:
            self.current_controller.flip_vertical()
            self.render_canvas()
            print("Flipped text vertically")

    def delete_selected_text(self):
        """Delete the selected text."""
        if self.current_controller:
            self.text_controllers.remove(self.current_controller)
            self.current_controller = None
            self.render_canvas()
            print("Deleted selected text")

    def render_canvas(self):
        """Render all text objects on the canvas (placeholder)."""
        # TODO: Implement with QGraphicsView
        self.clear_canvas()
        for controller in self.text_controllers:
            self.draw_text_on_canvas(controller)

    def draw_text_on_canvas(self, controller):
        """
        Draw a text object on the canvas (placeholder).
        
        Args:
            controller: The TextController to draw
        """
        # TODO: Convert PIL.Image to QPixmap and add to QGraphicsScene
        pass

    def clear_canvas(self):
        """Clear the canvas (placeholder)."""
        # TODO: Clear QGraphicsScene
        pass

    def update_ui_for_selection(self):
        """Update UI elements based on the current selection."""
        has_selection = self.current_controller is not None
        # Enable/disable formatting buttons
        self.main_window.btnBold.setEnabled(has_selection)
        self.main_window.btnItalic.setEnabled(has_selection)
        self.main_window.btnUnderline.setEnabled(has_selection)
        self.main_window.btnAlignLeft.setEnabled(has_selection)
        self.main_window.btnAlignCenter.setEnabled(has_selection)
        self.main_window.btnAlignRight.setEnabled(has_selection)
        self.main_window.btnTextColor.setEnabled(has_selection)
        self.main_window.fontComboBox.setEnabled(has_selection)

    def pil_image_to_qpixmap(self, pil_image):
        """
        Convert a PIL Image to a QPixmap for display in Qt widgets.
        
        Args:
            pil_image: PIL Image object
            
        Returns:
            QPixmap representation of the image
        """
        if pil_image.mode == "RGBA":
            qim = QImage(pil_image.tobytes("raw", "RGBA"), pil_image.width, pil_image.height, QImage.Format_RGBA8888)
        else:
            qim = QImage(pil_image.tobytes("raw", "RGB"), pil_image.width, pil_image.height, QImage.Format_RGB888)
        return QPixmap.fromImage(qim)