import json
import sys


def get_config():
    with open(sys.path[0] + '/config.json', 'r') as config_file:
        config = json.load(config_file)
        return config


def update_config(config):
    config = {**get_config(), **config}
    with open(sys.path[0] + '/config.json', 'w') as config_file:
        try:
            json.dump(config, config_file, indent="\t")
        except Exception as error:
            return 'Unable to save the new configuration:' + error
        else:
            return 'Configuration updated'
