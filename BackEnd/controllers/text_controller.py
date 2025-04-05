from PIL import Image
from models.text_model import TextModel, TextStyle
from tools.text_tool import TextTool

import pygame

class TextController:
    def __init__(self, x, y, text, style=None):
        """Khởi tạo controller cho văn bản"""
        self.model = TextModel(x, y, text, style)
        self.tool = TextTool(self.model)  # Gắn công cụ cho model
        self.selected = False
        self.dragging = False
    
    def update_text(self, new_text):
        """Cập nhật văn bản mới"""
        self.model.text = new_text
        self.tool._create_text_image()  # Tạo lại hình ảnh văn bản
    
    def set_formatting(self, **kwargs):
        """Cập nhật định dạng văn bản"""
        self.tool.set_formatting(**kwargs)

    def move(self, dx, dy):
        """Di chuyển văn bản"""
        self.tool.move(dx, dy)
    
    def rotate(self, angle):
        """Xoay văn bản"""
        self.tool.rotate(angle)

    def flip_horizontal(self):
        """Lật văn bản theo chiều ngang"""
        self.tool.model.current_image = self.tool.model.current_image.transpose(Image.FLIP_LEFT_RIGHT)

    def flip_vertical(self):
        """Lật văn bản theo chiều dọc"""
        self.tool.model.current_image = self.tool.model.current_image.transpose(Image.FLIP_TOP_BOTTOM)
    
    def is_point_inside(self, mouse_x, mouse_y):
        """Kiểm tra nếu điểm chuột nằm trong văn bản"""
        return self.tool.is_point_inside(mouse_x, mouse_y)
    
    def get_image(self):
        """Lấy hình ảnh văn bản"""
        return self.tool.get_image()

    def select(self):
        """Chọn văn bản"""
        self.selected = True

    def deselect(self):
        """Bỏ chọn văn bản"""
        self.selected = False

    def toggle_dragging(self, start_dragging=False):
        """Bật/tắt chế độ kéo thả"""
        self.dragging = start_dragging



# # Example usage - UI Integration
# def example_ui_integration():
#     # Initialize the controller
#     controller = TextController()

#     # Create text models with style
#     controller.create_text_model(100, 100, "Heading 1", TextStyle.HEADING)
#     controller.create_text_model(200, 200, "This is a body text", TextStyle.BODY)

#     # Select a text model from UI (for example, at coordinates 120, 110)
#     controller.select_model_at_point(120, 110)

#     # Apply formatting on active model
#     controller.apply_formatting_to_active_model(
#         uppercase=True, 
#         fill_color=(255, 255, 255),
#         letter_spacing=2
#     )

#     # Move the active model
#     controller.move_active_model(50, 50)

#     # Rotate active model
#     controller.rotate_active_model(45)

#     # Duplicate the active model
#     duplicated = controller.duplicate_active_model()
