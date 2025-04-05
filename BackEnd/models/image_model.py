
import pygame

class ImageModel:
    """Class representing an uploaded image as an editable object."""
    def __init__(self, file_path, x=0, y=0):
        # Load image from file path using Pygame for rendering compatibility
        self.image = pygame.image.load(file_path).convert_alpha()
        self.file_path = file_path  # Store file path for reference
        self.x = x  # Initial x position
        self.y = y  # Initial y position
        self.width, self.height = self.image.get_size()  # Get image dimensions
        self.rotation = 0  # Initial rotation angle (degrees)
        self.selected = False  # Selection state
        self.dragging = False  # Dragging state

    def move(self, dx, dy):
        """Move the image by dx, dy."""
        self.x += dx
        self.y += dy

    def rotate(self, angle):
        """Rotate the image by a given angle."""
        self.rotation = (self.rotation + angle) % 360

    def is_point_inside(self, mouse_x, mouse_y):
        """Check if a point is inside the image, accounting for rotation"""
        import math
        local_x = mouse_x - self.x  # Convert to local coordinates
        local_y = mouse_y - self.y
        angle_rad = math.radians(-self.rotation)  # Convert rotation to radians, negate it
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        rotated_x = local_x * cos_a + local_y * sin_a  # Rotate point to match image orientation
        rotated_y = -local_x * sin_a + local_y * cos_a
        return 0 <= rotated_x <= self.width and 0 <= rotated_y <= self.height  # Check if point is within bounds