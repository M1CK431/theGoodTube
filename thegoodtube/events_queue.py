from multiprocessing import SimpleQueue
from threading import Thread
from . import socketio

events_queue = SimpleQueue()


def events_queue_thread():
    while True:
        event = events_queue.get()
        socketio.emit(event["name"], event["payload"])


events_thread = Thread(target=events_queue_thread, daemon=True)
events_thread.start()
