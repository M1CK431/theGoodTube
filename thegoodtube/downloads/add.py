from flask import Response
from youtube_dl import YoutubeDL as ytdl
from multiprocessing import Process
from datetime import datetime, timedelta
from .downloads import download_events_queue
from os import environ

def add_download(download_params):
    download_dir = environ['HOME'] + '/downloads'
    download_params = {
        **download_params,
        **{
            'outtmpl': download_dir + '/%(title)s-%(id)s.%(ext)s',
            'progress_hooks': [progress_hook],
            'writeinfojson': True,
            'quiet': True
        }
    }
    process = Process(
        target=download_process,
        name=download_params['url'],
        args=(download_params,)
    )
    process.start()
    return Response(status=201)


def progress_hook(progress):
    global update_interval, last_update
    if (
        progress["status"] != "downloading" or
        datetime.now() > last_update + update_interval
    ):
        download_events_queue.put({"name": "progress", "payload": progress})
        last_update = datetime.now()


def download_process(download_params):
    global update_interval, last_update
    update_interval = timedelta(milliseconds=500)
    last_update = datetime.now()
    ytdl(download_params).download([download_params['url']])
    download_events_queue.put({"name": "finished", "payload": download_params})
