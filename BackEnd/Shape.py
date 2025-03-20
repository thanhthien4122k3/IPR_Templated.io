import pygame
import sys
import math

# Khởi tạo Pygame
pygame.init()

# Cài đặt kích thước khung chỉnh sửa
WIDTH, HEIGHT = 1000, 700
TOOLBAR_WIDTH = 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Image Editor - Shape Manipulation with UI")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)

# Font chữ
font = pygame.font.Font(None, 24)

# Lớp Button
class Button:
    def __init__(self, x, y, width, height, text, color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Lớp Shape
class Shape:
    def __init__(self, shape_type, x, y, width, height):
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.line_color = BLACK
        self.line_thickness = 2
        self.fill_color = None
        self.border_radius = 0
        self.alpha = 255
        self.selected = False
        self.resizing = False
        self.dragging = False
        self.rotation = 0
        self.resize_start = None
        self.resize_edge = None
        self.original_pos = (0, 0)
        self.original_size = (0, 0)

    def draw(self, screen):
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        temp_surface.set_alpha(self.alpha)

        rotated_surface = pygame.transform.rotate(temp_surface, self.rotation)
        rotated_rect = rotated_surface.get_rect(center=(self.width // 2, self.height // 2))

        if self.shape_type == "square":
            if self.fill_color:
                pygame.draw.rect(temp_surface, self.fill_color, (0, 0, self.width, self.height), 0, self.border_radius)
            pygame.draw.rect(temp_surface, self.line_color, (0, 0, self.width, self.height), self.line_thickness, self.border_radius)
        
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

        rotated_surface.blit(temp_surface, rotated_rect)
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

# Lớp Editor
class Editor:
    def __init__(self):
        self.shapes = []
        self.current_shape_type = "square"
        self.buttons = [
            Button(10, 10, 180, 40, "Add Square", LIGHT_GRAY, lambda: self.add_shape("square", 250, 100, 100, 100)),
            Button(10, 60, 180, 40, "Add Outline Square", LIGHT_GRAY, lambda: self.add_shape("outline_square", 250, 100, 100, 100)),
            Button(10, 110, 180, 40, "Add Circle", LIGHT_GRAY, lambda: self.add_shape("circle", 250, 100, 100, 100)),
            Button(10, 160, 180, 40, "Add Outline Circle", LIGHT_GRAY, lambda: self.add_shape("outline_circle", 250, 100, 100, 100)),
            Button(10, 210, 180, 40, "Add Triangle", LIGHT_GRAY, lambda: self.add_shape("triangle", 250, 100, 100, 100)),
            Button(10, 260, 180, 40, "Add Outline Triangle", LIGHT_GRAY, lambda: self.add_shape("outline_triangle", 250, 100, 100, 100)),
            Button(10, 310, 180, 40, "Add Line", LIGHT_GRAY, lambda: self.add_shape("line", 250, 100, 100, 20)),
            Button(10, 360, 180, 40, "Thicker Line", LIGHT_GRAY, lambda: self.set_selected_property("line_thickness", None, 1)),
            Button(10, 410, 180, 40, "Thinner Line", LIGHT_GRAY, lambda: self.set_selected_property("line_thickness", None, -1)),
            Button(10, 460, 180, 40, "More Transparent", LIGHT_GRAY, lambda: self.set_selected_property("alpha", None, -20)),
            Button(10, 510, 180, 40, "Less Transparent", LIGHT_GRAY, lambda: self.set_selected_property("alpha", None, 20)),
            Button(10, 560, 180, 40, "Increase Border Radius", LIGHT_GRAY, lambda: self.set_selected_property("border_radius", None, 5)),
            Button(10, 610, 180, 40, "Decrease Border Radius", LIGHT_GRAY, lambda: self.set_selected_property("border_radius", None, -5)),
        ]

    def add_shape(self, shape_type, x, y, width, height):
        shape = Shape(shape_type, x, y, width, height)
        self.shapes.append(shape)

    def set_selected_property(self, property_name, value=None, delta=None):
        selected_shape = next((shape for shape in self.shapes if shape.selected), None)
        if selected_shape:
            if property_name == "line_color":
                selected_shape.line_color = value
            elif property_name == "line_thickness":
                selected_shape.line_thickness = max(1, min(10, selected_shape.line_thickness + delta))
            elif property_name == "fill_color":
                selected_shape.fill_color = value
            elif property_name == "alpha":
                selected_shape.alpha = max(0, min(255, selected_shape.alpha + delta))
            elif property_name == "border_radius":
                selected_shape.border_radius = max(0, min(50, selected_shape.border_radius + delta))

    def is_near_border(self, mouse_x, mouse_y, shape):
        if not shape.selected:
            return False, (0, 0), None

        # Định nghĩa tọa độ và cạnh của đường viền
        border_x = shape.x - 5  # Thêm khoảng cách 5 pixel xung quanh hình
        border_y = shape.y - 5
        border_width = shape.width + 10
        border_height = shape.height + 10

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

        for corner_name, (corner_x, corner_y) in corners.items():
            distance = math.sqrt((mouse_x - corner_x) ** 2 + (mouse_y - corner_y) ** 2)
            if distance < 15:
                return True, (corner_x, corner_y), corner_name

        for edge_name, ((start_x, start_y), (end_x, end_y)) in edges.items():
            length = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
            if length == 0:
                continue
            t = max(0, min(1, ((mouse_x - start_x) * (end_x - start_x) + (mouse_y - start_y) * (end_y - start_y)) / (length ** 2)))
            proj_x = start_x + t * (end_x - start_x)
            proj_y = start_y + t * (end_y - start_y)
            distance = math.sqrt((mouse_x - proj_x) ** 2 + (mouse_y - proj_y) ** 2)
            if distance < 15:
                return True, (proj_x, proj_y), edge_name

        return False, (0, 0), None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            mouse_x, mouse_y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button.is_clicked((mouse_x, mouse_y)):
                        if button.action:
                            button.action()
                        break
                else:
                    if mouse_x > TOOLBAR_WIDTH:
                        for shape in reversed(self.shapes):
                            # Kiểm tra kéo cạnh/góc của đường viền
                            is_near, resize_point, edge = self.is_near_border(mouse_x, mouse_y, shape)
                            if is_near:
                                shape.resizing = True
                                shape.resize_start = resize_point
                                shape.resize_edge = edge
                                shape.original_pos = (shape.x, shape.y)
                                shape.original_size = (shape.width, shape.height)
                                break
                            # Kiểm tra di chuyển hình khối
                            elif shape.is_point_inside(mouse_x, mouse_y):
                                shape.selected = True
                                shape.dragging = True
                                shape.mouse_offset = (mouse_x - shape.x, mouse_y - shape.y)
                                break
                            else:
                                shape.selected = False

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for shape in self.shapes:
                    shape.dragging = False
                    shape.resizing = False

            if event.type == pygame.MOUSEMOTION:
                for shape in self.shapes:
                    if shape.dragging:
                        shape.x = mouse_x - shape.mouse_offset[0]
                        shape.y = mouse_y - shape.mouse_offset[1]
                        shape.x = max(TOOLBAR_WIDTH, shape.x)
                    elif shape.resizing:
                        # Tính toán dựa trên vị trí đường viền
                        border_x = shape.x - 5
                        border_y = shape.y - 5
                        if shape.resize_edge == "top-left":
                            shape.width = shape.original_size[0] + (shape.original_pos[0] - mouse_x + 5)
                            shape.height = shape.original_size[1] + (shape.original_pos[1] - mouse_y + 5)
                            shape.x = mouse_x - 5
                            shape.y = mouse_y - 5
                        elif shape.resize_edge == "top-right":
                            shape.width = mouse_x - border_x - 5
                            shape.height = shape.original_size[1] + (shape.original_pos[1] - mouse_y + 5)
                            shape.y = mouse_y - 5
                        elif shape.resize_edge == "bottom-left":
                            shape.width = shape.original_size[0] + (shape.original_pos[0] - mouse_x + 5)
                            shape.height = mouse_y - border_y - 5
                            shape.x = mouse_x - 5
                        elif shape.resize_edge == "bottom-right":
                            shape.width = mouse_x - border_x - 5
                            shape.height = mouse_y - border_y - 5
                        elif shape.resize_edge == "top":
                            shape.height = shape.original_size[1] + (shape.original_pos[1] - mouse_y + 5)
                            shape.y = mouse_y - 5
                        elif shape.resize_edge == "bottom":
                            shape.height = mouse_y - border_y - 5
                        elif shape.resize_edge == "left":
                            shape.width = shape.original_size[0] + (shape.original_pos[0] - mouse_x + 5)
                            shape.x = mouse_x - 5
                        elif shape.resize_edge == "right":
                            shape.width = mouse_x - border_x - 5

                        if shape.width < 20:
                            shape.width = 20
                            if shape.resize_edge in ["top-left", "bottom-left", "left"]:
                                shape.x = shape.original_pos[0] + shape.original_size[0] - 15
                        if shape.height < 20:
                            shape.height = 20
                            if shape.resize_edge in ["top-left", "top-right", "top"]:
                                shape.y = shape.original_pos[1] + shape.original_size[1] - 15

    def draw(self, screen):
        screen.fill(WHITE)
        pygame.draw.rect(screen, GRAY, (0, 0, TOOLBAR_WIDTH, HEIGHT))
        for button in self.buttons:
            button.draw(screen)
        for shape in self.shapes:
            shape.draw(screen)
            if shape.selected:
                # Vẽ đường viền bao quanh hình khối
                border_x = shape.x - 5
                border_y = shape.y - 5
                border_width = shape.width + 10
                border_height = shape.height + 10
                pygame.draw.rect(screen, BLACK, (border_x, border_y, border_width, border_height), 2)

        selected_shape = next((shape for shape in self.shapes if shape.selected), None)
        if selected_shape:
            status_text = f"Selected: {selected_shape.shape_type}, Alpha: {selected_shape.alpha}, Rotation: {selected_shape.rotation}"
        else:
            status_text = "No shape selected"
        status_surface = font.render(status_text, True, BLACK)
        screen.blit(status_surface, (TOOLBAR_WIDTH + 10, HEIGHT - 30))

        pygame.display.flip()

# Khởi tạo editor và vòng lặp chính
editor = Editor()
clock = pygame.time.Clock()

while True:
    editor.handle_events()
    editor.draw(screen)
    clock.tick(60)

