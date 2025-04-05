class TextStyle:
    """Predefined text styles"""
    HEADING = {
        'font_size': 36,
        'font_weight': 'bold',
        'color': (0, 0, 0)
    }
    SUBHEADING = {
        'font_size': 24,
        'font_weight': 'semi-bold',
        'color': (50, 50, 50)
    }
    BODY = {
        'font_size': 16,
        'font_weight': 'regular',
        'color': (0, 0, 0)
    }



class TextModel:
    def __init__(self, x, y, text, style=None):
        self.x = x
        self.y = y
        self.text = text

        self.formatting = {
            'font_name': 'arial.ttf',
            'font_size': style['font_size'] if style else 16,
            'font_weight': style['font_weight'] if style else 'regular',
            'color': style['color'] if style else (0, 0, 0),
            'uppercase': False,
            'lowercase': False,
            'bold': False,
            'italic': False,
            'underline': False,
            'strikethrough': False,
            'alignment': 'left',
            'letter_spacing': 0,
            'line_spacing': 1.2,
            'fill_color': None,
            'fill_padding': 0,
            'fill_corner_radius': 0,
            'stroke_width': 0,
            'stroke_color': (0, 0, 0),
            'opacity': 255
        }

        self.rotation = 0
        self.selected = False
        self.dragging = False

        self.original_image = None
        self.current_image = None
