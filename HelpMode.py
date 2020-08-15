#################################################
# HelpMode.py
# Pop-up mode that describes buttons and features
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
from WelcomeMode import *
from DrawMode import *
from FlipbookMode import *
from GameMode import *
from PlayMode import *

class HelpMode(Mode):
    def redrawAll(mode, canvas):
        scale = 9
        canvas.create_text(mode.width / 2, mode.height / scale, 
                text = "    Help Screen", font = 'Arial 40 bold', 
                justify = CENTER)

        help = '''
        Simply click and drag to draw.
        Use the left and right arrow keys to switch between layers and 
        create more of them.
        Press 'v' to toggle the current layer's visibility.
        To animate, simply draw one frame per layer and press the 
        'Flipbook' button!
        You can make also make a game from your drawings by pressing 'Game'!
        
        -----------------Buttons--------------------
        Undo: Undos last stroke on current layer
        Clear: Erases all strokes on current layer
        Clear All: Erases all strokes from all layers
        Brush: To draw 
        Color: Choose brush color
        Eraser: To erase
        Size: Adjust brush size
        '''

        canvas.create_text(mode.width / 2, mode.height / 2, 
                    text = help, font = 'Arial 30', justify = CENTER)

        back = "       Press 'c' to return to canvas!"
        canvas.create_text(mode.width / 2, mode.height - mode.height / scale, 
                        text = back, font = 'Arial 30', justify = CENTER)
    
    def keyPressed(mode, event):
        if event.key == 'c':
            mode.app.setActiveMode(mode.app.drawMode)