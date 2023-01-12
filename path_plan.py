import numpy as np
import matplotlib.pyplot as plt
import algoConstants as aconst
import Algorithm as algo

global mapData
global path
global scale
scale = 1

def get_obstacle_data(data):
    global mapData
    global scale
    mapData = np.zeros((26*scale,26*scale))
    for wall in data:
        print("Wall position:")
        print(wall)
        mapData = set_wall(mapData, wall[0]*scale, wall[1]*scale, wall[2]*scale, wall[3]*scale)
    
def plot_map():
    global mapData
    plt.title("pixel_plot")
    pixel_plot = plt.imshow(mapData,interpolation='nearest',origin='lower')
    plt.colorbar(pixel_plot)
    plt.show(pixel_plot)

def set_wall(data, xs, ys, xe, ye):
    step = 50
    if xe != xs:
        slope = (ye - ys)/(xe - xs)
        stepx = (xe - xs)/step
        for xp in np.arange(xs, xe, stepx):
            yp = slope * (xp - xs) + ys
            data[int(yp)][int(xp)] = aconst.OBSTACLE
    else:
        stepy = (ye - ys)/step
        for yp in np.arange(ys, ye, stepy):
            data[int(yp)][int(xs)] = aconst.OBSTACLE
    return data

def get_source_data(start, stop):
    global mapData
    mapData[int(start[1] * scale)][int(start[0] * scale)] = aconst.START
    mapData[int(stop[1] * scale)][int(stop[0] * scale)] = aconst.END
    
def plan_path():
    global mapData
    global path
    
    myAlgo = algo.AStarAlgorithm(mapData)
    myAlgo.alogo_exec()
    path = myAlgo.path

def get_next_point():
    global path
    return [ x/scale for x in path.pop()]
    
    
    
    
    
    
    
    
    
    
    
    
    
    