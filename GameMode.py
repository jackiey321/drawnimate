#################################################
# GameMode.py
# Mode where user makes drawings to be included in minigame
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
from tkinter.colorchooser import askcolor
from Drawnimate import *
from HelpMode import *
from DrawMode import *
from FlipbookMode import *
from WelcomeMode import *
from PlayMode import *
from Brush import *
from Layer import *
import math
from PIL import Image 

class GameMode(Mode):
    def appStarted(mode):
        mode.brush = Brush(mode.app, 5, "black")  # initial brush settings
        mode.buttonL, mode.buttonH = mode.getButtonDims()
        mode.margin = 10
        mode.grayMargin = 20
        mode.layers = [Layer(), Layer(), Layer(), Layer()]  # stores all layers
        mode.currLayer = mode.layers[0]  # current layer being drawn on
        mode.currStroke = []  # current strokes being drawn

    def getButtonDims(mode):
        scale = 20
        return mode.width / scale, mode.height / scale
    
    def keyPressed(mode, event):
        if event.key == 'h':
            mode.app.setActiveMode(mode.app.helpMode)
        elif event.key == 'Right':  # go to next layer 
            currIndex = mode.layers.index(mode.currLayer)
            if currIndex < len(mode.layers) - 1:  
                mode.currLayer = mode.layers[currIndex + 1]
        elif event.key == 'Left':  # go to previous layer
            currIndex = mode.layers.index(mode.currLayer)
            if currIndex > 0:
                mode.currLayer = mode.layers[currIndex - 1]

    def mousePressed(mode, event):
        if mode.inEraser(event.x, event.y):
            mode.brush.eraser = True  # switch from draw to eraser mode
            mode.brush.on = False
        elif mode.inBrush(event.x, event.y):  # switch from eraser to draw mode
            mode.brush.eraser = False
            mode.brush.on = True
        elif mode.inSize(event.x, event.y):  
            mode.brush.on = False  # turns off draw and eraser
            mode.brush.eraser = False
            # ask for new brush size
            newSize = mode.getUserInput("New brush size?")  
            if newSize != None and newSize.isdigit():
                mode.brush.size = int(newSize)
        elif mode.inClear(event.x, event.y): 
            # erases all strokes in current layer
            mode.currLayer.strokes = []   
        elif mode.inColor(event.x, event.y): 
            # uses tkinter color selector
            mode.brush.color = askcolor(color=mode.brush.color)[1]
        elif mode.inUndo(event.x, event.y):
            # removes last stroke
            if len(mode.currLayer.strokes) > 0:
                mode.currLayer.strokes.pop()
        elif mode.inCanvas(event.x, event.y):
            mode.app.setActiveMode(mode.app.drawMode)
        elif mode.inPlay(event.x, event.y):
            mode.loadImages()
            mode.app.setActiveMode(mode.app.playMode)
        elif mode.inSave(event.x, event.y):
            mode.app.saveSnapshot()
        else:
            mode.addToStroke(event.x, event.y)

    # determines if undo button clicked
    def inUndo(mode, x, y):
        left = mode.margin
        right = left + mode.buttonL 
        return (left <= x <= right and 
                mode.margin <= y <= mode.margin + mode.buttonH)

    # determines if clear button clicked
    def inClear(mode, x, y):
        interval = 20
        left = mode.margin + mode.buttonL + interval
        right = left + mode.buttonL 
        return (left <= x <= right and 
                mode.margin <= y <= mode.margin + mode.buttonH)     

    # determines if size button clicked
    def inSize(mode, x, y):
        interval = 140
        left = mode.width / 2 + interval - mode.buttonL / 2
        right = left + mode.buttonL 
        return (left <= x <= right and 
                mode.margin <= y <= mode.margin + mode.buttonH)

    # determines if brush button clicked
    def inBrush(mode, x, y):
        interval = 140
        left = mode.width / 2 - (mode.buttonL / 2 + interval)
        right = left + mode.buttonL 
        return (left <= x <= right and 
                mode.margin <= y <= mode.margin + mode.buttonH)

    # determines if color button clicked
    def inColor(mode, x, y):
        interval = 50
        left = mode.width / 2 - (mode.buttonL / 2 + interval)
        right = left + mode.buttonL 
        return (left <= x <= right and 
                mode.margin <= y <= mode.margin + mode.buttonH)

    # determines if eraser button clicked
    def inEraser(mode, x, y):
        interval = 50
        left = mode.width / 2 + interval - mode.buttonL  / 2
        right = left + mode.buttonL 
        return (left <= x <= right and 
                mode.margin <= y <= mode.margin + mode.buttonH)

    # determines if canvas button clicked
    def inCanvas(mode, x, y):
        right = mode.width - mode.margin 
        left = right - mode.buttonL
        return (left <= x <= right and 
                mode.margin <= y <= mode.margin + mode.buttonH)

    # determines if play button clicked
    def inPlay(mode, x, y):
        interval = 20
        right = mode.width - mode.margin 
        left = right - mode.buttonL
        top = mode.margin + mode.buttonH + interval
        return (left <= x <= right and top <= y <= top + mode.buttonH)

    # determines if save button clicked
    def inSave(mode, x, y):
        right = mode.width - mode.margin
        left = right - mode.buttonL
        top = mode.height - (mode.margin + mode.buttonH)
        return (left <= x <= right and top <= y <= top + mode.buttonH)

    # updates the newly saved images 
    def loadImages(mode):
        mode.loadPlayer()
        mode.loadEnemy()
        mode.loadGoal()
        mode.loadBackground()

    # updates player image
    def loadPlayer(mode):
        scale = 1/2
        image = mode.loadImage('player.png')
        image = mode.makeTransparent(image)
        width, height = image.size
        rectLength, rectHeight, margin = 380, 760, 120
        left = width / 2 - rectLength / 2
        top = height / 2 - rectHeight / 2 
        image = image.crop((left, top, left + rectLength, 
                                top + rectHeight - margin))
        mode.app.playMode.sprite = mode.scaleImage(image, scale)

    # updates enemy image
    def loadEnemy(mode):
        scale = 1/3
        image = mode.loadImage('enemy.png')
        image = mode.makeTransparent(image)
        width, height = image.size
        rectLength, rectHeight, margin = 380, 600, 120
        left = width / 2 - rectLength / 2
        top = height / 2 - rectHeight / 2 
        image = image.crop((left, top, left + rectLength, 
                                top + rectHeight - margin))
        mode.app.playMode.enemySprite = mode.scaleImage(image, scale)

    # updates goal image
    def loadGoal(mode):
        scale = 1/3
        image = mode.loadImage('goal.png')
        image = mode.makeTransparent(image)
        width, height = image.size
        rectLength, rectHeight, margin = 380, 600, 120
        left = width / 2 - rectLength / 2
        top = height / 2 - rectHeight / 2 
        image = image.crop((left, top, left + rectLength, 
                                top + rectHeight - margin))
        mode.app.playMode.goalSprite = mode.scaleImage(image, scale)

    # makes white pixels of image transparent
    # From: (https://stackoverflow.com/questions/765736/using-pil-to-make-all
    # -white-pixels-transparent)
    def makeTransparent(mode, img):
        img = img.convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        return img

    # updates background image
    def loadBackground(mode):
        scale = 1/2
        image = mode.loadImage('background.png')
        width, height = image.size
        margin = 10
        image = image.crop((margin, 0, width - margin, height))
        mode.app.playMode.background = mode.scaleImage(image, scale)

    # adds a click to strokes as one coordinate pair (dot)
    def addToStroke(mode, x, y):
        if mode.brush.on:
            size, color = mode.getBrushDetails()
            if mode.brush.eraser:
                color = 'white'
            mode.currStroke.append((x, y))
            mode.currLayer.strokes.append((size, color, mode.currStroke))

    # stores brush stroke
    def mouseDragged(mode, event):
        if mode.brush.on or mode.brush.eraser: 
            size, color = mode.getBrushDetails()
            if mode.brush.eraser:
                color = 'white'
            # adds coordinates to current stroke as mouse is dragged
            mode.currStroke.append((event.x, event.y))
            if len(mode.currLayer.strokes) > 0 and len(mode.currStroke) > 1:
                # removes unfinished stroke since constantly updated with 
                # coordinates until stroke is finished
                mode.currLayer.strokes.pop()
            # adds finished stroke to current layer
            mode.currLayer.strokes.append((size, color, mode.currStroke))

    def mouseReleased(mode, event):
        if not mode.brush.eraser and len(mode.currStroke) >= 2:
            upperSmooth = 50  
            lowerSmooth = 9  
            # to refine the smoothness of lines
            for maxLen in range (upperSmooth, lowerSmooth, -10):
                mode.smooth(maxLen)
        # resets current stroke for drawing a new stroke
        mode.currStroke = []

    # algorithm designed with aid from Professor Taylor
    def smooth(mode, maxLen):
        size, color = mode.getBrushDetails()
        bisects = []
        for i in range(1, len(mode.currStroke) - 1):
            x1, y1 = mode.currStroke[i - 1]
            x2, y2 = mode.currStroke[i]
            if mode.distance(x1, y1, x2, y2) > maxLen:
                # only bisects if segment too long
                bisects += mode.bisect(x1, y1, x2, y2, maxLen)
            else:
                # adds next point in sequence otherwise
                bisects += [mode.currStroke[i]]
        # add original start and end points
        mode.currStroke = [mode.currStroke[0]] + bisects + [mode.currStroke[-1]]
        # remove unsmoothed stroke
        mode.currLayer.strokes.pop()
        # add the smoothed stroke
        mode.currLayer.strokes.append((size, color, mode.currStroke))
            
    def distance(mode, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # recursively finds the midpoints of line segments until all the 
    # resulting segments are less than max length
    def bisect(mode, x1, y1, x2, y2, maxLen):
        midX = (x1 + x2) / 2
        midY = (y1 + y2) / 2
        if mode.distance(x1, y1, midX, midY) <= maxLen:
            return [(midX, midY)]
        else:
            # recurse lower half of segment
            lower = mode.bisect(x1, y1, midX, midY, maxLen)
            # recurse upper half of segment
            upper = mode.bisect(midX, midY, x2, y2, maxLen)
            # returns points in order
            return lower + [(midX, midY)] + upper

    def getBrushDetails(mode):
        return (mode.brush.size, mode.brush.color)

    def redrawAll(mode, canvas):      
        # draws all strokes in current layer
        for (size, color, stroke) in mode.currLayer.strokes:
            mode.drawStroke(canvas, size, color, stroke)

        mode.drawGrayMargins(canvas)
        mode.drawUndo(canvas)
        mode.drawClear(canvas)
        mode.drawColor(canvas)
        mode.drawSize(canvas)
        mode.drawLayer(canvas)
        mode.drawBrush(canvas)
        mode.drawEraser(canvas)
        mode.drawCanvas(canvas)
        mode.drawPlay(canvas)
        mode.drawSave(canvas)

        margin = 70
        canvas.create_text(mode.width / 2, margin, text = 'Game',
                            font = 'Arial 25 bold')
    
    # makes gray margins
    def drawGrayMargins(mode, canvas):
        topY = mode.grayMargin * 2 + mode.buttonH * 2
        canvas.create_rectangle(0, 0, mode.width, topY, fill = 'light gray')
        bottomY = mode.height - (mode.grayMargin + mode.buttonH)
        canvas.create_rectangle(0, bottomY, mode.width, mode.height, 
                                    fill = 'light gray')
                                    
    # makes brush button
    def drawBrush(mode, canvas):
        interval = 140
        left = mode.width / 2 - (mode.buttonL / 2 + interval)
        right = left + mode.buttonL
        if mode.brush.on:
            color = 'light gray'
        else:
            color = 'white'
        canvas.create_rectangle(left, mode.margin, right, 
                                mode.margin + mode.buttonH, fill = color)
        canvas.create_text(left + mode.buttonL  / 2, 
                             mode.margin + mode.buttonH / 2, text = 'Brush')

    # makes color button
    def drawColor(mode, canvas):
        interval = 45
        left = mode.width / 2 - (mode.buttonL / 2 + interval)
        right = left + mode.buttonL
        canvas.create_rectangle(left, mode.margin, right, 
                            mode.margin + mode.buttonH, fill = mode.brush.color)
        canvas.create_text(left + mode.buttonL  / 2, 
                             mode.margin + mode.buttonH / 2, text = 'Color')

    # makes eraser button
    def drawEraser(mode, canvas):
        interval = 45
        left = mode.width / 2 + interval - mode.buttonL / 2
        right = left + mode.buttonL
        if mode.brush.eraser:
            color = 'light gray'
        else:
            color = 'white'
        canvas.create_rectangle(left, mode.margin, right, 
                                mode.margin + mode.buttonH, fill = color)
        canvas.create_text(left + mode.buttonL / 2, 
                            mode.margin + mode.buttonH / 2, text = 'Eraser')

    # makes size button
    def drawSize(mode, canvas):
        interval = 140
        left = mode.width / 2 + interval - mode.buttonL / 2
        right = left + mode.buttonL 
        canvas.create_rectangle(left, mode.margin, right, 
                                mode.margin + mode.buttonH, fill = 'white')
        canvas.create_text(left + mode.buttonL / 2, 
            mode.margin + mode.buttonH / 2, text = f'Size: {mode.brush.size}')
    
    # makes undo button
    def drawUndo(mode, canvas):
        left = mode.margin
        right = left + mode.buttonL
        canvas.create_rectangle(left, mode.margin, right, 
                                mode.margin + mode.buttonH, fill = 'white')
        canvas.create_text(left + mode.buttonL / 2, 
                            mode.margin + mode.buttonH / 2, text = 'Undo')

    # makes clear button
    def drawClear(mode, canvas):
        interval = 20
        left = mode.margin + mode.buttonL + interval
        right = left + mode.buttonL
        canvas.create_rectangle(left, mode.margin, right, 
                                mode.margin + mode.buttonH, fill = 'white')
        canvas.create_text(left + mode.buttonL / 2, 
                            mode.margin + mode.buttonH / 2, text = 'Clear')        

    # makes canvas button          
    def drawCanvas(mode, canvas):
        right = mode.width - mode.margin 
        left = right - mode.buttonL
        canvas.create_rectangle(left, mode.margin, right, 
                    mode.margin + mode.buttonH, fill = 'white')
        canvas.create_text(left + mode.buttonL / 2, 
                            mode.margin + mode.buttonH / 2, text = 'Canvas')

    # makes play button 
    def drawPlay(mode, canvas):
        interval = 20
        right = mode.width - mode.margin 
        left = right - mode.buttonL
        top = mode.margin + mode.buttonH + interval
        canvas.create_rectangle(left, top, right, 
                    top + mode.buttonH, fill = 'white')
        canvas.create_text(left + mode.buttonL / 2, 
                            top + mode.buttonH / 2, text = 'Play!')
    
    # makes save button 
    def drawSave(mode, canvas):
        right = mode.width - mode.margin
        left = right - mode.buttonL
        top = mode.height - (mode.margin + mode.buttonH)
        canvas.create_rectangle(left, top, right, 
                    top + mode.buttonH, fill = 'white')
        canvas.create_text(left + mode.buttonL / 2, 
                            top + mode.buttonH / 2, text = 'Save') 

    def drawStroke(mode, canvas, size, color, stroke):
        radius = size // 2
        # draws a dot if one coordinate pair in stroke
        if len(stroke) == 1:
            cx, cy = stroke[0]
            canvas.create_oval(cx - radius, cy - radius, cx + radius, 
                    cy + radius, fill = color, outline = '')
        else:   # draw line segments connecting coordinate pairs in stroke
            for index in range(1, len(stroke)):
                prevCx, prevCy = stroke[index - 1]
                cx, cy = stroke[index]
                canvas.create_line(prevCx, prevCy, cx, cy, fill = color,
                                width = size, smooth = True, capstyle = ROUND, 
                                joinstyle = ROUND)
    
    # displays current layer number and label
    def drawLayer(mode, canvas):
        layer = mode.layers.index(mode.currLayer)
        
        if layer == 0:
            label = 'Player'
            mode.drawPlayerLayer(canvas)
        elif layer == 1:
            label = 'Enemy'
            mode.drawEnemyLayer(canvas)
        elif layer == 2:
            label = 'Goal'
            mode.drawGoalLayer(canvas)           
        elif layer == 3:
            label = 'Background'
            mode.drawBackgroundLayer(canvas)

        canvas.create_text(mode.width / 2, mode.height - mode.grayMargin, 
             text = f'{label}', font = 'Arial 20')

    def drawPlayerLayer(mode, canvas):
        margin = 100
        rectLength = 200
        rectHeight = 330
        left = mode.width / 2 - rectLength / 2
        top = mode.height / 2 - rectHeight / 2
        canvas.create_rectangle(left, top, left + rectLength, 
                                top + rectHeight, width = 5)
        message = ("Draw your player in the rectangle! It's best to fill it " + 
        "up as much as possible. Save it as  'player.png'  when finished. " +
        "Press the right arrow key for the next page.")
        canvas.create_text(mode.width / 2, margin, text = message, 
                        justify = CENTER, font = 'Arial 18')

    def drawEnemyLayer(mode, canvas):
        margin = 100
        rectLength = 200
        rectHeight = 250
        left = mode.width / 2 - rectLength / 2
        top = mode.height / 2 - rectHeight / 2
        canvas.create_rectangle(left, top, left + rectLength, 
                                top + rectHeight, width = 5)
        message = ("Draw your enemy in the rectangle! It's best to fill it " +
        "up as much as possible. Save it as  'enemy.png'  when finished. " +
        "Press the right arrow key for the next page.")
        canvas.create_text(mode.width / 2, margin, text = message, 
                        justify = CENTER, font = 'Arial 18')

    def drawGoalLayer(mode, canvas):
        margin = 100
        rectLength = 200
        rectHeight = 250
        left = mode.width / 2 - rectLength / 2
        top = mode.height / 2 - rectHeight / 2
        canvas.create_rectangle(left, top, left + rectLength, 
                                top + rectHeight, width = 5)
        message = ("Draw your goal in the rectangle! It's best to fill it " +
        "up as much as possible. Save it as  'goal.png'  when finished. " +
        "Press the right arrow key for the next page.")
        canvas.create_text(mode.width / 2, margin, text = message, 
                        justify = CENTER, font = 'Arial 18')
    
    def drawBackgroundLayer(mode, canvas):
        margin = 100
        message = ("Draw the background for the game so that it fills the " +
        "entire canvas. Save it as  'background.png'  when finished. " +
        "Press  'Play'  to begin the game!")
        canvas.create_text(mode.width / 2, margin, text = message, 
                            justify = CENTER, font = 'Arial 18')
