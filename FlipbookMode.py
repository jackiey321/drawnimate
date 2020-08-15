#################################################
# FlipbookMode.py
# Mode that allows user to animate layers into flipbook
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
from WelcomeMode import *
from GameMode import *
from PlayMode import *
from Brush import *
from Layer import *

class FlipbookMode(Mode):
    def appStarted(mode):
        mode.layers = mode.app.drawMode.layers  # accesses layers drawn
        mode.time = None
        mode.margin = 10
        mode.grayMargin = 20
        mode.buttonL, mode.buttonH = mode.getButtonDims()
        mode.timerDelay = 600
    
    def getButtonDims(mode):
        scale = 20
        return mode.width / scale, mode.height / scale
    
    # keep track of time for 'page' switching
    def timerFired(mode):
        if mode.time != None:
            mode.time += mode.timerDelay
    
    def keyPressed(mode, event):
        if event.key == 'h':
            mode.app.setActiveMode(mode.app.helpMode) 

    def mousePressed(mode, event):
        if mode.inCanvas(event.x, event.y):
            mode.app.setActiveMode(mode.app.drawMode)
        elif mode.inReplay(event.x, event.y):
            mode.app.drawMode.flipbook = True
            mode.time = 0      

    # determines if canvas button clicked
    def inCanvas(mode, x, y):
        right = mode.width - mode.margin 
        left = right - mode.buttonL
        return (left <= x <= right and 
                mode.margin <= y <= mode.margin + mode.buttonH)  

    # determines if replay button clicked
    def inReplay(mode, x, y):
        interval = 90
        right = mode.width - mode.margin - interval
        left = right - mode.buttonL 
        return (left <= x <= right and 
                mode.margin <= y <= mode.margin + mode.buttonH)   

    def redrawAll(mode, canvas):
        margin = 30
        if mode.app.drawMode.flipbook == True:
            # constant flip rate, one frame every tenth of second
            if mode.time % mode.timerDelay == 0:
                layer = mode.time // mode.timerDelay
                if layer == len(mode.layers):  # stop once last layer reached
                    mode.time = None  # reset
                    mode.app.drawMode.flipbook = False
                else:
                    # draws all strokes on each layer
                    for (size, color, stroke) in mode.layers[layer].strokes:
                        mode.drawStroke(canvas, size, color, stroke)
        
        mode.drawGrayMargins(canvas)
        mode.drawCanvas(canvas)
        mode.drawReplay(canvas)
        
        margin = 70
        canvas.create_text(mode.width / 2, margin, text = 'Flipbook',
                            font = 'Arial 25 bold')

    def drawStroke(mode, canvas, size, color, stroke):
        radius = size // 2
        # draws a dot if one coordinate pair in stroke
        if len(stroke) == 1:
            cx, cy = stroke[0]
            canvas.create_oval(cx - radius, cy - radius, cx + radius, 
                    cy + radius, fill = color, outline = '')
        else:  # draw line segments connecting coordinate pairs in stroke
            for index in range(1, len(stroke)):
                prevCx, prevCy = stroke[index - 1]
                cx, cy = stroke[index]
                canvas.create_line(prevCx, prevCy, cx, cy, fill = color,
                                width = size, smooth = True, capstyle = ROUND, 
                                joinstyle = ROUND)

    # makes gray margins
    def drawGrayMargins(mode, canvas):
        topY = mode.grayMargin * 2 + mode.buttonH * 2
        canvas.create_rectangle(0, 0, mode.width, topY, fill = 'light gray')
        bottomY = mode.height - (mode.grayMargin + mode.buttonH)
        canvas.create_rectangle(0, bottomY, mode.width, mode.height, 
                                    fill = 'light gray')

    # makes canvas button
    def drawCanvas(mode, canvas):
        right = mode.width - mode.margin 
        left = right - mode.buttonL
        canvas.create_rectangle(left, mode.margin, right, 
                    mode.margin + mode.buttonH, fill = 'white')
        canvas.create_text(left + mode.buttonL / 2, 
                            mode.margin + mode.buttonH / 2, text = 'Canvas')

    # makes replay button
    def drawReplay(mode, canvas):
        interval = 90
        right = mode.width - mode.margin - interval
        left = right - mode.buttonL
        canvas.create_rectangle(left, mode.margin, right, 
                    mode.margin + mode.buttonH, fill = 'white')
        canvas.create_text(left + mode.buttonL / 2, 
                            mode.margin + mode.buttonH / 2, text = 'Replay')
