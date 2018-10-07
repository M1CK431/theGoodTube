from __future__ import unicode_literals
from youtube_dl.version import __version__ as youtube_dl_version


def version():
    return {
        'api': '0.1',
        'youtube-dl': youtube_dl_version
    }
