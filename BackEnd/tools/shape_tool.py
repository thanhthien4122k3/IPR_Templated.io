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

        self._draw_handlers = {
            "square": self._draw_square,
            "outline_square": self._draw_outline_square,
            "circle": self._draw_circle,
            "outline_circle": self._draw_outline_circle,
            "triangle": self._draw_triangle,
            "outline_triangle": self._draw_outline_triangle,
            "line": self._draw_line,
        }
    
    def draw(self, screen):
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        temp_surface.set_alpha(self.alpha)

        handler = self._draw_handlers.get(self.shape_type)
        if handler:
            handler(temp_surface)

        rotated_surface = pygame.transform.rotate(temp_surface, self.rotation)
        screen.blit(rotated_surface, (self.x, self.y))

    def _draw_square(self, surface):
        if self.fill_color:
            pygame.draw.rect(surface, self.fill_color, (0, 0, self.width, self.height), 0, self.border_radius)
        pygame.draw.rect(surface, self.line_color, (0, 0, self.width, self.height), self.line_thickness, self.border_radius)

    def _draw_outline_square(self, surface):
        pygame.draw.rect(surface, self.line_color, (0, 0, self.width, self.height), self.line_thickness, self.border_radius)

    def _draw_circle(self, surface):
        center = (self.width // 2, self.height // 2)
        radius = min(self.width, self.height) // 2
        if self.fill_color:
            pygame.draw.circle(surface, self.fill_color, center, radius)
        pygame.draw.circle(surface, self.line_color, center, radius, self.line_thickness)

    def _draw_outline_circle(self, surface):
        center = (self.width // 2, self.height // 2)
        radius = min(self.width, self.height) // 2
        pygame.draw.circle(surface, self.line_color, center, radius, self.line_thickness)

    def _draw_triangle(self, surface):
        points = [(self.width // 2, 0), (0, self.height), (self.width, self.height)]
        if self.fill_color:
            pygame.draw.polygon(surface, self.fill_color, points)
        pygame.draw.polygon(surface, self.line_color, points, self.line_thickness)

    def _draw_outline_triangle(self, surface):
        points = [(self.width // 2, 0), (0, self.height), (self.width, self.height)]
        pygame.draw.polygon(surface, self.line_color, points, self.line_thickness)

    def _draw_line(self, surface):
        start = (0, self.height // 2)
        end = (self.width, self.height // 2)
        pygame.draw.line(surface, self.line_color, start, end, self.line_thickness)

    def is_point_inside(self, mouse_x, mouse_y):
        local_x = mouse_x - self.x
        local_y = mouse_y - self.y
        angle_rad = math.radians(-self.rotation)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        rotated_x = local_x * cos_a + local_y * sin_a
        rotated_y = -local_x * sin_a + local_y * cos_a
        return 0 <= rotated_x <= self.width and 0 <= rotated_y <= self.height

    def is_point_inside(self, mouse_x, mouse_y):
        local_x = mouse_x - self.x
        local_y = mouse_y - self.y
        angle_rad = math.radians(-self.rotation)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        rotated_x = local_x * cos_a + local_y * sin_a
        rotated_y = -local_x * sin_a + local_y * cos_a
        return 0 <= rotated_x <= self.width and 0 <= rotated_y <= self.height