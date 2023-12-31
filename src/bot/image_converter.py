from PIL import Image
from src.bot.util import get_desired_resolution
import io

def remove_bg(image: Image.Image, color=(255, 255, 255, 255)):
    pixels = image.load()
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if pixels[x, y] == color:
                image.putpixel((x, y), (0, 0, 0, 0))
    return image

def process_image_document(image: bytes, transparent: bool = True) -> io.BytesIO:
    stream = io.BytesIO(image)
    image_pil = Image.open(stream).convert("RGBA")
    size = image_pil.size
    image_pil = image_pil.resize(get_desired_resolution(size))
    if transparent:
        image_pil = remove_bg(image_pil)
    result_bytesio = io.BytesIO()
    result_bytesio.name = "out.png"
    image_pil.save(result_bytesio, "PNG")
    result_bytesio.seek(0)
    return result_bytesio
