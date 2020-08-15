#################################################
# Player.py
# Player class used in minigame
#
# Your name: Jackie Yang     Section: J
# Your andrew id: jaclyny
#
#################################################

from Drawnimate import *

class Player(object):
    def __init__(self, app):
        self.app = app
        self.locX = self.app.width / 2
        self.margin = 260
        self.locY = self.app.height - self.margin