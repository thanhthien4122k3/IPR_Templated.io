from PIL import Image, ImageDraw, ImageFont
import copy
import math


class TextTool:
    def __init__(self, model):
        self.model = model
        self._create_text_image()

    def _get_font_path(self):
        weight = self.model.formatting['font_weight'].lower()
        font_map = {
            'regular': 'arial.ttf',
            'bold': 'arialbd.ttf',
            'semi-bold': 'arialbd.ttf',
            'italic': 'ariali.ttf'
        }
        if self.model.formatting['italic']:
            return font_map.get('italic', 'arial.ttf')
        return font_map.get(weight, 'arial.ttf')

    def _create_text_image(self):
        display_text = self.model.text
        if self.model.formatting['uppercase']:
            display_text = display_text.upper()
        elif self.model.formatting['lowercase']:
            display_text = display_text.lower()

        font_path = self._get_font_path()
        try:
            font = ImageFont.truetype(font_path, self.model.formatting['font_size'])
        except IOError:
            font = ImageFont.load_default()

        dummy_draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
        text_width, text_height = dummy_draw.textsize(display_text, font=font)

        img_width = text_width + self.model.formatting['letter_spacing'] * len(display_text)
        img_height = int(text_height * self.model.formatting['line_spacing'])

        base_image = Image.new('RGBA', (img_width, img_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(base_image)

        if self.model.formatting['fill_color']:
            fill_rect = [
                0,
                0,
                img_width + 2 * self.model.formatting['fill_padding'],
                img_height + 2 * self.model.formatting['fill_padding']
            ]
            draw.rounded_rectangle(
                fill_rect,
                radius=self.model.formatting['fill_corner_radius'],
                fill=self.model.formatting['fill_color']
            )

        text_x = self.model.formatting['fill_padding']
        text_y = self.model.formatting['fill_padding']

        x_cursor = text_x
        for char in display_text:
            draw.text((x_cursor, text_y), char, font=font, fill=self.model.formatting['color'])
            char_width, _ = draw.textsize(char, font=font)
            x_cursor += char_width + self.model.formatting['letter_spacing']

        if self.model.formatting['underline']:
            draw.line(
                [(text_x, text_y + text_height),
                 (text_x + text_width, text_y + text_height)],
                fill=self.model.formatting['color'], width=2
            )

        if self.model.formatting['strikethrough']:
            draw.line(
                [(text_x, text_y + text_height // 2),
                 (text_x + text_width, text_y + text_height // 2)],
                fill=self.model.formatting['color'], width=2
            )

        self.model.original_image = base_image
        self.model.current_image = copy.deepcopy(base_image)

    def set_formatting(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.model.formatting:
                self.model.formatting[key] = value
        self._create_text_image()

    def move(self, dx, dy):
        self.model.x += dx
        self.model.y += dy

    def rotate(self, angle):
        self.model.rotation = (self.model.rotation + angle) % 360
        self.model.current_image = self.model.current_image.rotate(angle, expand=True)

    def is_point_inside(self, mouse_x, mouse_y):
        local_x = mouse_x - self.model.x
        local_y = mouse_y - self.model.y
        angle_rad = math.radians(-self.model.rotation)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        rotated_x = local_x * cos_a + local_y * sin_a
        rotated_y = -local_x * sin_a + local_y * cos_a

        return (0 <= rotated_x <= self.model.current_image.width and
                0 <= rotated_y <= self.model.current_image.height)

    def get_image(self):
        return self.model.current_image
