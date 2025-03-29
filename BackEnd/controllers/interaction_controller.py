# controllers/interaction_controller.py
import pygame
import math
from utils.geometry_utils import is_near_border

class InteractionController:
    def __init__(self, layer_controller):
        """Initialize with a LayerController instead of a list of objects."""
        self.layer_controller = layer_controller  # Reference to LayerController
        self.selected_layer = None  # Currently selected layer
        self.drag_offset = (0, 0)  # Offset between mouse and layer position during drag
        self.rotating = False  # Flag to indicate rotation mode
        self.resizing = False  # Flag to indicate resizing mode
        self.resize_edge = None  # Edge or corner being resized
        self.original_pos = (0, 0)  # Original position before resizing
        self.original_size = (0, 0)  # Original size before resizing

    def is_near_border(self, mouse_x, mouse_y, layer):
        """Check if mouse is near a border or corner of a layer for resizing."""
        if not layer.selected:
            return False, None
        return is_near_border(layer.x, layer.y, layer.width, layer.height, mouse_x, mouse_y)

    def handle_events(self):
        """Handle mouse events for interaction."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close the application
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_button_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_button_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(event)

    def _handle_mouse_button_down(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.button == 1:  # Left click: Trigger drag or resize
            self._process_left_click(mouse_x, mouse_y)
        elif event.button == 3 and self.selected_layer:  # Right click: Start rotation
            self.rotating = True

    def _handle_mouse_button_up(self, event):
        if event.button == 1 and self.selected_layer:  # Left release: Stop drag or resize
            self.selected_layer.dragging = False
            self.resizing = False
        elif event.button == 3:  # Right release: Stop rotation
            self.rotating = False

    def _handle_mouse_motion(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if not self.selected_layer:  # Exit if no layer selected
            return
        if self.resizing:  # Process resizing if active
            self._process_resize(mouse_x, mouse_y)
        elif event.buttons[0]:  # Process dragging if left button pressed
            self._process_drag(mouse_x, mouse_y)
        elif self.rotating:  # Process rotation if active
            self._process_rotation(mouse_x, mouse_y)

    def _process_left_click(self, mouse_x, mouse_y):
        """Process left-click to start dragging or resizing."""
        # Use LayerController to select a layer
        self.selected_layer = self.layer_controller.select_layer_at_point(mouse_x, mouse_y)
        if self.selected_layer:
            is_near, edge = self.is_near_border(mouse_x, mouse_y, self.selected_layer)
            if is_near:  # Start resizing if near border
                self.resizing = True
                self.resize_edge = edge
                self.original_pos = (self.selected_layer.x, self.selected_layer.y)
                self.original_size = (self.selected_layer.width, self.selected_layer.height)
            else:  # Start dragging if inside layer
                self.drag_offset = (mouse_x - self.selected_layer.x, mouse_y - self.selected_layer.y)

    def _process_resize(self, mouse_x, mouse_y):
        """Process resizing based on mouse position."""
        border_x, border_y = self.selected_layer.x - 5, self.selected_layer.y - 5
        resize_handlers = {
            "top-left": lambda: (
                self.layer_controller.resize_layer(
                    self.selected_layer,
                    self.original_size[0] + (self.original_pos[0] - mouse_x + 5),
                    self.original_size[1] + (self.original_pos[1] - mouse_y + 5),
                    mouse_x - 5,
                    mouse_y - 5
                )
            ),
            "top-right": lambda: (
                self.layer_controller.resize_layer(
                    self.selected_layer,
                    mouse_x - border_x - 5,
                    self.original_size[1] + (self.original_pos[1] - mouse_y + 5),
                    None,
                    mouse_y - 5
                )
            ),
            "bottom-left": lambda: (
                self.layer_controller.resize_layer(
                    self.selected_layer,
                    self.original_size[0] + (self.original_pos[0] - mouse_x + 5),
                    mouse_y - border_y - 5,
                    mouse_x - 5,
                    None
                )
            ),
            "bottom-right": lambda: (
                self.layer_controller.resize_layer(
                    self.selected_layer,
                    mouse_x - border_x - 5,
                    mouse_y - border_y - 5
                )
            ),
            "top": lambda: (
                self.layer_controller.resize_layer(
                    self.selected_layer,
                    self.selected_layer.width,
                    self.original_size[1] + (self.original_pos[1] - mouse_y + 5),
                    None,
                    mouse_y - 5
                )
            ),
            "bottom": lambda: (
                self.layer_controller.resize_layer(
                    self.selected_layer,
                    self.selected_layer.width,
                    mouse_y - border_y - 5
                )
            ),
            "left": lambda: (
                self.layer_controller.resize_layer(
                    self.selected_layer,
                    self.original_size[0] + (self.original_pos[0] - mouse_x + 5),
                    self.selected_layer.height,
                    mouse_x - 5,
                    None
                )
            ),
            "right": lambda: (
                self.layer_controller.resize_layer(
                    self.selected_layer,
                    mouse_x - border_x - 5,
                    self.selected_layer.height
                )
            )
        }

        # Execute resizing handler based on edge
        handler = resize_handlers.get(self.resize_edge)
        if handler:
            handler()

    def _process_drag(self, mouse_x, mouse_y):
        """Process dragging based on mouse position."""
        self.selected_layer.dragging = True
        new_x = mouse_x - self.drag_offset[0]
        new_y = mouse_y - self.drag_offset[1]
        dx = new_x - self.selected_layer.x
        dy = new_y - self.selected_layer.y
        self.layer_controller.move_layer(self.selected_layer, dx, dy)

    def _process_rotation(self, mouse_x, mouse_y):
        """Process rotation based on mouse position."""
        center_x = self.selected_layer.x + self.selected_layer.width // 2
        center_y = self.selected_layer.y + self.selected_layer.height // 2
        dx = mouse_x - center_x
        dy = mouse_y - center_y
        angle = math.degrees(math.atan2(dy, dx))
        self.layer_controller.rotate_layer(self.selected_layer, angle - self.selected_layer.rotation)