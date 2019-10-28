from .helpers import update_download, append_download
from .. import app
from ..events_queue import events_queue
from flask import Response
from youtube_dl import YoutubeDL as ytdl
from multiprocessing import Process
from os import environ, path, remove
import json


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
        target=download_thread,
        name=download_params['url'],
        args=(download_params,)
    )
    process.start()
    return Response(status=201)


def progress_hook(progress):
    info_file_basename = path.splitext(progress['filename'])[0]
    info_filename = info_file_basename + '.info.json'
    if not path.isfile(info_filename):
        info_file_basename = path.splitext(info_file_basename)[0]
        info_filename = info_file_basename + '.info.json'
    update_progress(info_filename, progress)


def download_thread(download_params):
    ytdl(download_params).download([download_params['url']])
    with open(app.root_path + '/state.json', 'r') as file:
        state = json.load(file)
    for index, item in enumerate(state):
        if item["webpage_url"] == download_params["url"]:
            remove(path.splitext(item["_filename"])[0] + '.info.json')
            break


def update_progress(filename, progress):
    with open(filename, 'r') as file:
        download = json.load(file)
    download["progress"] = progress
    events_queue.put({"name": "progress", "payload": download})
    if not update_download(download):
        append_download(download)
