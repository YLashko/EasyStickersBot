import os
UPDATE_INTERVAL = 1
OS_TYPE = os.environ.get("OS_TYPE", "win")
TOKEN = os.environ.get("TOKEN")
HELP_MESSAGE = """Hello! Here you can easily create stickers from any video! Just send me the file and I will convert it into an animated webm file you can then forward to the sticker bot! There' only one file type that's supported at the moment, mp4, but there will be more! There are also 3 modes available:
/cr - if the video is longer than 3 seconds, cut its tail;
/crsp - if the video is longer than 9 seconds, cut its tail, then speedup to make it 3 seconds long;
/sp - the same as crsp, but crops to 59 seconds"""
ADMIN = "532842840"
SUPPORTED_FORMATS = ["video/mp4", "image/png"]
FILE_SIZE_LIMIT = 20 * 1024 * 1024 # 20 mbytes
