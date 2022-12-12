import numpy as np
import algoConstants as const
from Pixel import Pixel, Index
from matplotlib import pyplot as plt

class AStarAlgorithm:
    def __init__(self, data):
        self.data = data
        (self.start, self.end) = self.get_sources()
        self.open_list = [Pixel(index=self.start,g_cost=0,h_cost=0)]
        self.closed_list: list[Pixel] = []
        self.path = []

    def get_sources(self):
        start = np.where(self.data == const.START)
        end = np.where(self.data == const.END)
        
        return (Index(start[0], start[1]), Index(end[0], end[1]))

    def alogo_exec(self):
        plt.ion()
        while not len(self.open_list) == 0:
            # find the node with the least f on the open list
            temp = 0
            for i, node in enumerate(self.open_list):
                if Pixel.compare_cost(node, self.open_list[temp]): #node.f_cost < self.open_list[temp].f_cost
                    temp = i

            curr_node = self.open_list.pop(temp)

            # generate q's 8 successors and set their parents to q
            successor = []
            for i in range(3):
                for j in range(3):
                    x = curr_node.index.x + i - 1
                    y = curr_node.index.y + j - 1
                    
                    if not(curr_node.index.x == x and curr_node.index.y == y) and x > 0 and y > 0:
                        
                        if x == self.end.x and y == self.end.y:
                            plt.close()
                            self.get_path(curr_node)
                            return
                        
                        s = Pixel(index=Index(x, y))
                        s.update_cost(parent=curr_node, end=Pixel(self.end))
                        successor.append(s)

            for si, sn in enumerate(successor):
                poplist = False
                for oi, on in enumerate(self.open_list):
                    if on.index.x == sn.index.x and on.index.y == sn.index.y:
                        if Pixel.compare_cost(sn, on): #on.f_cost > sn.f_cost
                            self.open_list[oi] = sn
                        poplist = True

                for ci, cn in enumerate(self.closed_list):
                    if cn.index.x == sn.index.x and cn.index.y == sn.index.y and Pixel.compare_cost(cn, sn): #cn.f_cost < sn.f_cost
                        poplist = True
                if poplist == False and self.data[sn.index.x[0]][sn.index.y[0]] != const.OBSTACLE:
                    self.open_list.append(sn)
                    if sn.index != self.start and sn.index != self.end:
                        self.data[sn.index.x[0]][sn.index.y[0]] = const.OPEN


            self.closed_list.append(curr_node)
            if curr_node.index != self.start and curr_node.index != self.end:
                self.data[curr_node.index.x[0]][curr_node.index.y[0]] = const.CLOSE
            #print("open list: ")
            #print(len(self.open_list))
            #print("closed list: ")
            #print(len(self.closed_list))
            #plt.clf()
            #plt.imshow(self.data, interpolation='nearest')
            #plt.plot()
            #plt.pause(0.01)

    def get_path(self, last: 'Pixel'):
        temp = last
        plt.ion()
        while temp.parent != None:
            self.data[temp.index.x[0]][temp.index.y[0]] = const.START
            self.path.append([float(temp.index.y[0]), float(temp.index.x[0]), 0.0])
            temp = temp.parent