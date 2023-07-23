import multiprocessing
import subprocess


bot_process = multiprocessing.Process(
    target=subprocess.run,
    kwargs={
        'args': f'python -m src.bot.bot flask_api',
        'shell': True
    })


flask_process = multiprocessing.Process(
    target=subprocess.run,
    kwargs={
        'args': f'python -m src.flask.flask_server',
        'shell': True
    })


if __name__ == '__main__':
    flask_process.start()
    bot_process.start()