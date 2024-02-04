import os
UPDATE_INTERVAL = 1
OS_TYPE = os.environ.get("OS_TYPE", "win")
TOKEN = os.environ.get("TOKEN")
HELP_MESSAGE = """Hello! Here you can easily create stickers from any video or photo! Just send me the file and I will convert it into an animated webm or png file you can then forward to the sticker bot! There are only 2 file types that're supported at the moment, mp4 and png, but there will be more! There are also 3 modes available:
/cr - if the video is longer than 3 seconds, trim it to 3 seconds;
/crsp - if the video is longer than 9 seconds, trim it to 9 seconds, then speedup to make it 3 seconds long;
/sp - the same as crsp, but trims to 59 seconds
New stuff 02/2024! You can now remove background from your videos and photos! Use /bg.
To get information on how to configure background removal tool, send /bghelp.
P.S. If there are any issues you can report them to @wymwymych, it is all his fault"""
BG_HELP_MESSAGE = """To toggle background removal tool, use /bg.
There are 2 parameters to configure: background color and color similarity
background color can be set to 4 values: black, white, green or blue, by using /bgc [black/white/green/blue].
The second parameter determines how different the pixel color can be for it to be marked as a background.
To use it, send /bgs {level}, level is a number from 0 to 5, the higher the number, the more different background color can be from white/black"""
ADMIN = "532842840"
SUPPORTED_FORMATS = ["video/mp4", "image/png"]
FILE_SIZE_LIMIT = 20 * 1024 * 1024 # 20 mbytes
SAVE_FILES = True
