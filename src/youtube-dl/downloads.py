from __future__ import unicode_literals
import json
from sys import path
import os
from glob import glob
import multiprocessing


def list():
    with open(path[0] + '/state.json', 'r') as file:
        return json.load(file)


def stop(url):
    for process in multiprocessing.active_children():
        if process.name == url:
            break
    else:
        return "No active download for " + url
    try:
        process.terminate()
        state = list()
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


def delete(url):
    for process in multiprocessing.active_children():
        if process.name == url:
            process.terminate()
            break
    state = list()
    for index, item in enumerate(state):
        if item["webpage_url"] == url:
            break
    else:
        return "No download to delete for " + url
    try:
        for file in glob(os.path.splitext(item["_filename"])[0] + '.*'):
            os.remove(file)
        state.remove(state[index])
        with open(path[0] + '/state.json', 'w') as file:
            json.dump(state, file, indent="\t")
    except Exception as error:
        return "Unable to delete the download of " + url + ": " + str(error)
    return "Download " + url + " deleted"


def clear(url):
    state = list()
    for index, item in enumerate(state):
        if item["webpage_url"] == url:
            break
    else:
        return "No download to clear for " + url
    if item["progress"]["status"] != "finished":
        return "Download not finished for " + url
    state.remove(state[index])
    with open(path[0] + '/state.json', 'w') as file:
        json.dump(state, file, indent="\t")
    return "Download " + url + " cleared"


def clear_all():
    state = list()
    for index, item in enumerate(state):
        if item["progress"]["status"] == "finished":
            state.remove(state[index])
    with open(path[0] + '/state.json', 'w') as file:
        json.dump(state, file)
    return "All finished downloads cleared"
