from PIL import Image
import os


class UploadController:
    def __init__(self):
        self.image = None
        self.image_path = None
        self.loaded = False

    def upload_image(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"FileNotFoundError: {file_path}")

        try:
            self.image = Image.open(file_path).convert("RGBA")
            self.image_path = file_path
            self.loaded = True
            print(f"Upload successfully: {file_path}")
        except Exception as e:
            print(f"Lỗi upload ảnh: {e}")
            self.image = None
            self.loaded = False

    def get_image(self):
        return self.image

    def is_loaded(self):
        return self.loaded
