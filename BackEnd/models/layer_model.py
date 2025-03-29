# models/layer_model.py
from utils.geometry_utils import is_point_inside

class LayerModel:
    def __init__(self, obj, name=None):
        """Initialize a layer with an object and default properties."""
        self.id = id(self)  # Unique identifier for the layer
        self.object = obj  # Object inside the layer (ImageModel, ShapeModel, etc.)
        self.name = name if name else f"Layer {self.id}"  # Layer name
        self.x = 0  # X-coordinate on canvas
        self.y = 0  # Y-coordinate on canvas
        self.width = obj.width if hasattr(obj, 'width') else 100  # Width of the layer
        self.height = obj.height if hasattr(obj, 'height') else 100  # Height of the layer
        self.rotation = 0  # Rotation angle in degrees
        self.visible = True  # Visibility state
        self.locked = False  # Lock state (if locked, cannot be edited)
        self.order = 0  # Order for rendering (higher order = drawn on top)
        self.selected = False  # Selection state
        self.dragging = False  # Dragging state

    def move(self, dx, dy):
        """Move the layer by a specified offset."""
        self.x += dx
        self.y += dy

    def rotate(self, angle):
        """Rotate the layer by a specified angle."""
        self.rotation = (self.rotation + angle) % 360

    def resize(self, width, height, x=None, y=None):
        """Resize the layer to new dimensions, optionally updating position."""
        self.width = max(20, width)  # Enforce minimum width
        self.height = max(20, height)  # Enforce minimum height
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    def is_point_inside(self, mouse_x, mouse_y):
        """Check if a point is inside the layer, accounting for rotation."""
        return is_point_inside(self.x, self.y, self.width, self.height, self.rotation, mouse_x, mouse_y)