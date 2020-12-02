#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
#---------------------------------------------
class Snake:
    def __init__(self, body = None):
        self.__snake = []
        self.__direction = None
        self.__grow = False

        if body is not None:
            try:
                for i, j in body:
                    self.addSnakePart(i, j)
            except ValueError:
                pass

    def addSnakePart(self, x, y):
        self.__snake.append((x, y))

    def changeDirection(self, newDirection):
        if newDirection in [UP, DOWN, LEFT, RIGHT] and\
           ((self.__direction == UP and newDirection != DOWN) or\
           (self.__direction == LEFT and newDirection != RIGHT) or\
           (self.__direction == RIGHT and newDirection != LEFT) or\
           (self.__direction == DOWN and newDirection != UP) or\
           (self.__direction == None)):
            self.__direction = newDirection

    def deleteSnakePart(self, x, y):
        try:
            self.__snake.remove((x, y))
        except ValueError:
            pass

    def getDirection(self):
        return self.__direction

    def getSnake(self):
        return self.__snake

    def getSnakeHead(self):
        return self.__snake[0]

    def gotCrashed(self):
        for i in self.__snake[1:]:
            if self.__snake[0][0] == i[0] and self.__snake[0][1] == i[1]:
                return True
        return False

    def grow(self):
        self.__grow = True

    def isGrowing(self):
        return self.__grow

    def move(self):
        if self.__direction == LEFT:
            newHead = (self.__snake[0][0] - 1, self.__snake[0][1])

        elif self.__direction == RIGHT:
            newHead = (self.__snake[0][0] + 1, self.__snake[0][1])

        elif self.__direction == DOWN:
            newHead = (self.__snake[0][0], self.__snake[0][1] + 1)

        elif self.__direction == UP:
            newHead = (self.__snake[0][0], self.__snake[0][1] - 1)


        if self.__direction != None:
            self.__snake.insert(0, newHead)

        if self.__grow:
            self.__grow = False
            return None

        return self.__snake.pop()