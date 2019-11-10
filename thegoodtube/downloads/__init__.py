from .. import app
from .downloads import downloads, get
from .add import add_download
from .clear import clear_downloads
from .delete import delete_download
from .progress import download_progress
from flask.json import jsonify
from flask import request, Response


@app.route("/downloads", methods=["GET"])
def downloads_list():
    return jsonify(downloads)


@app.route("/downloads", methods=["POST"])
def downloads_post():
    return add_download(request.get_json(force=True, silent=True))


@app.route("/downloads/<id>/progress", methods=["PATCH"])
def progress_patch(id):
    return download_progress(id, request.get_json(force=True, silent=True))


@app.route("/downloads/<id>", methods=["DELETE"])
def downloads_id_clear(id):
    return Response(status=clear_downloads(id))


@app.route("/downloads/<id>/files", methods=["DELETE"])
def files_delete(id):
    return delete_download(id)


@app.route("/downloads/<id>", methods=["GET"])
def downloads_id_get(id):
    return jsonify(get(id))


@app.route("/downloads", methods=["DELETE"])
def downloads_clear():
    return Response(status=clear_downloads())
