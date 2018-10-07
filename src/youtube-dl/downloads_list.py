from __future__ import unicode_literals
import threading


def downloads_list():
    list = []
    for download in threading.enumerate():
        if 'dl-' in download.name:
            del download._args[0]['progress_hook']
            list.append(
                {
                    'threadName': download._name,
                    'options': download._args[0]
                }
            )
    return list
