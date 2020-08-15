#################################################
# Brush.py
# Brush class used in modes with drawing
#
# Your name: Jackie Yang     Section: J
# Your andrew id: jaclyny
#
#################################################

from Drawnimate import *

class Brush(object):
    def __init__(self, app, size, color, on = True, eraser = False):
        self.app = app
        self.size = size
        self.color = color
        self.on = on   # indiciates if on draw mode
        self.eraser = eraser # indicates if on eraser mode