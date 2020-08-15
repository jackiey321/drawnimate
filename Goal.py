#################################################
# Goal.py
# Goal class used in minigame
#
# Your name: Jackie Yang     Section: J
# Your andrew id: jaclyny
#
#################################################

from Drawnimate import *
import random

class Goal(object):
    def __init__(self, app):
        self.app = app
        self.margin = 170
        self.locX = self.makeLocX()
        self.locY = self.app.height - self.margin

    # determines random x location of the goal 
    def makeLocX(self):
        num = 3
        randNum = random.randint(0,2)
        # randomly chooses if goal will be to the left or right of player
        if randNum == 0:
            return random.randint(self.app.width / 2 - self.app.width * num, 
                                self.app.width / 2 - self.margin * 2)
        else:
            return random.randint(self.app.width / 2 + self.margin * 2,
                                self.app.width / 2 + self.app.width * num)
