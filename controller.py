from PyQt4.QtCore import QTimer
from parse import Parser
import random

class Controller:

    def __init__(self, ui, parser, level):
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__walk)

        self.__ui = ui
        self.__parser = parser
        self.__solution = []
        self.__lvl = level

        self.__levelFile = 'C:/Users/Make/OneDrive/Study/Year 3/Artificial Intelligence/Project/Project/level.pl'

    def start(self, snake):
        self.__parser.reload()
        try:
            self.__solution = self.__parser.parse(snake)
            print(self.__solution)
        except:
            print('No solution')


        self.__ui.addSnakeParts(snake)

        if len(self.__solution) == 0:
            print("Unable to satisfy goal")
            return

        updateEvery = 500
        self.__timer.start(updateEvery)

    def __walk(self):
        reachGoal = len(self.__solution) == 0
        if reachGoal:
            self.__timer.stop()
            #self.__newApple(self.__lvl)

        else:
            direction = self.__solution.pop(0)

            self.__ui.changeSnakeDirection(direction)
            #self.__ui.moveSnake()

    def __newApple(self, level):

        snake = self.__ui.getSnake()
        self.__ui.clearSnake()

        level.placeApple(self.__randomApple(snake))
        level.export(self.__levelFile)

        self.__ui.update()
        self.__parser.reload()
        self.start(snake.getSnake())

    def __randomApple(self, snake):
        apple = self.__lvl.apple()
        while apple in self.__lvl.walls() or apple in snake.getSnake():
            appleX = random.randrange(0, self.__lvl.width())
            appleY = random.randrange(0, self.__lvl.height())
            apple = (appleX, appleY)
        
        return apple


