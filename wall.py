class Walls:
    def __init__(self, locations = None):
        self.__walls = []

        if locations is not None:
            try:
                for i, j in locations:
                    self.__snake.addWallBlock(i, j)
            except ValueError:
                pass

    def addWallBlock(self, x, y):
        if type(x) is int and type(y) is int:
            self.__walls.append((x, y))

    def gotCrashed(self, x, y):
        for i in self.__walls:
            if x in i and y in i:
                return True
        return False