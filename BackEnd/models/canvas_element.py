class CanvasElement:
    def __init__(self, element_type, item_id, **kwargs):
        self.type = element_type
        self.item = item_id
        self.properties = kwargs  # x, y, image, text, font, angle, etc.
