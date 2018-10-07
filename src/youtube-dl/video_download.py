from __future__ import unicode_literals
from youtube_dl import YoutubeDL as ytdl
import threading


def progress_hook(progress):
    print(progress)


def video_download_thread(data):
    return ytdl(data).download([data['url']])


def video_download(data):
    data['progress_hook'] = progress_hook
    thread = threading.Thread(target=video_download_thread, args=(data,))
    thread.start()
    thread.name = 'dl-' + str(thread.ident)
    return 'Download started (name: ' + thread.name + ')'
