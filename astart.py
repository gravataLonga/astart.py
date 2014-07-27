'''
aStart algoritm, done by: Jonathan Fontes - Portugal - jonathanfontes.pt

'''


from sets import Set
import logging


class Node:
    '''
    Define node in the map
    '''
    def __init__(self, x, y, typeNode):
        self.x = x
        self.y = y
        self.typeNode = typeNode
        self.g = 0
        self.f = 0
        self.walkable = True
        self.father = None
        self.cost = 10 # default cost to this node
        logging.debug(self)

    def __str__(self):
        return "Type of Node: {}, x: {}, y: {} ".format(self.typeNode, x, y)

    def setFather(self, node):
        self.father = node

    def setF(self, h):
        self.f = self.g + h

    def setG(self, g):
        self.g = g

    def isWalkable(self):
        return self.walkable

    def notWalkable(self):
        self.walkable = False

class AStar:

    def __init__(self, nodes, xStart, yStart, xEnd, yEnd):
        self.nodes = nodes
        self.opens = Set()
        self.closes = Set()
        self.setStartPoint(xStart, yStart)
        self.setEndPoint(xEnd, yEnd)
        self.find = True
        self.main()

    def main(self):
        '''
        Resolving the path from start to end. 
        @todo: When can't resolve the path, give an error. Resolving...
        '''
        current_node = self.begin

        # Debug Porpose...
        logging.info("Current Node: {}".format(current_node))
        logging.info("Start point: {}".format(self.begin))
        logging.info("End point: {}".format(self.end))

        while current_node != self.end:
            # Adicionar o quadro aos fechados.
            self.closes.add(current_node)
            self.opens.remove(current_node)
            # Getting neighhbord
            self.neighbors(current_node)
            # move to lowest cost
            t = self.lowestCost()
            if t is None:
                self.find = False
            else:
                current_node = t

        # Now getting the final path
        n = current_node
        self.path = []
        while n.father != None:
            self.path.append((n.x, n.y))
            n = n.father

    def  get(self):
        '''
        Return the path
        @todo: check if we got a path.
        '''
        return self.path

    def setStartPoint(self, x, y):
        '''
        Start point to search
        '''
        self.begin = self.nodes[x,y]
        self.opens.add(self.begin)

    def setEndPoint(self, x, y):
        '''
        Set the target.
        '''
        self.end = self.nodes[x,y]

    def heuristica(self, node):
        '''
        Our heuristh to calculate the cost of path
        '''
        h = (abs(node.x - self.end.x) + abs(node.y - self.end.y))
        return h

    def lowestCost(self):
        '''
        return the node with lowest f cost
        @todo: study if we need min = 1000000
        '''
        min = None
        min_n = None
        for n in self.opens:
            
            # to study
            if min is None:
                min = n.f

            if n == self.end:
                return n
            if n.f < min:
                min_n = n
                min = n.f
        return min_n


    def neighbors(self, node):
        '''
        Not accept diagonal
        '''
        x   = node.x
        y   = node.y
        # todo: 
        square = [[0,-1],[-1,0], [1,0],[0,1]]

        for pos in square:
            n = self.nodes[x + pos[0], y + pos[1]]
            # todo: change this to accept more options to non-walkvable
            if n.isWalkable() == False or n in self.closes:
                pass
            else:
                if n not in self.opens:
                    n.setFather(node)
                    n.setG(node.g + n.cost) 
                    n.setF(self.heuristica(n))
                    self.opens.add(n)
                else:
                    if n.g < node.g:
                        n.setFather(node)
                        n.setG(node.g + n.cost) 
                        n.setF(self.heuristica(n))
                        self.opens.add(n)
                    else:
                        pass

