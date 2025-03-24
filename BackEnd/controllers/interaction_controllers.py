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

    # Check if mouse is near a border or corner of the object for resizing
    def is_near_border(self, mouse_x, mouse_y, obj):
        if not obj.selected:
            return False, None

        # Define border coordinates with a 5-pixel buffer around the object
        border_x = obj.x - 5
        border_y = obj.y - 5
        border_width = obj.width + 10
        border_height = obj.height + 10

        # Define corners for resizing
        corners = {
            "top-left": (border_x, border_y),
            "top-right": (border_x + border_width, border_y),
            "bottom-left": (border_x, border_y + border_height),
            "bottom-right": (border_x + border_width, border_y + border_height)
        }
        # Define edges for resizing
        edges = {
            "top": ((border_x, border_y), (border_x + border_width, border_y)),
            "left": ((border_x, border_y), (border_x, border_y + border_height)),
            "right": ((border_x + border_width, border_y), (border_x + border_width, border_y + border_height)),
            "bottom": ((border_x, border_y + border_height), (border_x + border_width, border_y + border_height))
        }

        # Check if mouse is near a corner (within 15 pixels)
        for corner_name, (corner_x, corner_y) in corners.items():
            distance = math.sqrt((mouse_x - corner_x) ** 2 + (mouse_y - corner_y) ** 2)
            if distance < 15:
                return True, corner_name

        # Check if mouse is near an edge (within 15 pixels)
        for edge_name, ((start_x, start_y), (end_x, end_y)) in edges.items():
            length = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
            if length == 0:
                continue
            t = max(0, min(1, ((mouse_x - start_x) * (end_x - start_x) + (mouse_y - start_y) * (end_y - start_y)) / (length ** 2)))
            proj_x = start_x + t * (end_x - start_x)
            proj_y = start_y + t * (end_y - start_y)
            distance = math.sqrt((mouse_x - proj_x) ** 2 + (mouse_y - proj_y) ** 2)
            if distance < 15:
                return True, edge_name

        return False, None

    # Handle mouse events for dragging, rotating, and resizing objects
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit the application
                pygame.quit()
                exit()

            mouse_x, mouse_y = pygame.mouse.get_pos()  # Get current mouse position

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click: Start dragging or resizing
                    for obj in reversed(self.objects):  # Check objects in reverse order (topmost first)
                        # Check if mouse is near a border for resizing
                        is_near, edge = self.is_near_border(mouse_x, mouse_y, obj)
                        if is_near:
                            self.selected_object = obj
                            self.resizing = True
                            self.resize_edge = edge
                            self.original_pos = (obj.x, obj.y)
                            self.original_size = (obj.width, obj.height)
                            break
                        # Check if mouse is inside object for dragging
                        elif obj.is_point_inside(mouse_x, mouse_y):
                            obj.selected = True
                            self.selected_object = obj
                            self.drag_offset = (mouse_x - obj.x, mouse_y - obj.y)
                            break
                    else:  # If no object is clicked, deselect current object
                        if self.selected_object:
                            self.selected_object.selected = False
                            self.selected_object = None
                elif event.button == 3:  # Right click: Start rotating
                    if self.selected_object:
                        self.rotating = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left release: Stop dragging or resizing
                    if self.selected_object:
                        self.selected_object.dragging = False
                        self.resizing = False
                elif event.button == 3:  # Right release: Stop rotating
                    self.rotating = False

            elif event.type == pygame.MOUSEMOTION:
                if self.selected_object:
                    if self.resizing:  # Resizing the object
                        # Calculate border coordinates
                        border_x = self.selected_object.x - 5
                        border_y = self.selected_object.y - 5
                        # Adjust size and position based on the resize edge
                        if self.resize_edge == "top-left":
                            self.selected_object.width = self.original_size[0] + (self.original_pos[0] - mouse_x + 5)
                            self.selected_object.height = self.original_size[1] + (self.original_pos[1] - mouse_y + 5)
                            self.selected_object.x = mouse_x - 5
                            self.selected_object.y = mouse_y - 5
                        elif self.resize_edge == "top-right":
                            self.selected_object.width = mouse_x - border_x - 5
                            self.selected_object.height = self.original_size[1] + (self.original_pos[1] - mouse_y + 5)
                            self.selected_object.y = mouse_y - 5
                        elif self.resize_edge == "bottom-left":
                            self.selected_object.width = self.original_size[0] + (self.original_pos[0] - mouse_x + 5)
                            self.selected_object.height = mouse_y - border_y - 5
                            self.selected_object.x = mouse_x - 5
                        elif self.resize_edge == "bottom-right":
                            self.selected_object.width = mouse_x - border_x - 5
                            self.selected_object.height = mouse_y - border_y - 5
                        elif self.resize_edge == "top":
                            self.selected_object.height = self.original_size[1] + (self.original_pos[1] - mouse_y + 5)
                            self.selected_object.y = mouse_y - 5
                        elif self.resize_edge == "bottom":
                            self.selected_object.height = mouse_y - border_y - 5
                        elif self.resize_edge == "left":
                            self.selected_object.width = self.original_size[0] + (self.original_pos[0] - mouse_x + 5)
                            self.selected_object.x = mouse_x - 5
                        elif self.resize_edge == "right":
                            self.selected_object.width = mouse_x - border_x - 5

                        # Enforce minimum size constraints
                        if self.selected_object.width < 20:
                            self.selected_object.width = 20
                            if self.resize_edge in ["top-left", "bottom-left", "left"]:
                                self.selected_object.x = self.original_pos[0] + self.original_size[0] - 15
                        if self.selected_object.height < 20:
                            self.selected_object.height = 20
                            if self.resize_edge in ["top-left", "top-right", "top"]:
                                self.selected_object.y = self.original_pos[1] + self.original_size[1] - 15

                    elif event.buttons[0]:  # Dragging with left button
                        self.selected_object.dragging = True
                        new_x = mouse_x - self.drag_offset[0]
                        new_y = mouse_y - self.drag_offset[1]
                        self.selected_object.move(new_x - self.selected_object.x, new_y - self.selected_object.y)
                    elif self.rotating:  # Rotating with right button
                        center_x = self.selected_object.x + self.selected_object.width // 2
                        center_y = self.selected_object.y + self.selected_object.height // 2
                        dx = mouse_x - center_x
                        dy = mouse_y - center_y
                        angle = math.degrees(math.atan2(dy, dx))
                        self.selected_object.rotate(angle - self.selected_object.rotation)