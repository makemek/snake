#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------
from random import randint
#---------------------------------------------
class Apple:
    def __init__(self, x = 0, y = 0):
        self.__applePosition = (x, y)

    def generateApple(self, X_limit, Y_limit, criteria):
        newX = randint(0, X_limit - 1)
        newY = randint(0, Y_limit - 1)

        while (newX, newY) in criteria:
            newX = randint(0, X_limit - 1)
            newY = randint(0, Y_limit - 1)

        self.setApplePos(newX, newY)
        return (newX, newY)

    def getApplePos(self):
        return self.__applePosition

    def gotEaten(self, x, y):
        return x == self.__applePosition[0] and y == self.__applePosition[1]

    def setApplePos(self, x, y):
        self.__applePosition = (x, y)
