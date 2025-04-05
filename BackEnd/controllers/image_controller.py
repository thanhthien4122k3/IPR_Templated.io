import pygame
from PIL import Image
from models.image_model import ImageModel
from tools.image_tool import ImageTool

class ImageController:
    def __init__(self):
        """
        Initialize the controller with an empty list of image models
        """
        self._image_models = []  # List to store all image models
        self._active_model = None  # The currently selected active image model
        self._image_tool = None  # The image tool for editing images
    
    def create_image_model(self, file_path, x=0, y=0):
        """
        Create and add a new image model to the controller.
        
        Args:
            file_path (str): Path to the image file
            x (int): Initial x position for the image
            y (int): Initial y position for the image
        """
        image_model = ImageModel(file_path, x, y)
        self._image_models.append(image_model)
        return image_model
    
    def select_image_model(self, mouse_x, mouse_y):
        """
        Select an image model based on the mouse coordinates.
        
        Args:
            mouse_x (int): X-coordinate of the mouse
            mouse_y (int): Y-coordinate of the mouse
        
        Returns:
            ImageModel: The selected image model, or None if no model is selected
        """
        for model in reversed(self._image_models):
            if model.is_point_inside(mouse_x, mouse_y):
                if self._active_model:
                    self._active_model.selected = False  # Deselect previous model
                model.selected = True
                self._active_model = model
                return model
        if self._active_model:
            self._active_model.selected = False
            self._active_model = None
        return None
    
    def move_active_model(self, dx, dy):
        """
        Move the currently active image model by dx, dy.
        
        Args:
            dx (int): Change in x position
            dy (int): Change in y position
        """
        if self._active_model:
            self._active_model.move(dx, dy)
    
    def rotate_active_model(self, angle):
        """
        Rotate the currently active image model by a given angle.
        
        Args:
            angle (int): Rotation angle in degrees
        """
        if self._active_model:
            self._active_model.rotate(angle)
    
    def flip_active_model_horizontal(self):
        """Flip the currently active image model horizontally."""
        if self._active_model:
            self._active_model.image = pygame.transform.flip(self._active_model.image, True, False)
    
    def flip_active_model_vertical(self):
        """Flip the currently active image model vertically."""
        if self._active_model:
            self._active_model.image = pygame.transform.flip(self._active_model.image, False, True)
    
    def add_image_tool(self, x, y, width, height):
        """
        Create and assign an ImageTool for editing the image.
        
        Args:
            x (int): X-coordinate for the tool
            y (int): Y-coordinate for the tool
            width (int): Width of the tool's area
            height (int): Height of the tool's area
        """
        self._image_tool = ImageTool(x, y, width, height)
    
    def apply_image_tool_action(self, action, *args):
        """
        Apply a specific image tool action like flipping, rotating, etc.
        
        Args:
            action (str): The action to perform (flip, rotate, etc.)
            *args: Additional arguments for the action (e.g., angle for rotate)
        """
        if self._image_tool:
            if action == "flip_horizontal":
                self._image_tool.flip_horizontal()
            elif action == "flip_vertical":
                self._image_tool.flip_vertical()
            elif action == "rotate":
                angle = args[0] if args else 0
                self._image_tool.rotate(angle)
            elif action == "round_corners":
                radius = args[0] if args else 10
                self._image_tool.round_corners(radius)
            elif action == "add_border":
                border_size = args[0] if args else 10
                border_color = args[1] if len(args) > 1 else (0, 0, 0)
                self._image_tool.add_border(border_size, border_color)
            elif action == "adjust_transparency":
                alpha = args[0] if args else 255
                self._image_tool.adjust_transparency(alpha)
            elif action == "crop":
                box = args[0] if args else (0, 0, self._image_tool.width, self._image_tool.height)
                self._image_tool.crop(box)
    
    def reset_image_tool(self):
        """Reset the image tool to its original state."""
        if self._image_tool:
            self._image_tool.reset_to_original()

    def get_all_image_models(self):
        """Get all image models managed by the controller."""
        return self._image_models

    def get_active_image_model(self):
        """Get the currently active image model."""
        return self._active_model
    
    def remove_image_model(self, image_model):
        """
        Remove a specific image model from the controller.
        
        Args:
            image_model (ImageModel): The image model to remove
        """
        if image_model in self._image_models:
            self._image_models.remove(image_model)
            if self._active_model == image_model:
                self._active_model = None
