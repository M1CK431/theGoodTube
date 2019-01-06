from __future__ import unicode_literals
from youtube_dl.version import __version__ as youtube_dl_version


def socketio_emit(name, message):
    from server import socketio
    print('socketio in version:', socketio)
    socketio.emit(name, message)


def version():
    socketio_emit('version', {'api': '0.1'})
    return {
        'api': '0.1',
        'youtube-dl': youtube_dl_version
    }
