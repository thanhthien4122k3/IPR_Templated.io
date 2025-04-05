import copy
from PIL import Image, ImageOps, ImageDraw


class ImageTool:
    def __init__(self, x, y, width, height):
        """
        Initialize an image model with position, dimensions, and default properties
        """
        self.x = x  # X-coordinate on canvas
        self.y = y  # Y-coordinate on canvas
        self.width = width  # Width of the image
        self.height = height  # Height of the image
        
        # Create a blank RGBA image as the default
        self.original_image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        self.current_image = copy.deepcopy(self.original_image)
        
        self.rotation = 0  # Rotation angle in degrees
        self.selected = False  # Flag to indicate if image is selected
        self.dragging = False  # Flag to indicate if image is being dragged
    
    def flip_horizontal(self):
        """Flip image horizontally"""
        self.current_image = ImageOps.mirror(self.current_image)
    
    def flip_vertical(self):
        """Flip image vertically"""
        self.current_image = ImageOps.flip(self.current_image)
    
    def rotate(self, angle):
        """Rotate image by given angle"""
        self.rotation = (self.rotation + angle) % 360
        self.current_image = self.current_image.rotate(angle, expand=True)
    
    def round_corners(self, radius):
        """Round image corners"""
        mask = Image.new("L", self.current_image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, self.current_image.width, self.current_image.height), 
                                radius=radius, fill=255)
        
        result = self.current_image.copy()
        if result.mode != 'RGBA':
            result = result.convert('RGBA')
        
        background = Image.new('RGBA', self.current_image.size, (255, 255, 255, 0))
        self.current_image = Image.composite(result, background, mask)
    
    def add_border(self, border_size, border_color):
        """Add border to image"""
        self.current_image = ImageOps.expand(
            self.current_image, 
            border=border_size, 
            fill=border_color
        )
    
    def adjust_transparency(self, alpha):
        """Adjust image transparency"""
        img = self.current_image.convert("RGBA")
        new_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        pixels = img.load()
        new_pixels = new_img.load()
        
        for x in range(img.width):
            for y in range(img.height):
                r, g, b, _ = pixels[x, y]
                new_pixels[x, y] = (r, g, b, alpha)
        
        self.current_image = new_img
    
    def crop(self, box):
        """Crop image based on given box coordinates"""
        self.current_image = self.current_image.crop(box)
    
    def reset_to_original(self):
        """Reset image to its original state"""
        self.current_image = copy.deepcopy(self.original_image)
    

    
