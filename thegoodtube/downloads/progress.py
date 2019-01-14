from .add import add_download
from .helpers import get_downloads, update_download
from ..events_queue import events_queue
from flask import Response, jsonify
from multiprocessing import active_children


def download_progress(id, progress):
    download = get_downloads(id)
    if download:
        if progress:
            if progress["status"] == "stop":
                if download["progress"]["status"] == "downloading":
                    return stop_download(download)
                else:
                    return Response(status=422)
            elif progress["status"] == "start":
                if download["progress"]["status"] != "downloading":
                    return start_download(download)
                else:
                    return Response(status=422)
            else:
                return Response(status=422)
        else:
            return Response(status=400)
    else:
        return Response(status=404)


def start_download(download):
    add_download({"url": download["webpage_url"]})
    download["progress"] = {
            **download["progress"],
            **{
                "status": "starting",
                "_eta_str": "starting",
                "_speed_str": "starting",
                "speed": 0,
                "eta": 0
            }
        }
    update_download(download)
    events_queue.put({"name": "start", "payload": download})
    return Response(status=204)


def stop_download(download):
    for process in active_children():
        if process.name == download["webpage_url"]:
            break
    try:
        process.terminate()
        download["progress"] = {
            **download["progress"],
            **{
                "status": "stopped",
                "_eta_str": "stopped",
                "_speed_str": "stopped",
                "speed": 0,
                "eta": 0
            }
        }
        update_download(download)
    except Exception as error:
        response = jsonify({
            "error": "Unable to stop the download of "
            + download["title"] + ": " + error
        })
        response.status_code = 500
        return response
    events_queue.put({"name": "stop", "payload": download})
    return Response(status=204)
