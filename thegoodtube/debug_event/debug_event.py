from .. import app


@app.route("/socketio", methods=['GET'])
def socketioclient():
    with open(app.root_path + '/debug_event/socketIO.html', 'r') as file:
        return file.read()


@app.route("/socketiojs", methods=['GET'])
def socketiojsclient():
    with open(
        app.root_path + '/debug_event/socket.io.slim.dev.js', 'r'
    ) as file:
        return file.read()


@app.route("/event", methods=['GET'])
def event():
    from .. import socketio
    print("socketio in socketio.py:", socketio)
    socketio.emit('alive', {'alive': True})
    return ''
