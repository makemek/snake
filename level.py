class Level:
    
    def __init__(self, width, height, walls, apple):
        self.__width = width
        self.__height = height
        self.__walls = walls
        self.__apple = apple

        self.__graph = self.__generate(walls)
        self.__edges = {}
        self.placeApple(apple)

    def __generate(self, walls):
        
        dir = [ (-1,0), (1,0), (0,-1), (0,1) ]
        graph = {}

        for y in range(self.__height):
            for x in range(self.__width):
                adjList = []
                for d in dir:
                    pos = (x + d[0], y + d[1])
                    if ( (self.__withinMap(pos[0], pos[1])) and ( pos not in walls)):
                        adjList.append(pos)

                if ( (x,y) not in walls):
                    graph[(x,y)] = adjList

        return graph
                
    def placeApple(self, apple):
        self.__apple = apple
        self.__edges = self.__placeApple(apple)

    
    def __placeApple(self, apple):
        queue = []
        visited = set()
        edges = {}

        queue.append(apple)
        queue.append(apple) # parent

        # BFS
        walk = 1
        edges[(apple,apple)] = 0
        
        while(len(queue) > 0):
             
            point = queue.pop(0)
            parent = queue.pop(0)

            for p in self.__graph[point]:
                if p not in visited:
                    edges[(point, p)] = edges[(parent,point)] + 1
                    edges[(p, point)] = edges[(point, p)]
                    queue.append(p)
                    queue.append(point) # parent
                    
            
            visited.add(point)

        edges.pop((apple,apple))
        return edges

    def getLevel(self):
        return self.__edges
                
    def __withinMap(self, x, y):
        return ( x in range(self.__width)) & ( y in range(self.__height))

    def export(self, filename):
        pred = 'edge(point({}, {}), point({}, {}), {}).\n'
        applePred = 'apple(point({}, {})).\n'

        with open(filename, 'w') as file_:

            for (p1,p2), cost in self.__edges.items():
                toWrite = pred.format(p1[0], p1[1], p2[0], p2[1], cost)
                file_.write(toWrite)

            toWrite = applePred.format(self.__apple[0], self.__apple[1])
            file_.write(toWrite)

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def walls(self):
        return self.__walls

    def apple(self):
        return self.__apple