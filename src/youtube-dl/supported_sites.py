from __future__ import unicode_literals
from youtube_dl.extractor import list_extractors
# import json


def supported_sites():
    list = []
    for extractor in list_extractors(0):
        if extractor._WORKING:
            list.append(extractor.IE_NAME)
    return list
