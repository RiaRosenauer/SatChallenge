#calculating the orbit of a sattelite projected onto earth


import math
import matplotlib.pyplot as plt
import numpy as np


#physical constants
M_sun =1.989*10**(30) #in kg
G = 6.67430*10**(-11) 
Omega = math.pi*2/(24*60*60) # Earth rotation velocity
 


#important 'basic' functions
def velocity(height):
    #in m/s
    return M_sun*G/height

def period(height):
    return 2*math.pi*height/velocity(height)

def sphere_tocart(r, theta, phi):
    return r*np.sin(theta)*np.cos(phi), r*math.sin(theta)*math.sin(phi), r*sin(theta)

def cart_tosphere(x,y,z):
    r = math.sqrt((x**2 + y**2 + z**2))
    return r, np.arccos(z/r) ,math.atan2(x,y)


height = 42000*10**(3) #in m vom Erdmittelpunkt
alpha = math.pi/2 #in Grad (Winkel der Rotationsebene zur z-Achse)
granularity = 100
T_max = 10000


T = period(height)
#omega = 2*math.pi/T
omega = math.pi*2/(24*60*60)

#rotation vectors
def R_x(theta):
    return np.array([[1,0,0],[0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])

def r_vec(t, w):
    return np.array([np.sin(w * t), np.cos(w * t), 0])



#calculate r, theta, phi depening on time
def timeEvolution(t, alpha, w):
    #R_x(alpha).dot(r_vec(t))
    r, theta, phi = cart_tosphere( *(R_x(alpha).dot(r_vec(t, w))))
    phi -= Omega * t 
    return theta, phi % 2*np.pi

#returns arrays of theta and phi
def get_orbits(height, alpha, omega, granularity, T_max):
    phi_arr = []
    theta_arr = []
    for t in range(T_max):
        theta, phi = timeEvolution(t/granularity, alpha, omega)
        phi_arr.append(phi)
        theta_arr.append(theta)
    return phi_arr, theta_arr

def plot_orbits(phi_arr, theta_arr):
    img = plt.imread("Equirectangular_projection_SW.jpg")

    plt.figure(figsize = (20,10))
    plt.imshow(img, extent=[0, 2*math.pi, 0, math.pi])  
    plt.scatter(phi_arr, theta_arr, color='firebrick', s = 20)
    plt.show()


phi_arr, theta_arr = get_orbits(height, alpha, omega, granularity, T_max)
plot_orbits(phi_arr, theta_arr)
