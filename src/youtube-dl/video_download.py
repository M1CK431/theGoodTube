from __future__ import unicode_literals
from youtube_dl import YoutubeDL as ytdl
from multiprocessing import Process
import sys
from os import path, remove
import config
import json
# from flask import current_app
# from flask_socketio import SocketIO


def socketio_emit(name, message):
    # socketio = SocketIO(current_app._get_current_object())
    from server import socketio
    socketio.emit(name, message)


def update_progress(filename, progress):
    with open(filename, 'r') as file:
        info = json.load(file)
    with open(sys.path[0] + '/state.json', 'r') as file:
        state = json.load(file)
        for index, item in enumerate(state):
            if item["id"] == info["id"]:
                state[index]["progress"] = progress
                break
        else:
            info['progress'] = progress
            state.append(info)
    with open(sys.path[0] + '/state.json', 'w') as file:
        json.dump(state, file, indent="\t")
    socketio_emit('progress', state)


def progress_hook(progress):
    info_file_basename = path.splitext(progress['filename'])[0]
    info_filename = info_file_basename + '.info.json'
    if not path.isfile(info_filename):
        info_file_basename = path.splitext(info_file_basename)[0]
        info_filename = info_file_basename + '.info.json'
    update_progress(info_filename, progress)


def download_thread(data):
    ytdl(data).download([data['url']])
    with open(sys.path[0] + '/state.json', 'r') as file:
        state = json.load(file)
    for index, item in enumerate(state):
        if item["webpage_url"] == data["url"]:
            remove(path.splitext(item["_filename"])[0] + '.info.json')
            break


def download(data):
    data = {**config.get_config()['youtube-dl'], **data}
    if not hasattr(data, 'outtmpl'):
        data['outtmpl'] = sys.path[0] + '/downloads/%(title)s-%(id)s.%(ext)s'
    data['progress_hooks'] = [progress_hook]
    data['writeinfojson'] = True
    process = Process(target=download_thread, name=data['url'], args=(data,))
    process.start()
    socketio_emit('download', {'state': 'started', **data})
    return 'Download started'
