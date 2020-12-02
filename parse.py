from pyswip import Prolog


class Parser:

    def __init__(self, consultFile):
        self.__intf = Prolog()
        self.__consultFile = consultFile
        self.reload()
        

    def reload(self):
        self.__intf.consult(self.__consultFile)

    def parse(self, snake):
        
        solution = 'Path'
        query = 'solve([{}], {})'
        

        point = 'point({}, {}),'
        points = ''
        for joint in snake:
            points = points + point.format(joint[0], joint[1])

        points = points[:-1]
        query = query.format(points, solution)
        
        print(query)

        sol = self.__intf.query(query)
        result = sol.next()
        sol.close()

        
        
        return self.__interpretSolution(result[solution])        
    
    def __interpretSolution(self, solution):

        if len(solution) == 0:
            return solution

        for idx in range(len(solution)):
            solution[idx] = solution[idx].chars
        solution.reverse()

        return solution

    def getConsultFile(self):
        return self.__consultFile