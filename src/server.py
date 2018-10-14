import connexion
import config

# import main config
config = config.get_config()['main']

# Create the application instance
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host=config['host'], port=config['port'], debug=True)
