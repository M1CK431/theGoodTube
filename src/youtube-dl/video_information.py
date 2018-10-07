from __future__ import unicode_literals
from youtube_dl import YoutubeDL as ytdl


def video_information(url):
    return ytdl().extract_info(url, download=False)
