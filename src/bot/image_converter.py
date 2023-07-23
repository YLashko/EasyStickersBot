from PIL import Image
from src.bot.util import get_desired_resolution
import io

def process_image_document(image: bytes) -> io.BytesIO:
    stream = io.BytesIO(image)
    image_pil = Image.open(stream)
    size = image_pil.size

    image_pil = image_pil.resize(get_desired_resolution(size))
    result_bytesio = io.BytesIO()
    result_bytesio.name = "out.png"
    image_pil.save(result_bytesio, "PNG")
    result_bytesio.seek(0)
    return result_bytesio
