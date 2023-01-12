#!/usr/bin/env python

"""
Mobile robot simulation setup
@author: Bijo Sebastian 
"""

#Import libraries
import time

#Import files
import sim_interface
import control
import path_plan
from optimizer import Obstacle

global robot_state
global goal_state

no_obstacle = 2

def get_to_goal_loop(next_state):
    global robot_state
    global goal_state
    global obstacleData
    
    while not control.at_goal(robot_state, next_state):
        if ((goal_state[0] - robot_state[0])**2 + (goal_state[1] - robot_state[1])**2) < ((next_state[0] - goal_state[0])**2 + (next_state[1] - goal_state[1])**2):
            print("skip")
            return
        [V,W] = control.gtg(robot_state, goal_state, next_state, obstacleData)
        sim_interface.setvel_pioneers(V, W)
        time.sleep(0.5)
        robot_state = sim_interface.localize_robot()
        for i in range(no_obstacle):
            obstacles_state = sim_interface.localize_obstacle(i)
            obstacleData[i].x = obstacles_state[0]
            obstacleData[i].y = obstacles_state[1]
            obstacleData[i].theta = obstacles_state[2]
            
        print(next_state)
        print("")
    

def main():
    global robot_state
    global goal_state
    global obstacleData
    obstacleData = []
    
    
    if (sim_interface.sim_init()):

        #Obtain handles to sim elements
        sim_interface.get_handles()
        sim_interface.get_dynamic_obstacles(no_obstacle)

        #Extract the maze segments from the simulation, could be used in planning
        obstacles = sim_interface.get_maze_segments()
        path_plan.get_obstacle_data(obstacles)

        #Start simulation
        if (sim_interface.start_simulation()):
            
            #Stop robot
            sim_interface.setvel_pioneers(0.0, 0.0)
            for i in range(no_obstacle):
                obstacleData.append(Obstacle(0.0, 0.0, 0.0, 0.1, -0.3))
                sim_interface.setvel_obstacle(obstacleData[i].v, obstacleData[i].w, i)

            #Obtain goal state
            goal_state = sim_interface.get_goal_pose()

            #Obtain robots position
            robot_state = sim_interface.localize_robot()
            
            for i in range(no_obstacle):
                obstacles_state = sim_interface.localize_obstacle(i)
                obstacleData[i].x = obstacles_state[0]
                obstacleData[i].y = obstacles_state[1]
                obstacleData[i].theta = obstacles_state[2]
            
            path_plan.get_source_data(robot_state, goal_state)
            path_plan.plot_map()
            path_plan.plan_path()
            path_plan.plot_map()
            print(path_plan.path)
            local_goal = path_plan.get_next_point()
            #get_to_goal_loop(local_goal)
            
            while len(path_plan.path) > 0:
                local_goal = path_plan.get_next_point()
                get_to_goal_loop(local_goal)
                for i in range(no_obstacle):
                    obstacles_state = sim_interface.localize_obstacle(i)
                print("\n\nSubPoint Covered\n\n")
            
            get_to_goal_loop(goal_state)

            #Stop robot
            sim_interface.setvel_pioneers(0.0, 0.0)

        else:
            print ('Failed to start simulation')
    else:
        print ('Failed connecting to remote API server')
    
    #stop robots
    sim_interface.setvel_pioneers(0.0, 0.0)
    sim_interface.sim_shutdown()
    time.sleep(2.0)
    return

#run
if __name__ == '__main__':

    main()                    
    print ('Program ended')
            

 