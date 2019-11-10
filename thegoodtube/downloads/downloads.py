from multiprocessing import SimpleQueue
from threading import Thread
from .. import socketio
from os import environ, path, makedirs, mknod, stat, remove as remove_file
import json
from atexit import register
from datetime import datetime, timedelta

downloads = []

# Preserve state at exit
prefs_dir = environ['HOME'] + '/.config/theGoodTube'
state_file = prefs_dir + '/downloads.json'
save_interval = timedelta(seconds=2)

def save():
    if not path.isdir(prefs_dir):
        makedirs(prefs_dir)
    if not path.isfile(state_file):
        mknod(state_file)
    last_update = datetime.fromtimestamp(stat(state_file).st_mtime)
    # workaround: prevent atexit to stupidly call registered function 2 times
    if last_update + save_interval < datetime.now():
        with open(state_file, 'w') as file:
            json.dump(downloads, file, indent="\t")

register(save)

# Restore state at startup
if path.isfile(state_file):
    with open(state_file, 'r') as file:
        downloads = json.load(file)


# State managment
def get(id):
    for index, download in enumerate(downloads):
        if download["id"] == id:
            break
    else:
        return None
    return download


def add(download):
    downloads.append(download)


def update(updated_download):
    for index, download in enumerate(downloads):
        if download["id"] == updated_download["id"]:
            downloads[index] = updated_download
            return True
    else:
        return False


def remove(id):
    for index, download in enumerate(downloads):
        if download["id"] == id:
            downloads.pop(index)
            return True
    else:
        return False


def remove_finished():
    downloads[:] = [download for download in downloads if download["progress"]["status"] != "finished"]


# Handle download events from download processes
download_events_queue = SimpleQueue()

def download_events_queue_thread():
    def progress(payload):
        for index, download in enumerate(downloads):
            if download["id"] in payload["filename"]:
                downloads[index]["progress"] = payload
                socketio.emit("progress", downloads[index])
                break
        else:
            info_file_basename = path.splitext(payload['filename'])[0]
            info_filename = info_file_basename + '.info.json'
            if not path.isfile(info_filename):
                info_file_basename = path.splitext(info_file_basename)[0]
                info_filename = info_file_basename + '.info.json'
            with open(info_filename, 'r') as file:
                download = json.load(file)
            download["progress"] = payload
            downloads.append(download)
            socketio.emit("progress", download)

    def finished(download_params):
        for index, download in enumerate(downloads):
            if download["webpage_url"] == download_params["url"]:
                remove_file(path.splitext(download["_filename"])[0] + '.info.json')
                break

    event_handlers = { "progress": progress, "finished": finished }

    while True:
        event = download_events_queue.get()
        event_handlers[event["name"]](event["payload"])

download_events_thread = Thread(target=download_events_queue_thread, daemon=True)
download_events_thread.start()
