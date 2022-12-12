import algoConstants as const
from math import sqrt

class Index:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __ne__(self, other):
        if self.x != other.x or self.y != other.y:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

class Pixel:
    def __init__(self, index: Index, g_cost=float('inf'), h_cost=float('inf')):
        self.index = index
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = self.g_cost + self.h_cost
        self.parent = None

    def __str__(self):
        return "Index: {0} {1}, Parent: {2}".format(self.index.x, self.index.y, self.parent)

    def __repr__(self):
        return "Index: {0} {1}, Parent: {2}".format(self.index.x, self.index.y, self.parent)
    
    @staticmethod
    def compare_cost(curr: 'Pixel', prev: 'Pixel'):
        if curr.f_cost < prev.f_cost:
            return 1
        elif curr.f_cost == prev.f_cost:
            if curr.h_cost <= prev.h_cost:
                return 1
        else:
            return 0
    
    #Euclidean Distance
    def update_cost(self, parent: 'Pixel', end: 'Pixel'):
        if (parent.index.x == self.index.x or parent.index.y == self.index.y):
            self.g_cost = parent.g_cost + const.WEIGHT
        else:
            self.g_cost = parent.g_cost + const.DWEIGHT

        dx = self.index.x - end.index.x
        dy = self.index.y - end.index.y

        self.h_cost = sqrt(dx**2 + dy**2) * const.WEIGHT
        self.f_cost = self.g_cost + self.h_cost
        self.parent = parent
    
    #Diagonal Distance
    """
    def update_cost(self, parent: 'Pixel', end: 'Pixel'):
        if (parent.index.x == self.index.x or parent.index.y == self.index.y):
            self.g_cost = parent.g_cost + const.WEIGHT
        else:
            self.g_cost = parent.g_cost + const.DWEIGHT

        dx = abs(parent.index.x - end.index.x)
        dy = abs(parent.index.y - end.index.y)

        self.h_cost = const.WEIGHT * (dx + dy) + (const.DWEIGHT - 2 * const.WEIGHT) * min(dx, dy)
        self.f_cost = self.g_cost + self.h_cost
        self.parent = parent
    """
    
    #Manhattan Distance
    """
    def update_cost(self, parent: 'Pixel', end: 'Pixel'):
        if (parent.index.x == self.index.x or parent.index.y == self.index.y):
            self.g_cost = parent.g_cost + const.WEIGHT
        else:
            self.g_cost = parent.g_cost + const.DWEIGHT

        dx = abs(parent.index.x - end.index.x)
        dy = abs(parent.index.y - end.index.y)

        self.h_cost = dx + dy
        self.f_cost = self.g_cost + self.h_cost
        self.parent = parent
    """

    

