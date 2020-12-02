

def ExportLevel():

    #lvl = Level(5,5,[(1,0), (1,1), (1,2), (1,3), (3,1), (3,2), (3,3), (3,4)],(0,0))
    #lvl.export('lvl_5x5_zigzag.pl')

    #lvl_2x2 = Level(2,2, [], (1,0))
    #lvl_2x2.export('lvl_2x2.pl')

    #lvl_4x4_wallMid = Level(4,4, [(1,1), (1,2), (2,1), (2,2)], (0,3))
    #lvl_4x4_wallMid.export('lvl_4x4_wallMid.pl')

    #lvl_4x4 = Level(4,4, [], (0,3))
    #lvl_4x4.export('lvl_4x4.pl')

    #print('Export Successfully!')
    pass

def generateMap(ui, walls, apple):

    for wall in walls:
        ui.addWall(wall[0], wall[1])

    ui.generateApple(apple[0], apple[1])
    return ui

def main():
    app = QApplication(sys.argv)

    width = 3
    height = 3
    walls = [ ]
    apple = (1,0)
    snake = [(0,1)]

    ui = SnakeGame(1024, 576, width, height)
    ui = generateMap(ui, walls, apple)

    # create & export level
    address = 'C:/Users/Make/OneDrive/Study/Year 3/Artificial Intelligence/Project/Project/'
   
    print("Exporting knowledge bases")
    level = Level(width, height, walls, apple)
    level.export(address + 'level.pl')
    print('Export Success!')
    

    parser = Parser(address + 'controller.pl')
    controller = Controller(ui, parser, level)
    controller.start(snake)

    app.exec_()

if __name__ == '__main__':
    from level import Level
    from parse import Parser
    from controller import Controller
    from SnakeGame import SnakeGame
    from PyQt4.QtGui import QApplication
    import time
    import sys
    main()

