# models/shape_model.py
class ShapeModel:
    def __init__(self, shape_type, width, height):
        """Initialize shape with type, size, and default properties."""
        self.shape_type = shape_type  # Type of shape (e.g., "square", "circle")
        self.width = width  # Initial width (used for rendering)
        self.height = height  # Initial height (used for rendering)
        self.line_color = (0, 0, 0)  # Line color (default black)
        self.line_thickness = 2  # Line thickness
        self.fill_color = None  # Fill color (default none)
        self.border_radius = 0  # Border radius for rounded corners
        self.alpha = 255  # Transparency level (0-255)