# tools/shape_tool.py
import pygame
import math

# Class to handle drawing various shapes on a surface
class ShapeTool:
    # Initialize with a dictionary of shape drawing handlers
    def __init__(self):
        self._draw_handlers = {
            "square": self._draw_square,
            "outline_square": self._draw_outline_square,
            "circle": self._draw_circle,
            "outline_circle": self._draw_outline_circle,
            "triangle": self._draw_triangle,
            "outline_triangle": self._draw_outline_triangle,
            "line": self._draw_line,
        }
    
    # Draw a shape on the given surface with specified properties
    def draw(self, surface, shape_type, width, height, line_color, line_thickness, fill_color=None, border_radius=0, alpha=255, rotation=0):
        temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a temporary surface with alpha support
        temp_surface.set_alpha(alpha)  # Set transparency level

        handler = self._draw_handlers.get(shape_type)  # Get the appropriate drawing handler
        if handler:
            handler(temp_surface, line_color, line_thickness, fill_color, border_radius)  # Call the handler to draw

        rotated_surface = pygame.transform.rotate(temp_surface, rotation)  # Rotate the drawn shape
        surface.blit(rotated_surface, (0, 0))  # Draw the rotated shape onto the main surface

    # Draw a filled square with an optional border
    def _draw_square(self, surface, line_color, line_thickness, fill_color, border_radius):
        if fill_color:
            pygame.draw.rect(surface, fill_color, (0, 0, surface.get_width(), surface.get_height()), 0, border_radius)
        pygame.draw.rect(surface, line_color, (0, 0, surface.get_width(), surface.get_height()), line_thickness, border_radius)

    # Draw an outline-only square
    def _draw_outline_square(self, surface, line_color, line_thickness, fill_color, border_radius):
        pygame.draw.rect(surface, line_color, (0, 0, surface.get_width(), surface.get_height()), line_thickness, border_radius)

    # Draw a filled circle with an optional border
    def _draw_circle(self, surface, line_color, line_thickness, fill_color, border_radius):
        center = (surface.get_width() // 2, surface.get_height() // 2)
        radius = min(surface.get_width(), surface.get_height()) // 2
        if fill_color:
            pygame.draw.circle(surface, fill_color, center, radius)
        pygame.draw.circle(surface, line_color, center, radius, line_thickness)

    # Draw an outline-only circle
    def _draw_outline_circle(self, surface, line_color, line_thickness, fill_color, border_radius):
        center = (surface.get_width() // 2, surface.get_height() // 2)
        radius = min(surface.get_width(), surface.get_height()) // 2
        pygame.draw.circle(surface, line_color, center, radius, line_thickness)

    # Draw a filled triangle with an optional border
    def _draw_triangle(self, surface, line_color, line_thickness, fill_color, border_radius):
        points = [(surface.get_width() // 2, 0), (0, surface.get_height()), (surface.get_width(), surface.get_height())]
        if fill_color:
            pygame.draw.polygon(surface, fill_color, points)
        pygame.draw.polygon(surface, line_color, points, line_thickness)

    # Draw an outline-only triangle
    def _draw_outline_triangle(self, surface, line_color, line_thickness, fill_color, border_radius):
        points = [(surface.get_width() // 2, 0), (0, surface.get_height()), (surface.get_width(), surface.get_height())]
        pygame.draw.polygon(surface, line_color, points, line_thickness)

    # Draw a horizontal line
    def _draw_line(self, surface, line_color, line_thickness, fill_color, border_radius):
        start = (0, surface.get_height() // 2)
        end = (surface.get_width(), surface.get_height() // 2)
        pygame.draw.line(surface, line_color, start, end, line_thickness)