import copy
from PIL import Image, ImageOps, ImageDraw
from models.image_model import ImageModel

class ImageController:
    def __init__(self):
        """
        Initialize the image controller with an empty list of images
        """
        self.images = []  # List to store ImageModel instances
        self.selected_image = None  # Currently selected image
    
    def create_image(self, x, y, width, height):
        """
        Create a new image and add it to the controller
        
        Args:
            x (int): X-coordinate of the image
            y (int): Y-coordinate of the image
            width (int): Width of the image
            height (int): Height of the image
        
        Returns:
            ImageModel: The newly created image model
        """
        new_image = ImageModel(x, y, width, height)
        self.images.append(new_image)
        return new_image
    
    def delete_image(self, image):
        """
        Remove an image from the controller
        
        Args:
            image (ImageModel): The image to be deleted
        """
        if image in self.images:
            self.images.remove(image)
            if self.selected_image == image:
                self.selected_image = None
    
    def select_image(self, mouse_x, mouse_y):
        """
        Select an image at the given mouse coordinates
        
        Args:
            mouse_x (int): X-coordinate of mouse
            mouse_y (int): Y-coordinate of mouse
        
        Returns:
            ImageModel or None: The selected image, or None if no image is selected
        """
        # Reverse iteration to select top-most image in overlapping scenarios
        for image in reversed(self.images):
            if image.is_point_inside(mouse_x, mouse_y):
                # Deselect previous image
                if self.selected_image:
                    self.selected_image.selected = False
                
                # Select new image
                image.selected = True
                self.selected_image = image
                return image
        
        # Deselect if no image is found
        if self.selected_image:
            self.selected_image.selected = False
            self.selected_image = None
        
        return None
    
    def move_selected_image(self, dx, dy):
        """
        Move the currently selected image
        
        Args:
            dx (int): Change in x-coordinate
            dy (int): Change in y-coordinate
        """
        if self.selected_image:
            self.selected_image.move(dx, dy)
    
    def rotate_selected_image(self, angle):
        """
        Rotate the currently selected image
        
        Args:
            angle (int): Rotation angle in degrees
        """
        if self.selected_image:
            self.selected_image.rotate(angle)
    
    def apply_transformation(self, transformation_func):
        """
        Apply a custom transformation to the selected image
        
        Args:
            transformation_func (callable): A function that takes an ImageModel as an argument
        """
        if self.selected_image:
            transformation_func(self.selected_image)
    
    def get_images_at_point(self, mouse_x, mouse_y):
        """
        Get all images at a specific point
        
        Args:
            mouse_x (int): X-coordinate of mouse
            mouse_y (int): Y-coordinate of mouse
        
        Returns:
            list: List of images at the given point
        """
        return [image for image in self.images if image.is_point_inside(mouse_x, mouse_y)]
    
    def clear_all_images(self):
        """
        Remove all images from the controller
        """
        self.images.clear()
        self.selected_image = None
    
    def duplicate_selected_image(self):
        """
        Create a duplicate of the selected image
        
        Returns:
            ImageModel or None: The duplicated image, or None if no image is selected
        """
        if self.selected_image:
            # Create a new image with offset
            new_image = self.create_image(
                self.selected_image.x + 20,  # Slight offset
                self.selected_image.y + 20,
                self.selected_image.width,
                self.selected_image.height
            )
            
            # Copy image properties
            new_image.current_image = copy.deepcopy(self.selected_image.current_image)
            new_image.original_image = copy.deepcopy(self.selected_image.original_image)
            new_image.rotation = self.selected_image.rotation
            
            return new_image
        
        return None