#################################################
# Drawnimate.py
# Main file to run entire application
#
# Your name: Jackie Yang     Section: J
# Your andrew id: jaclyny
#
#################################################

# Animation Framework From:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# Modified cmu_112_graphics lines 298 and 299
from cmu_112_graphics import *
from tkinter import *
from WelcomeMode import *
from HelpMode import *
from DrawMode import *
from FlipbookMode import *
from GameMode import *
from PlayMode import *

# ModalApp Framework From:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
class DrawingApp(ModalApp):
    def appStarted(app):
        app.welcomeMode = WelcomeMode()
        app.drawMode = DrawMode()
        app.helpMode = HelpMode()
        app.flipbookMode = FlipbookMode()
        app.playMode = PlayMode()
        app.player = Player(app)
        app.gameMode = GameMode()
        app.setActiveMode(app.welcomeMode)

def runDrawingApplication():
    DrawingApp(width = 1440, height = 800)

#################################################
# testAll and main
#################################################

def main():
    runDrawingApplication()

if __name__ == '__main__':
    main()