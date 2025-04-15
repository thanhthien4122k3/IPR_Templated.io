from PIL import Image
import io

def export_canvas(canvas, path):
    ps = canvas.postscript(colormode="color")
    img = Image.open(io.BytesIO(ps.encode("utf-8")))
    img.save(path)
