from __future__ import unicode_literals
from youtube_dl import YoutubeDL as ytdl
import threading
import sys
import config


def progress_hook(progress):
    print(progress)


def video_download_thread(data):
    return ytdl(data).download([data['url']])


def video_download(data):
    data = {**config.get_config()['youtube-dl'], **data}
    if not hasattr(data, 'outtmpl'):
        data['outtmpl'] = sys.path[0] + '/downloads/%(title)s-%(id)s.%(ext)s'
    data['progress_hooks'] = [progress_hook]
    thread = threading.Thread(target=video_download_thread, args=(data,))
    thread.start()
    thread.name = 'dl-' + str(thread.ident)
    return 'Download started (name: ' + thread.name + ')'
