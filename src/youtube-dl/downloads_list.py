from __future__ import unicode_literals
import json
from sys import path


def downloads_list():
    with open(path[0] + '/state.json', 'r') as file:
        return json.load(file)
