#################################################
# Enemy.py
# Enemy class used in minigame
#
# Your name: Jackie Yang     Section: J
# Your andrew id: jaclyny
#
#################################################

from Drawnimate import *
import random

class Enemy(object):
    def __init__(self, app):
        self.app = app
        self.margin = 170
        self.locX = self.makeLocX()
        self.locY = self.app.height - self.margin

    # determines random x location of the enemy 
    def makeLocX(self):
        num = 2
        randNum = random.randint(0,2)
        # randomly chooses if enemy will be to the left or right of player
        if randNum == 0:
            return random.randint(self.app.player.locX - self.app.width * num, 
                                self.app.player.locX - self.margin * 2)
        else:
            return random.randint(self.app.player.locX + self.margin * 2,
                                self.app.player.locX + self.app.width * num)
