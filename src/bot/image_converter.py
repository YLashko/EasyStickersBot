from PIL import Image
from src.bot.util import get_desired_resolution
import io


def remove_bg(image: Image.Image, color = (255, 255, 255, 255), similarity_level = 0):
    pixels = image.load()
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if compute_difference(pixels[x, y], color) <= similarity_level:
                image.putpixel((x, y), (0, 0, 0, 0))
    return image


def compute_difference(color1: tuple, color2: tuple) -> float:
    return (
        (color1[0] - color2[0]) ** 2 + \
        (color1[1] - color2[1]) ** 2 + \
        (color1[2] - color2[2]) ** 2 + \
        (color1[3] - color2[3]) ** 2
    ) ** 0.5


def process_image_document(image: bytes, transparent: bool = True, background_color: tuple = (255, 255, 255, 255), similarity_level: int = 0) -> io.BytesIO:
    stream = io.BytesIO(image)
    image_pil = Image.open(stream).convert("RGBA")
    size = image_pil.size
    image_pil = image_pil.resize(get_desired_resolution(size))
    if transparent:
        image_pil = remove_bg(image_pil, background_color, similarity_level)
    result_bytesio = io.BytesIO()
    result_bytesio.name = "out.png"
    image_pil.save(result_bytesio, "PNG")
    result_bytesio.seek(0)
    return result_bytesio
