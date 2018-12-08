import connexion
from flask_socketio import SocketIO
import config

# import main config
config = config.get_config()['main']

# Create the application instance
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')


# SocketIO related
flask_app = app.app
socketio = SocketIO(flask_app)


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    socketio.run(
        flask_app,
        host=config['host'],
        port=config['port'],
        debug=True
    )
