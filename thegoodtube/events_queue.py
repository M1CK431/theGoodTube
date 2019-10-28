from multiprocessing import SimpleQueue
from threading import Thread
from . import socketio
from datetime import datetime, timedelta

events_queue = SimpleQueue()


def events_queue_thread():
    interval = timedelta(milliseconds=500)
    last_progress_event_datetime = datetime.now()
    while True:
        event = events_queue.get()
        if (
            event["name"] == "progress"
            and event["payload"]["progress"] == "downloading"
        ):
            if datetime.now() > last_progress_event_datetime + interval:
                socketio.emit(event["name"], event["payload"])
                last_progress_event_datetime = datetime.now()
        else:
            socketio.emit(event["name"], event["payload"])

events_thread = Thread(target=events_queue_thread, daemon=True)
events_thread.start()
