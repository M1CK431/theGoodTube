from .downloads import get, remove
from .progress import stop_download
from .. import socketio
from flask import Response, jsonify
from glob import glob
from os import path, remove as remove_file
import re


def delete_download(id):
    download = get(id)
    if download:
        if download["progress"]["status"] == "downloading":
            stop_download(download)

        escaped_filename = re.sub(
            '([\[\]\?\*])', r'[\1]',
            path.splitext(download["_filename"])[0]
        )
        try:
            for file in glob(escaped_filename + '.*'):
                remove_file(file)
        except Exception as error:
            response = jsonify({
                "error": "Unable to delete file(s) of "
                + download["title"] + ": " + str(error)
            })
            response.status_code = 500
            return response

        remove(download["id"])
        socketio.emit("delete", download)
        return Response(status=204)
    else:
        return Response(status=404)
