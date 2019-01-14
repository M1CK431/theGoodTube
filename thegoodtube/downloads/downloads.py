from .. import app
from .add import add_download
from .delete import delete_download
from .progress import download_progress
from .helpers import (
    get_downloads,
    remove_download,
    remove_finished_downloads
)
from ..events_queue import events_queue
from flask.json import jsonify
from flask import request, Response


@app.route("/downloads", methods=["GET"])
def downloads_list():
    return jsonify(get_downloads())


@app.route("/downloads", methods=["POST"])
def downloads_post():
    return add_download(request.get_json(force=True, silent=True))


@app.route("/downloads/<id>/progress", methods=["PATCH"])
def progress_patch(id):
    return download_progress(id, request.get_json(force=True, silent=True))


@app.route("/downloads/<id>", methods=["DELETE"])
def downloads_id_delete(id):
    events_queue.put({"name": "clear", "payload": {"id": id}})
    return Response(status=remove_download(id))


@app.route("/downloads/<id>/files", methods=["DELETE"])
def files_delete(id):
    return delete_download(id)


@app.route("/downloads/<id>", methods=["GET"])
def downloads_id_get(id):
    return jsonify(get_downloads(id))


@app.route("/downloads", methods=["DELETE"])
def downloads_delete():
    remove_finished_downloads()
    events_queue.put({"name": "clear finished", "payload": {}})
    return Response(status=204)
