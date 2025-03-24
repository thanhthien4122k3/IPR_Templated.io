import pygame
import math

# Class to handle user interactions (dragging, rotating, resizing) for various objects (shapes, text, images, etc.)
class InteractionController:
    def __init__(self, objects):
        self.objects = objects  # List of objects (ShapeModel, Text, Image, etc.)
        self.selected_object = None  # Currently selected object
        self.drag_offset = (0, 0)  # Offset between mouse and object position during drag
        self.rotating = False  # Flag to indicate rotation mode
        self.resizing = False  # Flag to indicate resizing mode
        self.resize_edge = None  # Edge or corner being resized
        self.original_pos = (0, 0)  # Original position before resizing
        self.original_size = (0, 0)  # Original size before resizing

    # Check if mouse is near a border or corner of an object for resizing
    def is_near_border(self, mouse_x, mouse_y, obj):
        # Return False if object is not selected
        if not obj.selected:
            return False, None

        # Define border coordinates with 5-pixel buffer
        border_x, border_y = obj.x - 5, obj.y - 5
        border_width, border_height = obj.width + 10, obj.height + 10

        # Define corners and edges for resizing
        corners = {
            "top-left": (border_x, border_y),
            "top-right": (border_x + border_width, border_y),
            "bottom-left": (border_x, border_y + border_height),
            "bottom-right": (border_x + border_width, border_y + border_height)
        }
        edges = {
            "top": ((border_x, border_y), (border_x + border_width, border_y)),
            "left": ((border_x, border_y), (border_x, border_y + border_height)),
            "right": ((border_x + border_width, border_y), (border_x + border_width, border_y + border_height)),
            "bottom": ((border_x, border_y + border_height), (border_x + border_width, border_y + border_height))
        }

        # Check proximity to corners (within 15 pixels)
        for name, (x, y) in corners.items():
            if math.sqrt((mouse_x - x) ** 2 + (mouse_y - y) ** 2) < 15:
                return True, name

        # Check proximity to edges (within 15 pixels)
        for name, ((start_x, start_y), (end_x, end_y)) in edges.items():
            length = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
            if length == 0:
                continue
            t = max(0, min(1, ((mouse_x - start_x) * (end_x - start_x) + (mouse_y - start_y) * (end_y - start_y)) / (length ** 2)))
            proj_x, proj_y = start_x + t * (end_x - start_x), start_y + t * (end_y - start_y)
            if math.sqrt((mouse_x - proj_x) ** 2 + (mouse_y - proj_y) ** 2) < 15:
                return True, name

        return False, None

    # Handle all mouse events for interaction
    def handle_events(self):
        # Process each event in the queue
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

    # Handle mouse button press events
    def _handle_mouse_button_down(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.button == 1:  # Left click: Trigger drag or resize
            self._process_left_click(mouse_x, mouse_y)
        elif event.button == 3 and self.selected_object:  # Right click: Start rotation
            self.rotating = True

    # Handle mouse button release events
    def _handle_mouse_button_up(self, event):
        if event.button == 1 and self.selected_object:  # Left release: Stop drag or resize
            self.selected_object.dragging = False
            self.resizing = False
        elif event.button == 3:  # Right release: Stop rotation
            self.rotating = False

    # Handle mouse movement events
    def _handle_mouse_motion(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if not self.selected_object:  # Exit if no object selected
            return
        if self.resizing:  # Process resizing if active
            self._process_resize(mouse_x, mouse_y)
        elif event.buttons[0]:  # Process dragging if left button pressed
            self._process_drag(mouse_x, mouse_y)
        elif self.rotating:  # Process rotation if active
            self._process_rotation(mouse_x, mouse_y)

    # Process left-click to start dragging or resizing
    def _process_left_click(self, mouse_x, mouse_y):
        for obj in reversed(self.objects):  # Check objects from topmost
            is_near, edge = self.is_near_border(mouse_x, mouse_y, obj)
            if is_near:  # Start resizing if near border
                self.selected_object = obj
                self.resizing = True
                self.resize_edge = edge
                self.original_pos = (obj.x, obj.y)
                self.original_size = (obj.width, obj.height)
                break
            elif obj.is_point_inside(mouse_x, mouse_y):  # Start dragging if inside object
                obj.selected = True
                self.selected_object = obj
                self.drag_offset = (mouse_x - obj.x, mouse_y - obj.y)
                break
        else:  # Deselect if no object clicked
            if self.selected_object:
                self.selected_object.selected = False
                self.selected_object = None

    # Process resizing based on mouse position
    def _process_resize(self, mouse_x, mouse_y):
        border_x, border_y = self.selected_object.x - 5, self.selected_object.y - 5
        resize_handlers = {
            "top-left": lambda: (
                setattr(self.selected_object, "width", self.original_size[0] + (self.original_pos[0] - mouse_x + 5)),
                setattr(self.selected_object, "height", self.original_size[1] + (self.original_pos[1] - mouse_y + 5)),
                setattr(self.selected_object, "x", mouse_x - 5),
                setattr(self.selected_object, "y", mouse_y - 5)
            ),
            "top-right": lambda: (
                setattr(self.selected_object, "width", mouse_x - border_x - 5),
                setattr(self.selected_object, "height", self.original_size[1] + (self.original_pos[1] - mouse_y + 5)),
                setattr(self.selected_object, "y", mouse_y - 5)
            ),
            "bottom-left": lambda: (
                setattr(self.selected_object, "width", self.original_size[0] + (self.original_pos[0] - mouse_x + 5)),
                setattr(self.selected_object, "height", mouse_y - border_y - 5),
                setattr(self.selected_object, "x", mouse_x - 5)
            ),
            "bottom-right": lambda: (
                setattr(self.selected_object, "width", mouse_x - border_x - 5),
                setattr(self.selected_object, "height", mouse_y - border_y - 5)
            ),
            "top": lambda: (
                setattr(self.selected_object, "height", self.original_size[1] + (self.original_pos[1] - mouse_y + 5)),
                setattr(self.selected_object, "y", mouse_y - 5)
            ),
            "bottom": lambda: setattr(self.selected_object, "height", mouse_y - border_y - 5),
            "left": lambda: (
                setattr(self.selected_object, "width", self.original_size[0] + (self.original_pos[0] - mouse_x + 5)),
                setattr(self.selected_object, "x", mouse_x - 5)
            ),
            "right": lambda: setattr(self.selected_object, "width", mouse_x - border_x - 5)
        }

        # Execute resizing handler based on edge
        handler = resize_handlers.get(self.resize_edge)
        if handler:
            handler()

        # Enforce minimum size constraints
        if self.selected_object.width < 20:
            self.selected_object.width = 20
            if self.resize_edge in ["top-left", "bottom-left", "left"]:
                self.selected_object.x = self.original_pos[0] + self.original_size[0] - 15
        if self.selected_object.height < 20:
            self.selected_object.height = 20
            if self.resize_edge in ["top-left", "top-right", "top"]:
                self.selected_object.y = self.original_pos[1] + self.original_size[1] - 15

    # Process dragging based on mouse position
    def _process_drag(self, mouse_x, mouse_y):
        self.selected_object.dragging = True
        new_x = mouse_x - self.drag_offset[0]
        new_y = mouse_y - self.drag_offset[1]
        self.selected_object.move(new_x - self.selected_object.x, new_y - self.selected_object.y)

    # Process rotation based on mouse position
    def _process_rotation(self, mouse_x, mouse_y):
        center_x = self.selected_object.x + self.selected_object.width // 2
        center_y = self.selected_object.y + self.selected_object.height // 2
        dx = mouse_x - center_x
        dy = mouse_y - center_y
        angle = math.degrees(math.atan2(dy, dx))
        self.selected_object.rotate(angle - self.selected_object.rotation)