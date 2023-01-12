import robot_params
import numpy as np 
from optimizer import Optimizer

prev_heading_error = 0.0
total_heading_error = 0.0

def at_goal(robot_state, goal_state):    
    
    #check if we have reached goal point
    d = np.sqrt(((goal_state[0] - robot_state[0])**2) + ((goal_state[1] - robot_state[1])**2))
    
    if d <= robot_params.goal_threshold:
        print("Reached goal")
        return True
    else:
        return False

def gtg(robot_state, goal_state, next_state, allObstacles):  
    #The Go to goal controller
    print("gtg")
    global prev_heading_error
    global total_heading_error
    global opt
    
    #Controller parameters
    Kp = 0.00656
    Kd = 0.0001
    Ki = 0.0
    dt = 0.5

    #determine how far to rotate to face the goal point
    #PS. ALL ANGLES ARE IN RADIANS
    delta_theta = (np.arctan2((next_state[1] - robot_state[1]), (next_state[0] - robot_state[0]))) - robot_state[2]
    #restrict angle to (-pi,pi)
    delta_theta = ((delta_theta + np.pi)%(2.0*np.pi)) - np.pi
    
    #Error is delta_theta in degrees
    e_new = ((delta_theta*180.0)/np.pi)
    e_dot = (e_new - prev_heading_error)/dt
    total_heading_error = (total_heading_error + e_new)*dt
    #control input for angular velocity
    W = (Kp*e_new) + (Ki*total_heading_error) + (Kd*e_dot)
    prev_heading_error = e_new
  
    #find distance to goal
    d = np.sqrt(((goal_state[0] - robot_state[0])**2) + ((goal_state[1] - robot_state[1])**2))
    
    #velocity parameters
    distThresh = 0.1#mm
    
    #control input for linear velocity
    V = (0.12/1.5)*(np.arctan(d - distThresh))
    
    opt = Optimizer(robot_state[0], robot_state[1], robot_state[2], V, W)
    for obs in allObstacles:
        opt.get_obstacle(obs)
        opt.goal.x = goal_state[0]
        opt.goal.y = goal_state[1]
    
    if opt.obstacles:
        V, W = ao(robot_state, goal_state)
        
    
    #request robot to execute velocity
    return[V,W]

def ao(robot_state, goal_state):
    print("ao")
    global prev_heading_error
    global total_heading_error
    global opt
    
    #Controller parameters
    Kp = 0.00656
    Kd = 0.0001
    Ki = 0.0
    dt = 0.5

    #determine how far to rotate to face the goal point
    #PS. ALL ANGLES ARE IN RADIANS
    delta_theta = (np.arctan2((goal_state[1] - robot_state[1]), (goal_state[0] - robot_state[0]))) - robot_state[2]
    #restrict angle to (-pi,pi)
    delta_theta = ((delta_theta + np.pi)%(2.0*np.pi)) - np.pi
    
    #Error is delta_theta in degrees
    e_new = ((delta_theta*180.0)/np.pi)
    e_dot = (e_new - prev_heading_error)/dt
    total_heading_error = (total_heading_error + e_new)*dt
    #control input for angular velocity
    W = (Kp*e_new) + (Ki*total_heading_error) + (Kd*e_dot)
    prev_heading_error = e_new
  
    #find distance to goal
    d = np.sqrt(((goal_state[0] - robot_state[0])**2) + ((goal_state[1] - robot_state[1])**2))
    
    #velocity parameters
    distThresh = 0.1#mm
    
    #control input for linear velocity
    V = (0.12/1.5)*(np.arctan(d - distThresh))
    opt.V = V
    opt.W = W
    sol = opt.optimize()
    
    return sol[0], sol[1]
    
                                       
                   
