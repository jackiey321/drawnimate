#################################################
# Background.py
# Background class used in minigame
#
# Your name: Jackie Yang     Section: J
# Your andrew id: jaclyny
#
#################################################

from Drawnimate import *

class Background(object):
    def __init__(self, app, x):
        self.app = app
        self.x = x
        self.margin = 30
        self.y = self.app.height / 2 + self.margin
