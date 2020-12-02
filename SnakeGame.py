#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------
# 1. Import Modules
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from snake import *
from apple import *
from wall import *

from time import sleep

#---------------------------------------------
# 2. Constants
TITLE = "Snake AI Project"
APPLE = 'image/apple.png'
WALL = 'image/wall.png'
SNAKE = {'bd':'image/snake_body_down.png',\
         'bl':'image/snake_body_left.png',\
         'br':'image/snake_body_right.png',\
         'bu':'image/snake_body_up.png',\
         'hd':'image/snake_head_down.png',\
         'hl':'image/snake_head_left_.png',\
         'hr':'image/snake_head_right_.png',\
         'hu':'image/snake_head_up_.png',\
         'td':'image/snake_tail_down_.png',\
         'tl':'image/snake_tail_left_.png',\
         'tr':'image/snake_tail_right_.png',\
         'tu':'image/snake_tail_up_.png',\
         'dl':'image/snake_down_left_.png',\
         'dr':'image/snake_down_right_.png',\
         'ul':'image/snake_up_left_.png',\
         'ur':'image/snake_up_right_.png' }
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
#---------------------------------------------
# 3. Class
class SnakeGame(QWidget):
    def __init__(self, width, height, cols, rows, parent = None):
        super(SnakeGame, self).__init__(parent)

        self.__width = width
        self.__height = height
        self.__col = cols
        self.__row = rows
        self.__blockWidth = self.__width / self.__col
        self.__blockHeight = self.__height / self.__row
        
        self.clearSnake()
        self.setupTable()
        self.setupWidget()
        self.setupWall()
        self.setupApple()
        self.setupTimer()
        self.show()

    def setupWidget(self):
        layout = QVBoxLayout(self)

        self.setWindowTitle(TITLE)
        self.setMinimumSize(self.__width, self.__height)
        self.setMaximumSize(self.__width, self.__height)

        layout.addWidget(self.__table)
        layout.setMargin(0)
        self.setLayout(layout)

    def setupTable(self):
        self.__table = QTableWidget(self.__row, self.__col, self)

        # Table Rows
        self.__table.verticalHeader().setVisible(False)
        for i in range(self.__row):
            self.__table.setRowHeight(i, self.__blockHeight)
        # Table Column
        self.__table.horizontalHeader().setVisible(False)
        for i in range(self.__col):
            self.__table.setColumnWidth(i, self.__blockWidth)

        self.__table.setContentsMargins(0, 0, 0, 0)
        self.__table.setAutoScroll(False)
        self.__table.setShowGrid(False)
        self.__table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__table.setSelectionMode(QAbstractItemView.NoSelection)
        #self.__table.setDisabled(True)

    def setupSnake(self):
        tempBlockX = round(self.__col / 2)
        tempBlockY = round(self.__row / 2)
        self.__snake = Snake(LEFT,\
                              [(tempBlockX, tempBlockY),\
                              (tempBlockX + 1, tempBlockY),\
                              (tempBlockX + 2, tempBlockY)])

        for i in range(3):
            snakeImage = QPixmap('image/snake.png').scaled(self.__blockWidth, self.__blockHeight)
            snakeCell = QTableWidgetItem()
            snakeCell.setData(Qt.DecorationRole, snakeImage)
            self.__table.setItem(tempBlockY, tempBlockX + i, snakeCell)

    def setupApple(self):
        self.__apple = Apple()

    def setupWall(self):
        self.__walls = Walls()

    def setupTimer(self):
        self.__repeater = QTimer()
        self.__repeater.timeout.connect(self.begin)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Up:
            self.__snake.changeDirection(UP)
        elif e.key() == Qt.Key_Down:
            self.__snake.changeDirection(DOWN)
        elif e.key() == Qt.Key_Left:
            self.__snake.changeDirection(LEFT)
        elif e.key() == Qt.Key_Right:
            self.__snake.changeDirection(RIGHT)

    def startgame(self, speed):
        self.generateApple()
        self.__repeater.start(speed)

    def begin(self):
        if self.gameOver():
            self.__repeater.stop()
            return None

        self.moveSnake()
        
        headPosition = self.__snake.getSnakeHead()
        if self.__apple.gotEaten(headPosition[0], headPosition[1]):
            self.generateApple()
            self.__snake.grow()

    def generateApple(self, X = None, Y = None):
        apple = self.__apple.getApplePos()
        appleCell = QTableWidgetItem()
        appleCell.setData(Qt.DecorationRole,\
                          QPixmap(APPLE).scaled(\
                                                self.__blockWidth,\
                                                self.__blockHeight))

        if X != None and Y != None:
            self.__table.takeItem(apple[1], apple[0])
            apple = self.__apple.setApplePos(X, Y)
        else:
            apple = self.__apple.generateApple(self.__col, self.__row, self.__snake.getSnake())
        apple = self.__apple.getApplePos()
        self.__table.setItem(apple[1], apple[0], appleCell)

    def moveSnake(self):
        tail = self.__snake.move()

        if tail is not None:
            self.__table.takeItem(tail[1], tail[0])
        if (self.__snake.getSnake()) != 0:
            snakeImage = QPixmap('image/snake.png').scaled(self.__blockWidth, self.__blockHeight)
            snakeCell = QTableWidgetItem()
            snakeCell.setData(Qt.DecorationRole, snakeImage)

            snakePosition = self.__snake.getSnakeHead()
            self.__table.setItem(snakePosition[1], snakePosition[0], snakeCell)
        

    def gameOver(self):
        head = self.__snake.getSnakeHead()

        # Check for the collision with the wall
        crash = head[0] < 0 or\
                head[0] >= self.__col or\
                head[1] < 0 or\
                head[1] >= self.__row
        
        # Check for the collision with itself
        if not crash:
            crash = self.__snake.gotCrashed()

        if not crash:
            snake_head = self.__snake.getSnakeHead()
            crash = self.__walls.gotCrashed(snake_head[0], snake_head[1])

        return crash

    def changeSnakeDirection(self, newDirection):
        self.__snake.changeDirection(newDirection)
        self.moveSnake()

    def addWall(self, x, y):
        if 0 <= x < self.__col and 0 <= y < self.__row:
            wallCell = QTableWidgetItem()
            wallCell.setData(Qt.DecorationRole,\
                              QPixmap(WALL).scaled(\
                                                    self.__blockWidth,\
                                                    self.__blockHeight))
            self.__table.setItem(y, x, wallCell)
            self.__walls.addWallBlock(x, y)

    def removeWall(self, x, y):
        if (x,y) in self.__walls:
            self.__table.takeItem(y, x)

    def addSnakePart(self, x, y):
        self.__snake.addSnakePart(x, y)

        snakeImage = QPixmap('image/snake.png').scaled(self.__blockWidth, self.__blockHeight)
        snakeCell = QTableWidgetItem()
        snakeCell.setData(Qt.DecorationRole, snakeImage)
        self.__table.setItem(y, x, snakeCell)

    def addSnakeParts(self, parts):
        for i in range(len(parts)):
            self.__snake.addSnakePart(parts[i][0], parts[i][1])

            snakeImage = QPixmap('image/snake.png').scaled(self.__blockWidth, self.__blockHeight)
            snakeCell = QTableWidgetItem()
            snakeCell.setData(Qt.DecorationRole, snakeImage)
            self.__table.setItem(parts[i][1], parts[i][0], snakeCell)

    def clearSnake(self):
        self.__snake = Snake()

    def getCurrentDirection(self):
        return self.__snake.getDirection()

    def getWalls(self):
        return self.__walls

    def getApple(self):
        return self.__apple.getApplePos()

    def getFieldSize(self):
        return (self.__col, self.__row)

    def getSnake(self):
        return self.__snake