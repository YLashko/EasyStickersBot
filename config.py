import os
UPDATE_INTERVAL = 1
OS_TYPE = os.environ.get("OS_TYPE", "win")
TOKEN = os.environ.get("TOKEN")
HELP_MESSAGE = """Hello! Here you can easily create stickers from any video or photo! Just send me the file and I will convert it into an animated webm or png file you can then forward to the sticker bot! There are only 2 file types that're supported at the moment, mp4 and png, but there will be more! There are also 3 modes available:
/cr - if the video is longer than 3 seconds, trim it to 3 seconds;
/crsp - if the video is longer than 9 seconds, trim it to 9 seconds, then speedup to make it 3 seconds long;
/sp - the same as crsp, but trims to 59 seconds"""
ADMIN = "532842840"
SUPPORTED_FORMATS = ["video/mp4", "image/png"]
FILE_SIZE_LIMIT = 20 * 1024 * 1024 # 20 mbytes
SAVE_FILES = True
