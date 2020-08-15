#################################################
# PlayMode.py
# Runs the minigame the user can play
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
from WelcomeMode import *
from Player import *
from Enemy import *
from Goal import *
from Background import *
from PIL import Image 

class PlayMode(Mode):
    def appStarted(mode):
        mode.margin = 10
        mode.grayMargin = 20
        mode.buttonL, mode.buttonH = mode.getButtonDims()
        mode.enemyDx = 15
        mode.moveDx = 30
        mode.moveDy = 25
        mode.scrollMarg = 260
        mode.timerDelay = 1 
        mode.restart()

    # values that need to be reset for each run
    def restart(mode):
        mode.app.player.locX = mode.width / 2
        mode.app.player.locY = mode.height - mode.scrollMarg
        mode.sprite = mode.loadPlayer()
        mode.enemySprite = mode.loadEnemy()
        mode.goalSprite = mode.loadGoal()
        mode.background = mode.loadBackground()
        mode.goal = Goal(mode.app)
        mode.makeBackgrounds()
        mode.gameOver = False
        mode.won = False
        mode.enemies = []
        mode.jump = False
        mode.peak = False
        mode.imageFlip = False
        mode.scrollX = 0
        mode.timer = 0 

    # makes player image
    def loadPlayer(mode):
        scale = 1/2
        image = mode.loadImage('player.png')
        image = mode.makeTransparent(image)
        width, height = image.size
        rectLength = 380 
        rectHeight = 760 
        margin = 120
        left = width / 2 - rectLength / 2
        top = height / 2 - rectHeight / 2 
        image = image.crop((left, top, left + rectLength, 
                                top + rectHeight - margin))
        return mode.scaleImage(image, scale)

    # makes enemy image
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
        return mode.scaleImage(image, scale)

    # makes goal image
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
        return mode.scaleImage(image, scale)

    # makes background image
    def loadBackground(mode):
        scale = 1/2
        image = mode.loadImage('background.png')
        width, height = image.size
        margin = 10
        image = image.crop((margin, 0, width - margin, height))
        return mode.scaleImage(image, scale)

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

    # creates list of 3 copies of drawn background
    def makeBackgrounds(mode):
        width, length = mode.background.size
        background1 = Background(mode.app, mode.width / 2 - width)
        background2 = Background(mode.app, mode.width / 2)
        background3 = Background(mode.app, mode.width / 2 + width)
        mode.backgrounds = [background1, background2, background3]     

    def timerFired(mode):
        if not mode.gameOver:
            mode.timer += 1
            mode.makeEnemies()
            mode.chasePlayer()

            # lets the player jump
            marg1, marg2 = 420, 260
            if mode.jump:
                if not mode.peak and mode.app.player.locY > mode.height - marg1:
                    mode.app.player.locY -= mode.moveDy
                else:
                    # reached max height of jump
                    mode.peak = True
                
                if mode.peak:
                    if mode.app.player.locY < mode.height - marg2:
                        # player falls back down 
                        mode.app.player.locY += mode.moveDy
                    else:
                        mode.jump = False

    # generates an enemy at a specified time interval
    def makeEnemies(mode):
        time = 10
        if mode.timer % time == 0:
            mode.enemies.append(Enemy(mode.app))
        
        # starts deleting enemies if too many to save space
        maxNum = 40
        if len(mode.enemies) > maxNum:
            mode.enemies.pop(0)

    # makes enemies move in the direction of the player
    def chasePlayer(mode):
        width, height = mode.enemySprite.size
        for enemy in mode.enemies:
            # if enemy to the right of player
            if enemy.locX >= mode.app.player.locX:
                enemy.locX -= mode.enemyDx
                enemyLeft = enemy.locX - width / 2 - mode.scrollX
                if mode.checkCollision(enemyLeft, enemy.locY):
                    mode.gameOver = True
            # if enemy to the left of player
            else:
                enemy.locX += mode.enemyDx
                enemyRight = enemy.locX + width / 2 - mode.scrollX
                if mode.checkCollision(enemyRight, enemy.locY):
                    mode.gameOver = True
            
            # enemies that get jumped on die
            enemyTop = enemy.locY - height / 2 
            if mode.checkStomped(enemyTop, enemy.locX - mode.scrollX):
                mode.enemies.remove(enemy)

    # checks for side collision between player and enemies/goal
    def checkCollision(mode, enemyBorder, enemyLocY):
        width, height = mode.sprite.size
        playerTop = mode.app.player.locY - height / 2
        playerLeft = mode.app.player.locX - width / 2 - mode.scrollX
        return (playerLeft <= enemyBorder <= playerLeft + width and 
                playerTop <= enemyLocY <= playerTop + height)

    # checks if player has jumped on top of an enemy
    def checkStomped(mode, enemyTop, enemyLocX):
        width, height = mode.sprite.size
        playerLeft = mode.app.player.locX - width / 2 - mode.scrollX
        playerBottom =  mode.app.player.locY + height / 2
        return (enemyTop <= playerBottom and 
                playerLeft <= enemyLocX <= playerLeft + width)

    def keyPressed(mode, event):
        if(event.key == 'r'):
            mode.restart()
        if not mode.gameOver:
            width, height = mode.background.size
            if (event.key == "Left"):
                mode.imageFlip = True   # flip image
                mode.movePlayer(-mode.moveDx) # reverse direction
                # rotates the left most copy of background to right most
                if mode.backgrounds[2].x - width/2 - mode.scrollX >= mode.width:
                    newX = mode.backgrounds[0].x - width
                    mode.backgrounds.pop()
                    mode.backgrounds.insert(0, Background(mode.app, newX))
            elif (event.key == "Right"):
                mode.imageFlip = False 
                mode.movePlayer(mode.moveDx)
                # rotates the right most copy of background to left most
                if mode.backgrounds[0].x + width / 2 - mode.scrollX <= 0:
                    newX = mode.backgrounds[2].x + width
                    mode.backgrounds.append(Background(mode.app, newX))
                    mode.backgrounds.pop(0)
            elif (event.key == 'Up'):
                mode.jump = True
                mode.peak = False

    # Copied from http://www.cs.cmu.edu/~11/notes/notes-animations-part2.html
    def movePlayer(mode, dx):
        mode.app.player.locX += dx
        mode.makePlayerVisible()

        # checks if player has reached the goal
        width, length = mode.goalSprite.size
        goalLeft = mode.goal.locX - width / 2 - mode.scrollX
        goalRight = goalLeft + width
        if (mode.checkCollision(goalLeft, mode.goal.locY) or 
            mode.checkCollision(goalRight, mode.goal.locY)):
            mode.won = True
            mode.gameOver = True

    # Copied from http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    def makePlayerVisible(mode):
        # scroll to make player visible as needed
        if (mode.app.player.locX < mode.scrollX + mode.scrollMarg):
            mode.scrollX = mode.app.player.locX - mode.scrollMarg
        if (mode.app.player.locX > mode.scrollX + mode.width - mode.scrollMarg):
            mode.scrollX = mode.app.player.locX - mode.width + mode.scrollMarg
    
    def getButtonDims(mode):
        scale = 20
        return mode.width / scale, mode.height / scale

    def mousePressed(mode, event):
        if mode.inCanvas(event.x, event.y):
            mode.restart()
            mode.app.setActiveMode(mode.app.drawMode)

    # determines if canvas button clicked
    def inCanvas(mode, x, y):
        right = mode.width - mode.margin 
        left = right - mode.buttonL
        return (left <= x <= right and 
                mode.margin <= y <= mode.margin + mode.buttonH)

    def redrawAll(mode, canvas):
        mode.drawBackground(canvas)
        mode.drawGrayMargins(canvas)
        mode.drawCanvas(canvas)
        mode.drawEnemies(canvas)
        mode.drawPlayer(canvas)
        mode.drawGoal(canvas)
        if mode.gameOver:
            mode.drawGameOver(canvas)

    def drawBackground(mode, canvas):
        # draw the background, shifted by the scrollX offset
        for background in mode.backgrounds:
            cx, cy = background.x, background.y
            cx -= mode.scrollX
            canvas.create_image(cx, cy,
                                image=ImageTk.PhotoImage(mode.background))

    def drawEnemies(mode, canvas):
        # draw the enemies, shifted by the scrollX offset
        for enemy in mode.enemies:
            cx, cy = enemy.locX, enemy.locY
            cx -= mode.scrollX
            canvas.create_image(cx, cy,
                                image=ImageTk.PhotoImage(mode.enemySprite))            

    def drawPlayer(mode, canvas):
        # draw the player, shifted by the scrollX offset
        cx, cy = mode.app.player.locX, mode.app.player.locY
        cx -= mode.scrollX
        sprite = mode.sprite
        if mode.imageFlip:
            sprite = mode.sprite.transpose(Image.FLIP_LEFT_RIGHT)
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))

    def drawGoal(mode, canvas):
        # draw the goal, shifted by the scrollX offset
        cx, cy = mode.goal.locX, mode.goal.locY
        cx -= mode.scrollX
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.goalSprite))

    # makes gray margins
    def drawGrayMargins(mode, canvas):
        topY = mode.grayMargin * 2 + mode.buttonH * 2
        canvas.create_rectangle(0, 0, mode.width, topY, fill = 'light gray')
        bottomY = mode.height - (mode.grayMargin + mode.buttonH)
        canvas.create_rectangle(0, bottomY, mode.width, mode.height, 
                                    fill = 'light gray')

        # gives instructions for the game
        margin = 80
        message = ("Use the arrow keys to move and find the goal! " + 
        "Press up to jump and kill the enemies!" )
        canvas.create_text(mode.width / 2, margin, text = message, 
                        justify = CENTER, font = 'Arial 25')

    # makes canvas button          
    def drawCanvas(mode, canvas):
        right = mode.width - mode.margin 
        left = right - mode.buttonL
        canvas.create_rectangle(left, mode.margin, right, 
                    mode.margin + mode.buttonH, fill = 'white')
        canvas.create_text(left + mode.buttonL / 2, 
                            mode.margin + mode.buttonH / 2, text = 'Canvas')

    def drawGameOver(mode, canvas):
        if mode.won: 
            canvas.create_text(mode.width / 2, mode.height / 2,
            text = 'YOU WON!', font= 'Arial 60 bold', fill = 'red')
        else:
            canvas.create_text(mode.width / 2, mode.height / 2,
                text = 'GAME OVER!', font= 'Arial 60 bold', fill = 'red')
        
        space = 50
        canvas.create_text(mode.width / 2, mode.height / 2 + space, 
                    text = "Press 'r' to replay!", font = "Arial 50 bold", 
                    fill = 'red')