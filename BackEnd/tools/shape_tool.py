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
            "star": self._draw_star,  
            "outline_star": self._draw_outline_star,  
            "heart": self._draw_heart,  
            "outline_heart": self._draw_outline_heart, 
            "polygon": self._draw_polygon,  
            "outline_polygon": self._draw_outline_polygon,
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

    # Draw a filled star
    def _draw_star(self, surface, line_color, line_thickness, fill_color, border_radius):
        center_x, center_y = surface.get_width() // 2, surface.get_height() // 2
        outer_radius = min(surface.get_width(), surface.get_height()) // 2
        inner_radius = outer_radius // 2
        points = []
        for i in range(10):
            angle = math.radians(i * 36)
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        if fill_color:
            pygame.draw.polygon(surface, fill_color, points)
        pygame.draw.polygon(surface, line_color, points, line_thickness)

    # Draw an outline-only star
    def _draw_outline_star(self, surface, line_color, line_thickness, fill_color, border_radius):
        
        center_x, center_y = surface.get_width() // 2, surface.get_height() // 2
        outer_radius = min(surface.get_width(), surface.get_height()) // 2
        inner_radius = outer_radius // 2
        points = []
        for i in range(10):
            angle = math.radians(i * 36)
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(surface, line_color, points, line_thickness)

    # Draw a filled heart.
    def _draw_heart(self, surface, line_color, line_thickness, fill_color, border_radius):
        width, height = surface.get_width(), surface.get_height()
        points = []
        for t in range(0, 360, 5):
            t_rad = math.radians(t)
            x = width // 2 + 16 * (math.sin(t_rad) ** 3) * (width / 100)
            y = height // 2 - (13 * math.cos(t_rad) - 5 * math.cos(2 * t_rad) - 2 * math.cos(3 * t_rad) - math.cos(4 * t_rad)) * (height / 100)
            points.append((x, y))
        if fill_color:
            pygame.draw.polygon(surface, fill_color, points)
        pygame.draw.polygon(surface, line_color, points, line_thickness)

    # Draw an outline-only heart
    def _draw_outline_heart(self, surface, line_color, line_thickness, fill_color, border_radius):
        width, height = surface.get_width(), surface.get_height()
        points = []
        for t in range(0, 360, 5):
            t_rad = math.radians(t)
            x = width // 2 + 16 * (math.sin(t_rad) ** 3) * (width / 100)
            y = height // 2 - (13 * math.cos(t_rad) - 5 * math.cos(2 * t_rad) - 2 * math.cos(3 * t_rad) - math.cos(4 * t_rad)) * (height / 100)
            points.append((x, y))
        pygame.draw.polygon(surface, line_color, points, line_thickness)

    # Draw a filled polygon (hexagon)
    def _draw_polygon(self, surface, line_color, line_thickness, fill_color, border_radius):
        center_x, center_y = surface.get_width() // 2, surface.get_height() // 2
        radius = min(surface.get_width(), surface.get_height()) // 2
        points = []
        for i in range(6):
            angle = math.radians(i * 60)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        if fill_color:
            pygame.draw.polygon(surface, fill_color, points)
        pygame.draw.polygon(surface, line_color, points, line_thickness)

    # Draw an outline-only polygon (hexagon).
    def _draw_outline_polygon(self, surface, line_color, line_thickness, fill_color, border_radius):
        center_x, center_y = surface.get_width() // 2, surface.get_height() // 2
        radius = min(surface.get_width(), surface.get_height()) // 2
        points = []
        for i in range(6):
            angle = math.radians(i * 60)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(surface, line_color, points, line_thickness)