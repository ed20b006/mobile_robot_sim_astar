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

global robot_state

def get_to_goal_loop(goal_state):
    global robot_state
    
    while not control.at_goal(robot_state, goal_state):
        [V,W] = control.gtg(robot_state, goal_state)
        sim_interface.setvel_pioneers(V, W)
        time.sleep(0.5)
        robot_state = sim_interface.localize_robot()
        print(goal_state)
    

def main():
    global robot_state
    
    if (sim_interface.sim_init()):

        #Obtain handles to sim elements
        sim_interface.get_handles()

        #Extract the maze segments from the simulation, could be used in planning
        obstacles = sim_interface.get_maze_segments()
        path_plan.get_obstacle_data(obstacles)

        #Start simulation
        if (sim_interface.start_simulation()):
            
            #Stop robot
            sim_interface.setvel_pioneers(0.0, 0.0)

            #Obtain goal state
            goal_state = sim_interface.get_goal_pose()

            #Obtain robots position
            robot_state = sim_interface.localize_robot()
            path_plan.get_source_data(robot_state, goal_state)
            path_plan.plot_map()
            path = path_plan.plan_path()
            path_plan.plot_map()
            print(path)
            local_goal = path.pop()
            get_to_goal_loop(local_goal)
            
            while len(path) > 0:
                local_goal = path.pop()
                get_to_goal_loop(local_goal)
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
            

 