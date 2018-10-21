from __future__ import unicode_literals
import json
from sys import path
import multiprocessing


def list():
    with open(path[0] + '/state.json', 'r') as file:
        return json.load(file)


def stop(url):
    for download in multiprocessing.active_children():
        if download.name == url:
            break
    else:
        return "No active download for " + url
    try:
        download.terminate()
        with open(path[0] + '/state.json', 'r') as file:
            state = json.load(file)
            for index, item in enumerate(state):
                if item["webpage_url"] == url:
                    break
            state[index]["progress"] = {
                **state[index]["progress"],
                **{
                    "status": "stopped",
                    "_eta_str": "stopped",
                    "_speed_str": "stopped",
                    "speed": 0,
                    "eta": 0
                }
            }
        with open(path[0] + '/state.json', 'w') as file:
            json.dump(state, file, indent="\t")
    except Exception as error:
        return "Unable to stop the download of " + url + ": " + error
    return "Download stopped for " + url
