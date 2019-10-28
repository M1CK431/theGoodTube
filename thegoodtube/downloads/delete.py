from .helpers import get_downloads, remove_download
from .progress import stop_download
from ..events_queue import events_queue
from flask import Response, jsonify
from glob import glob
from os import path, remove
import re


def delete_download(id):
    download = get_downloads(id)
    if download:
        if download["progress"]["status"] == "downloading":
            stop_download(download)
        try:
            escaped_filename = re.sub(
                '([\[\]\?\*])', r'[\1]',
                path.splitext(download["_filename"])[0]
            )
            for file in glob(escaped_filename + '.*'):
                remove(file)
        except Exception as error:
            response = jsonify({
                "error": "Unable to delete file(s) of "
                + download["title"] + ": " + str(error)
            })
            response.status_code = 500
            return response
        events_queue.put({"name": "delete", "payload": download})
        return Response(status=remove_download(download["id"], True))
    else:
        return Response(status=404)
