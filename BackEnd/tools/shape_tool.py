# tools/shape_tool.py
import pygame
import math

class ShapeTool:
    def __init__(self, shape_type, x, y, width, height):
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.line_color = (0, 0, 0)  # BLACK
        self.line_thickness = 2
        self.fill_color = None
        self.border_radius = 0
        self.alpha = 255
        self.rotation = 0

    def draw(self, screen):
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        temp_surface.set_alpha(self.alpha)

        if self.shape_type == "square":
            if self.fill_color:
                pygame.draw.rect(temp_surface, self.fill_color, (0, 0, self.width, self.height), 0, self.border_radius)
            pygame.draw.rect(temp_surface, self.line_color, (0, 0, self.width, self.height), self.line_thickness, self.border_radius)
        # Tương tự cho các loại hình khác: circle, triangle, line...
        elif self.shape_type == "outline_square":
            pygame.draw.rect(temp_surface, self.line_color, (0, 0, self.width, self.height), self.line_thickness, self.border_radius)

        elif self.shape_type == "circle":
            if self.fill_color:
                pygame.draw.circle(temp_surface, self.fill_color, (self.width // 2, self.height // 2), min(self.width, self.height) // 2)
            pygame.draw.circle(temp_surface, self.line_color, (self.width // 2, self.height // 2), min(self.width, self.height) // 2, self.line_thickness)

        elif self.shape_type == "outline_circle":
            pygame.draw.circle(temp_surface, self.line_color, (self.width // 2, self.height // 2), min(self.width, self.height) // 2, self.line_thickness)

        elif self.shape_type == "triangle":
            points = [(self.width // 2, 0), (0, self.height), (self.width, self.height)]
            if self.fill_color:
                pygame.draw.polygon(temp_surface, self.fill_color, points)
            pygame.draw.polygon(temp_surface, self.line_color, points, self.line_thickness)

        elif self.shape_type == "outline_triangle":
            points = [(self.width // 2, 0), (0, self.height), (self.width, self.height)]
            pygame.draw.polygon(temp_surface, self.line_color, points, self.line_thickness)

        elif self.shape_type == "line":
            start_x, start_y = 0, self.height // 2
            end_x, end_y = self.width, self.height // 2
        pygame.draw.line(temp_surface, self.line_color, (start_x, start_y), (end_x, end_y), self.line_thickness)
         
        rotated_surface = pygame.transform.rotate(temp_surface, self.rotation)
        screen.blit(rotated_surface, (self.x, self.y))

    def is_point_inside(self, mouse_x, mouse_y):
        local_x = mouse_x - self.x
        local_y = mouse_y - self.y
        angle_rad = math.radians(-self.rotation)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        rotated_x = local_x * cos_a + local_y * sin_a
        rotated_y = -local_x * sin_a + local_y * cos_a
        return 0 <= rotated_x <= self.width and 0 <= rotated_y <= self.height