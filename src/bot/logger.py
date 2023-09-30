from datetime import datetime
from src.bot.queries import *

class Logger:
    formatters = {
        "video_convert": lambda telegram_nickname, file_size, time: f"a video for @{telegram_nickname} with a size of {round(file_size / 1024, 4)}KB converted. time taken - {round(time, 4)}s",
        "photo_convert": lambda telegram_nickname, photo_res, photo_size, time: f"a photo for @{telegram_nickname} with a resolution of {photo_res[0]}x{photo_res[1]} and a size of {round(photo_size / 1024, 4)}KB converted. time taken - {round(time, 4)}s",
        "error": lambda where, exception_content: f"an exception in {where} occured: {exception_content}",
        "request_submit": lambda telegram_nickname, request_type, info: f"a request for @{telegram_nickname} submitted, type: {request_type}, file info: {info}",
        "help": lambda telegram_nickname: f"@{telegram_nickname} asked for help or started using the bot",
        "change_mode": lambda telegram_nickname, mode: f"@{telegram_nickname} changed their mode to {mode}", 
    }

    def __init__(self, max_length = 1000, show_time = True, database=None) -> None:
        self.max_length = max_length
        self.show_time = show_time
        self.database = database
        self.logs = []
    
    def log(self, record_type, *args, **kwargs) -> None:
        
        if record_type not in Logger.formatters.keys():
            raise ValueError(f"Invalid record type: {record_type}. Record types available - {', '.join(list(Logger.formatters.keys()))}")
        
        record = ""
        if self.show_time:
            record = datetime.now().strftime("%d/%m/%Y, %H:%M:%S - ")
        record += Logger.formatters[record_type](*args)

        filepath = kwargs["filepath"] if kwargs.keys().__contains__("filepath") else ""

        if self.database is not None:
            self.log_to_database(record, filepath)
        else:
            self.log_to_list(record, filepath)

    def log_to_database(self, text, filepath):
        self.database.execute(make_record(text, filepath))
    
    def log_to_list(self, text, filepath):
        self.logs.append([text, filepath])

        if len(self.logs) > self.max_length:
            self.logs.pop(0)
