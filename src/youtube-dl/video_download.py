from __future__ import unicode_literals
from youtube_dl import YoutubeDL as ytdl
import threading
import sys
from os import path, remove
import config
import json


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


def progress_hook(progress):
    info_file_basename = path.splitext(progress['filename'])[0]
    info_filename = info_file_basename + '.info.json'
    if not path.isfile(info_filename):
        info_file_basename = path.splitext(info_file_basename)[0]
        info_filename = info_file_basename + '.info.json'
    update_progress(info_filename, progress)


def video_download_thread(data):
    ytdl(data).download([data['url']])
    with open(sys.path[0] + '/state.json', 'r') as file:
        state = json.load(file)
    for index, item in enumerate(state):
        if item["webpage_url"] == data["url"]:
            remove(path.splitext(item["_filename"])[0] + '.info.json')
            break


def video_download(data):
    data = {**config.get_config()['youtube-dl'], **data}
    if not hasattr(data, 'outtmpl'):
        data['outtmpl'] = sys.path[0] + '/downloads/%(title)s-%(id)s.%(ext)s'
    data['progress_hooks'] = [progress_hook]
    data['writeinfojson'] = True
    thread = threading.Thread(target=video_download_thread, args=(data,))
    thread.start()
    return 'Download started'
