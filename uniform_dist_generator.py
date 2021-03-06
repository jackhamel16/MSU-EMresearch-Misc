""" 
Generates a dot distribution using a uniform random distribution
"""

import random
import numpy as np

def write_file(dot_x,dot_y,dot_z,tf,dc1,dc2,ds,dx,dy,dz):
    """
    Writes dot distribution to a file.
    dots are lists that correspond with each other to one dot position
    rest are ints/floats
    """
    file_name = input("Enter save name: ")
    file = open(file_name, "w")
    
    for i,dot in enumerate(dot_x):
        print("{:15.8f}{:15.8f}{:15.8f}{:15.8f}{:15.8f}{:15.8f}{:15.8f}\
        {:15.8f}{:15.8f}{:15.8f}".format(dot_x[i],dot_y[i],dot_z[i]\
        ,tf,dc1,dc2,ds,dx,dy,dz),file = file)
    file.close()
    
def generate_dot(x_lower, x_upper, y_lower, y_upper, z_lower, z_upper):
    """
    generates a dot with a three coordinate position
    returns position as length three tuple
    """
    # Function not used atm. function below is better at the moment
    return random.uniform(x_lower,x_upper), random.uniform(y_lower,y_upper),\
    random.uniform(z_lower, z_upper)
    
def generate_dots(size, count):
    """
    Generates dots in a 3 column array as x,y,z. distributed in cube centered\
    on origin
    size is the size of the cube
    count is the number of dots
    """
    return np.random.uniform(-size/2, size/2, (count, 3)) 
    
def calculate_timestep(dipole_mag, distance):
    """
    Calculates the timestep for simulation using rabi frequency
    dipole_mag is the magnitude of the dipole
    distance is seperation between two dots
    returns timestep
    """
    hbar = 0.658211928
    mu0 = 2.013354451e-4
    
    rabi = dipole_mag**2/(hbar * distance**3) * mu0/(4 * np.pi)
    
    return 1/(20 * rabi)

def calculate_min_distance(dot_array):
    """
    Calculates the minimum distance between two dots in the distribution
    dot_array n x 3 array of dot positions
    returns minimum distance
    """
    min_distance = 10000000 # Needs to be a value greater than the likely min distance
    
    for dot in dot_array:
        x_dot,y_dot,z_dot = dot[0],dot[1],dot[2]
        for dot in dot_array:
            x_dist = x_dot - dot[0]
            y_dist = y_dot - dot[1]
            z_dist = z_dot - dot[2]
            distance = np.sqrt(x_dist**2+y_dist**2+z_dist**2)
            if (distance != 0) and distance < min_distance:
                min_distance = distance
                
    return min_distance
            
    
def build_uniform_file(size, count):
    """
    creates a uniform distribution of dots in a cube centered at origin
    size is length of one side of the cube
    count is the number of dots in the cube
    returns array of dot positions for user benefit
    note: keep density below 2400 or add in minimum distance enforcement
    """    
    TRANS_FREQ = 2278.9013 
    DECAY1 = 10
    DECAY2 = 10
    DIPOLE_STR = 5.2917721e-4
    DIPOLE_X = 1
    DIPOLE_Y = 0
    DIPOLE_Z = 0

    dot_array = generate_dots(size, count)

    x_list = [row[0] for row in dot_array]
    y_list = [row[1] for row in dot_array]
    z_list = [row[2] for row in dot_array]

    min_distance = calculate_min_distance(dot_array)
    timestep = calculate_timestep(DIPOLE_STR, min_distance)
    
    print("Max Timestep: "+str(timestep))
    write_file(x_list,y_list,z_list,TRANS_FREQ,DECAY1,DECAY2,\
    DIPOLE_STR,DIPOLE_X,DIPOLE_Y,DIPOLE_Z)
    