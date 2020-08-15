#################################################
# WelcomeMode.py
# Splash screen introducing the application
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
from Drawnimate import *
from HelpMode import *
from DrawMode import *
from FlipbookMode import *
from GameMode import *
from PlayMode import *

class WelcomeMode(Mode):
    def redrawAll(mode, canvas):
        scale = 4
        welcome = '     Welcome to Drawnimate: A Drawing and Animating App!'
        canvas.create_text(mode.width / 2, mode.height / scale, text = welcome,
                            font = 'Arial 40 bold', justify = CENTER)
        instructions = '''
        Simply click and drag to draw.
        Use the left and right arrow keys to switch between layers and 
        create more of them.
        Press 'v' to toggle the current layer's visibility.
        To animate, simply draw one frame per layer and press the 
        'Flipbook' button!
        You can also make a game from your drawings by pressing 'Game'!
        Press 'h' to open the help screen anytime.
        '''
        canvas.create_text(mode.width / 2, mode.height / 2, text = instructions,
                            font = 'Arial 30', justify = CENTER)

        start = '       Press any key to begin!'
        canvas.create_text(mode.width / 2, mode.height - mode.height / scale, 
                        text = start, font = 'Arial 30', justify = CENTER)                 

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.drawMode)
