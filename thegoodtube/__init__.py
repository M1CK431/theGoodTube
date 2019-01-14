from flask import Flask, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object('config')
socketio = SocketIO(app, logger=True)


@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "name": "theGoodTube",
        "description": "REST API over youtube-dl",
        "version": app.config["VERSION"],
        "environment": app.config["ENV"]
    })


from .downloads import downloads # noqa
from . import events_queue # noqa
# Only used for socketio test purpose
from .debug_event import debug_event # noqa
