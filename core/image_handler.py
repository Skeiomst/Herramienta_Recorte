from PIL import Image

class ImageHandler:
    def __init__(self):
        self.image = None
        self.path = ""

    def load_image(self, path):
        self.image = Image.open(path)
        self.path = path

    def crop(self, x, y, w, h):
        return self.image.crop((x, y, x + w, y + h))
