import os
import pygame
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QListWidgetItem
from PyQt6.QtGui import QPixmap, QIcon, QImage
from PyQt6.QtCore import Qt, QSize
from BackEnd.controllers.image_controller import ImageController
from BackEnd.controllers.upload_controller import UploadController

class ImageManager:
    """
    Class that connects the UI image-related elements with the backend ImageController and UploadController.
    Manages image uploads, displays, and transformations.
    """
    def __init__(self, main_window):
        """
        Initialize the image manager with connections to the UI elements.
        
        Args:
            main_window: The main editor window instance with UI elements
        """
        self.main_window = main_window
        self.image_controller = ImageController()
        self.upload_controller = UploadController()
        
        # Setup image directory for storing uploaded images
        self.image_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "BackEnd", "assets", "images")
        os.makedirs(self.image_dir, exist_ok=True)
        
        # Track current canvas size
        self.canvas_width = self.main_window.canvasFrame.width() - 20  # Adjust for margins
        self.canvas_height = self.main_window.canvasFrame.height() - 20
        
        # Setup current transformation parameters
        self.current_rotation = 0
        self.currently_selected_image = None
        
        # Connect signals
        self.setup_connections()

    def setup_connections(self):
        """Connect UI signals to functions."""
        # Image page buttons
        self.main_window.uploadImageButton.clicked.connect(self.upload_image)
        self.main_window.btnImages.clicked.connect(self.activate_image_mode)
        self.main_window.imagesList.itemDoubleClicked.connect(self.add_image_to_canvas)
        
        # Upload page buttons
        self.main_window.chooseFileButton.clicked.connect(self.choose_file)
        self.main_window.uploadButton.clicked.connect(self.upload_from_list)
        self.main_window.uploadedFilesList.itemClicked.connect(self.select_image_from_list)
        
        # Zoom controls
        self.main_window.sliderZoom.valueChanged.connect(self.handle_zoom_change)
        self.main_window.btnZoomIn.clicked.connect(self.zoom_in)
        self.main_window.btnZoomOut.clicked.connect(self.zoom_out)
        
        # Canvas interaction
        self.main_window.canvasFrame.mousePressEvent = self.canvas_mouse_press

    def activate_image_mode(self):
        """Activate the image editing mode and switch to pageImages."""
        self.main_window.toolsStackedWidget.setCurrentWidget(self.main_window.pageImages)
        self.main_window.btnText.setChecked(False)
        self.main_window.btnShapes.setChecked(False)
        self.main_window.btnUpload.setChecked(False)
        self.main_window.btnImages.setChecked(True)
        self.refresh_image_list()

    def activate_upload_mode(self):
        """Activate the upload mode and switch to pageUpload."""
        self.main_window.toolsStackedWidget.setCurrentWidget(self.main_window.pageUpload)
        self.main_window.btnText.setChecked(False)
        self.main_window.btnShapes.setChecked(False)
        self.main_window.btnImages.setChecked(False)
        self.main_window.btnUpload.setChecked(True)

    def choose_file(self):
        """Open a file dialog to choose an image file and add it to uploadedFilesList."""
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Choose Image File",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            try:
                # Add file path to uploadedFilesList
                item = QListWidgetItem(os.path.basename(file_path))
                item.setData(Qt.UserRole, file_path)
                self.main_window.uploadedFilesList.addItem(item)
                print(f"Selected file: {file_path}")
            except Exception as e:
                QMessageBox.critical(self.main_window, "Error", f"Failed to select file: {str(e)}")

    def upload_from_list(self):
        """Upload the selected image from uploadedFilesList."""
        selected_items = self.main_window.uploadedFilesList.selectedItems()
        if selected_items:
            file_path = selected_items[0].data(Qt.UserRole)
            self.upload_image(file_path)

    def upload_image(self, file_path=None):
        """
        Upload an image using UploadController and add it to imagesList.
        
        Args:
            file_path (str, optional): Path to the image file. If None, open file dialog.
        """
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self.main_window,
                "Open Image",
                "",
                "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
            )
        
        if file_path:
            try:
                # Use UploadController to load the image
                self.upload_controller.upload_image(file_path)
                
                if self.upload_controller.is_loaded():
                    # Copy the image to the assets directory with a unique name
                    file_name = os.path.basename(file_path)
                    base_name, ext = os.path.splitext(file_name)
                    dest_path = os.path.join(self.image_dir, f"{base_name}_{os.path.getmtime(file_path):.0f}{ext}")
                    
                    # Save the uploaded image to assets
                    if not os.path.exists(dest_path):
                        pil_image = self.upload_controller.get_image()
                        pil_image.save(dest_path)
                    
                    # Add to imagesList
                    self.add_image_to_list(dest_path)
                    
                    # Show success message
                    QMessageBox.information(self.main_window, "Success", "Image uploaded successfully!")
                else:
                    QMessageBox.warning(self.main_window, "Warning", "Failed to load the image.")
                
            except Exception as e:
                QMessageBox.critical(self.main_window, "Error", f"Failed to upload image: {str(e)}")

    def add_image_to_list(self, image_path):
        """
        Add an image to the imagesList with a thumbnail.
        
        Args:
            image_path: Path to the image file
        """
        pixmap = QPixmap(image_path)
        thumbnail = pixmap.scaled(QSize(48, 48), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        item = QListWidgetItem(os.path.basename(image_path))
        item.setIcon(QIcon(thumbnail))
        item.setData(Qt.UserRole, image_path)
        
        self.main_window.imagesList.addItem(item)

    def refresh_image_list(self):
        """Refresh the imagesList from the assets directory."""
        self.main_window.imagesList.clear()
        
        if not os.path.exists(self.image_dir):
            return
            
        for file_name in os.listdir(self.image_dir):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(self.image_dir, file_name)
                self.add_image_to_list(image_path)

    def select_image_from_list(self, item):
        """
        Select an image from uploadedFilesList and add it to canvas.
        
        Args:
            item: The list item clicked
        """
        file_path = item.data(Qt.UserRole)
        try:
            self.upload_controller.upload_image(file_path)
            if self.upload_controller.is_loaded():
                center_x = self.canvas_width // 2
                center_y = self.canvas_height // 2
                image_model = self.image_controller.create_image_model(file_path, center_x, center_y)
                self.currently_selected_image = image_model
                self.image_controller.select_image_model(center_x, center_y)
                self.render_canvas()
                print(f"Selected image: {file_path}")
            else:
                QMessageBox.warning(self.main_window, "Warning", "Failed to load the image.")
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to select image: {str(e)}")

    def add_image_to_canvas(self, item):
        """
        Add the selected image to the canvas on double-click.
        
        Args:
            item: The list item double-clicked
        """
        image_path = item.data(Qt.UserRole)
        if not image_path or not os.path.exists(image_path):
            QMessageBox.warning(self.main_window, "Warning", "Image file not found.")
            return
            
        try:
            self.upload_controller.upload_image(image_path)
            if not self.upload_controller.is_loaded():
                QMessageBox.warning(self.main_window, "Warning", "Failed to load the image.")
                return
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Error loading image: {str(e)}")
            return
            
        center_x = self.canvas_width // 2
        center_y = self.canvas_height // 2
        
        image_model = self.image_controller.create_image_model(image_path, center_x, center_y)
        self.render_canvas()
        
        self.image_controller.select_image_model(center_x, center_y)
        self.currently_selected_image = image_model

    def render_canvas(self):
        """Render all images on the canvas (placeholder)."""
        # TODO: Implement with QGraphicsView
        self.clear_canvas()
        for image_model in self.image_controller.get_all_image_models():
            self.draw_image_on_canvas(image_model)

    def draw_image_on_canvas(self, image_model):
        """
        Draw an image model on the canvas (placeholder).
        
        Args:
            image_model: The image model to draw
        """
        # TODO: Convert pygame.Surface to QPixmap and add to QGraphicsScene
        pass

    def clear_canvas(self):
        """Clear the canvas (placeholder)."""
        # TODO: Clear QGraphicsScene
        pass

    def canvas_mouse_press(self, event):
        """
        Handle mouse press events on the canvas.
        
        Args:
            event: The mouse event
        """
        mouse_x = event.position().x()
        mouse_y = event.position().y()
        
        selected_model = self.image_controller.select_image_model(mouse_x, mouse_y)
        self.currently_selected_image = selected_model
        
        self.update_ui_for_selection()
        self.render_canvas()

    def update_ui_for_selection(self):
        """Update UI elements based on the current selection (placeholder)."""
        has_selection = self.currently_selected_image is not None
        # TODO: Enable/disable editing buttons when implemented

    def rotate_image(self, angle):
        """
        Rotate the currently selected image.
        
        Args:
            angle: Rotation angle in degrees
        """
        if self.currently_selected_image:
            self.image_controller.rotate_active_model(angle)
            self.current_rotation = (self.current_rotation + angle) % 360
            self.render_canvas()

    def flip_image_horizontal(self):
        """Flip the currently selected image horizontally."""
        if self.currently_selected_image:
            self.image_controller.flip_active_model_horizontal()
            self.render_canvas()

    def flip_image_vertical(self):
        """Flip the currently selected image vertically."""
        if self.currently_selected_image:
            self.image_controller.flip_active_model_vertical()
            self.render_canvas()

    def move_image(self, dx, dy):
        """
        Move the currently selected image.
        
        Args:
            dx: Change in x position
            dy: Change in y position
        """
        if self.currently_selected_image:
            self.image_controller.move_active_model(dx, dy)
            self.render_canvas()

    def delete_selected_image(self):
        """Delete the currently selected image from the canvas."""
        if self.currently_selected_image:
            self.image_controller.remove_image_model(self.currently_selected_image)
            self.currently_selected_image = None
            self.render_canvas()

    def apply_image_effect(self, effect_name, *args):
        """
        Apply an effect to the currently selected image.
        
        Args:
            effect_name: Name of the effect to apply
            *args: Additional arguments for the effect
        """
        if self.currently_selected_image:
            self.image_controller.apply_image_tool_action(effect_name, *args)
            self.render_canvas()

    def handle_zoom_change(self, zoom_value):
        """
        Handle changes to the zoom level.
        
        Args:
            zoom_value: The new zoom value (0-200)
        """
        scale_factor = zoom_value / 100.0
        # TODO: Apply scale_factor to QGraphicsView
        self.render_canvas()

    def zoom_in(self):
        """Increase zoom level."""
        current_value = self.main_window.sliderZoom.value()
        self.main_window.sliderZoom.setValue(min(current_value + 10, 200))

    def zoom_out(self):
        """Decrease zoom level."""
        current_value = self.main_window.sliderZoom.value()
        self.main_window.sliderZoom.setValue(max(current_value - 10, 0))

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

    def pygame_to_qpixmap(self, pygame_surface):
        """
        Convert a Pygame Surface to a QPixmap for display in Qt widgets.
        
        Args:
            pygame_surface: Pygame Surface object
            
        Returns:
            QPixmap representation of the surface
        """
        img_data = pygame.image.tostring(pygame_surface, "RGBA")
        width, height = pygame_surface.get_size()
        qimage = QImage(img_data, width, height, QImage.Format_RGBA8888)
        return QPixmap.fromImage(qimage)