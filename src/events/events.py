from __future__ import unicode_literals
import sys
from pipes import Template as pipe
import json
from urllib.request import urlopen
import config

config = config.get_config()['main']
eventsQueuePipePath = sys.path[0] + '/events/eventsQueue.fifo'
eventsQueuePipe = pipe()


def sendEvent(event):
    with eventsQueuePipe.open(eventsQueuePipePath, 'w') as eventsPipe:
        json.dump(event, eventsPipe)


def eventsConsumer():
    while True:
        with open(eventsQueuePipePath, 'r') as eventsPipe:
            event = eventsPipe.read()
            if event:
                print('New event:', json.loads(event))
                urlopen('http://127.0.0.1:5000/event')
