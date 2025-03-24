# models/shape_model.py

# Class to store and manage the state of a shape
class ShapeModel:
    # Initialize shape with type, position, size, and default properties
    def __init__(self, shape_type, x, y, width, height):
        self.shape_type = shape_type  # Type of shape (e.g., "square", "circle")
        self.x = x  # X-coordinate on canvas
        self.y = y  # Y-coordinate on canvas
        self.width = width  # Width of the shape
        self.height = height  # Height of the shape
        self.line_color = (0, 0, 0)  # Line color (default black)
        self.line_thickness = 2  # Line thickness
        self.fill_color = None  # Fill color (default none)
        self.border_radius = 0  # Border radius for rounded corners
        self.alpha = 255  # Transparency level (0-255)
        self.rotation = 0  # Rotation angle in degrees
        self.selected = False  # Flag to indicate if shape is selected
        self.dragging = False  # Flag to indicate if shape is being dragged

    # Move the shape by a specified offset
    def move(self, dx, dy):
        self.x += dx  # Update x-coordinate
        self.y += dy  # Update y-coordinate

    # Rotate the shape by a specified angle
    def rotate(self, angle):
        self.rotation = (self.rotation + angle) % 360  # Update rotation, keep within 0-359 degrees

    # Check if a point (mouse position) is inside the shape, accounting for rotation
    def is_point_inside(self, mouse_x, mouse_y):
        import math
        local_x = mouse_x - self.x  # Convert to local coordinates
        local_y = mouse_y - self.y
        angle_rad = math.radians(-self.rotation)  # Convert rotation to radians, negate it
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        rotated_x = local_x * cos_a + local_y * sin_a  # Rotate point to match shape orientation
        rotated_y = -local_x * sin_a + local_y * cos_a
        return 0 <= rotated_x <= self.width and 0 <= rotated_y <= self.height  # Check if point is within bounds