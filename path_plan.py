import numpy as np
import matplotlib.pyplot as plt
import algoConstants as aconst
import Algorithm as algo

global mapData

def get_obstacle_data(data):
    global mapData
    mapData = np.zeros((26,26))
    for wall in data:
        print("Wall position:")
        print(wall)
        mapData = set_wall(mapData, wall[0], wall[1], wall[2], wall[3])
    
    
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
    mapData[int(start[1])][int(start[0])] = aconst.START
    mapData[int(stop[1])][int(stop[0])] = aconst.END
    
def plan_path():
    global mapData
    
    myAlgo = algo.AStarAlgorithm(mapData)
    myAlgo.alogo_exec()
    return myAlgo.path
    
    
    
    
    
    
    
    
    
    
    
    
    
    