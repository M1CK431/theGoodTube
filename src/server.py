import connexion
from flask_socketio import SocketIO
import config
import sys
# from multiprocessing import Process
# import events.events as events

# import main config
config = config.get_config()['main']

# Create the application instance
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')


# Events related
flask_app = app.app
socketio = SocketIO(flask_app, logger=True)
print('socketio in server:', socketio)
# eventsProcess = Process(
#     name='Events',
#     daemon=True,
#     target=events.eventsConsumer
# )
# eventsProcess.start()


@app.route("/socketio", methods=['GET'])
def socketioclient():
    with open(sys.path[0] + '/socketIO.html', 'r') as file:
        return file.read()


@app.route("/socketiojs", methods=['GET'])
def socketiojsclient():
    with open(sys.path[0] + '/socket.io.slim.dev.js', 'r') as file:
        return file.read()


@app.route("/event", methods=['GET'])
def event():
    socketio.emit('alive', {'alive': True})
    print('socketio in server (event route)', socketio)
    return ''


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    socketio.run(
        flask_app,
        host=config['host'],
        port=config['port'],
        debug=True
    )
