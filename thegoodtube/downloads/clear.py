from flask import Response, jsonify
from .downloads import remove, remove_finished
from .. import socketio


def clear_downloads(id):
    if "id" in locals():
        if remove(id):
            socketio.emit("clear", {"id": id})
            return 204
        else:
            return 404
    else:
        remove_finished()
        socketio.emit("clear_all", {})
        return 204
