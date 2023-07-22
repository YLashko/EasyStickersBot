from collections import defaultdict
from telebot.async_telebot import AsyncTeleBot
from src.converter import Converter, PipeModes
import asyncio
import aiohttp
from pathlib import Path
import os
from src.image_converter import process_image_document
from config import ADMIN, FILE_SIZE_LIMIT, HELP_MESSAGE, SUPPORTED_FORMATS, TOKEN, UPDATE_INTERVAL
from src.util import os_path, first_nonnone, format_from_filename

bot = AsyncTeleBot(TOKEN)

class GlobalData:
    def __init__(self, in_f, buf_f, out_f):
        self.in_f = in_f
        self.buf_f = buf_f
        self.out_f = out_f
        self.running = True
        self.converter = Converter(in_f, buf_f, out_f)
        self.user_modes = defaultdict(lambda: PipeModes.Crop)

    def set_user_mode(self, uid: str | int, mode: int) -> None:
        if not mode in PipeModes.modes_list:
            raise ValueError("Mode is not on the list")
        self.user_modes[uid] = mode
    
    def process_video(self, uid, filename):

        res_filename = self.converter.create_and_run_pipe(filename, self.user_modes[uid])
        return res_filename


@bot.message_handler(commands=["start", "help"])
async def help(message):
    await bot.send_message(
        message.from_user.id, 
        HELP_MESSAGE
    )


@bot.message_handler(commands=["stop"])
async def stop(message):
    global global_data
    if str(message.from_user.id) == ADMIN:
        await bot.send_message(message.from_user.id, "Stopping bot...")
        global_data.running = False
        await bot.close_session()
        return


@bot.message_handler(commands=["cr"])
async def mode_crop(message):
    global global_data
    global_data.set_user_mode(message.from_user.id, PipeModes.Crop)
    await bot.send_message(message.from_user.id, "Convert mode set to Crop!")


@bot.message_handler(commands=["crsp"])
async def mode_crop(message):
    global global_data
    global_data.set_user_mode(message.from_user.id, PipeModes.CropAndSpeedup)
    await bot.send_message(message.from_user.id, "Convert mode set to Crop + Speedup!")


@bot.message_handler(commands=["sp"])
async def mode_crop(message):
    global global_data
    global_data.set_user_mode(message.from_user.id, PipeModes.Speedup)
    await bot.send_message(message.from_user.id, "Convert mode set to Speedup!")


@bot.message_handler(content_types=["photo", "document"])
async def receive_photo(message):
    global global_data
    user = message.from_user
    doc = first_nonnone([message.photo, message.document]) # there are many copies sent at the same time, -1 to pick the highest resolution
    
    if message.photo is not None:
        doc = doc[-1]
    
    if message.document is not None:
        if doc.mime_type not in SUPPORTED_FORMATS:
            await bot.send_message(user.id, "Format not supported")
            return
    
    if doc.file_size > FILE_SIZE_LIMIT:
        await bot.send_message(user.id, "File exceeds the size limit")
        return

    info = await bot.get_file(doc.file_id)
    downloaded_file = await bot.download_file(info.file_path)
    
    result_io = process_image_document(downloaded_file)
    await bot.send_document(user.id, result_io)


@bot.message_handler(content_types=["video", "animation"])
async def receive_vid(message):
    global global_data
    user = message.from_user
    doc = first_nonnone([message.video, message.animation, message.document])
    filename = doc.file_name
    info = await bot.get_file(doc.file_id)

    if doc.mime_type not in SUPPORTED_FORMATS:
        await bot.send_message(user.id, "Format not supported")
        return
    
    if doc.file_size > FILE_SIZE_LIMIT:
        await bot.send_message(user.id, "File exceeds the size limit")
        return
    
    downloaded_file = await bot.download_file(info.file_path)
    target_path = os_path(f"{global_data.in_f}/in-{global_data.converter.counter}.mp4")

    with open(target_path, "wb") as f:
        f.write(downloaded_file)
    
    result_path = global_data.converter.create_and_run_pipe(
        f"in-{global_data.converter.counter}.mp4",
        global_data.user_modes[user.id]
    )
    await bot.send_animation(user.id, open(result_path, "rb"))
    os.remove(result_path)


async def polling():
    global global_data
    while global_data.running:
        try:
            await bot.polling(non_stop=True, interval=UPDATE_INTERVAL)
        except Exception as e:
            print(f"Exception in polling: {e}")


def run():
    global global_data

    if TOKEN in [None, ""]:
        raise ValueError("Token is not set up")
    
    global_data = GlobalData("in", "buf", "out")
    global_data.loop = asyncio.get_event_loop()
    global_data.loop.create_task(polling())
    global_data.loop.run_forever()


if __name__ == "__main__":
    run()
