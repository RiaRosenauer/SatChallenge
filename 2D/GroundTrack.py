#calculating the orbit of a sattelite projected onto earth
import math
import matplotlib.pyplot as plt
import numpy as np
import itertools


#physical constants
M_earth =5.97*(10**(24)) #in kg
G = 6.67430*(10**(-11))
Omega = math.pi*2/(24*60*60) # Earth rotation angular velocity; earth rotating aroung z-axis
 

#important 'basic' functions
def velocity(height):
    #in m/s
    return math.sqrt(M_earth*G/height)

def period(height):
    return 2*math.pi*height/velocity(height)

def sphere_tocart(r, theta, phi):
    return r*np.sin(theta)*np.cos(phi), r*math.sin(theta)*math.sin(phi), r*math.cos(theta)

def cart_tosphere(x,y,z):
    r = math.sqrt((x**2 + y**2 + z**2))
    return r, np.arccos(z/r) ,math.atan2(y,x)


#rotation vectors
def R_x(theta):
    return np.array([[1,0,0],[0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])

def r_vec(t, w):
    return np.array([np.sin(w * t), np.cos(w * t), 0])

#ensuring the right modulo of phi-omega*t
def convert_angle(angle):
    while angle <= 0:
        angle = angle + 2*math.pi
    return angle


#calculate r, theta, phi depening on time
def timeEvolution(t, alpha, w):
    #R_x(alpha).dot(r_vec(t))
    r, theta, phi = cart_tosphere( *(R_x(alpha).dot(r_vec(t, w))))
    phi2 =  convert_angle(phi - Omega * t)
    return theta, phi2

#returns arrays of theta and phi
def get_orbits(height, alpha, omega, granularity, T_max):
    phi_arr = []
    theta_arr = []

    for t in np.linspace(0, T_max, granularity):
        theta, phi = timeEvolution(t, alpha, omega)
        phi_arr.append(phi)
        theta_arr.append(theta)

    return phi_arr, theta_arr

def plot_orbits(phi_arr, theta_arr):
    img = plt.imread("Equirectangular_projection_SW.jpg")
    plt.imshow(img, extent=[0, math.pi*2, 0, math.pi])  
    plt.scatter(phi_arr, theta_arr, color='firebrick', s = 20)
    
    
    

    
def R_z(phi):
    return np.array([[np.cos(phi),-np.sin(phi),0],[np.sin(phi), np.cos(phi),0], [0,0,1]])

def R_y(theta):
    return np.array([[np.cos(theta),0, -np.sin(theta)],[0, 1,0],[np.sin(theta), 0, np.cos(theta)]])


def get_theta(alpha, R_e, H):
    # airplane to satellite distance from transmission angle, H as in altitude measured from earth 

    y = R_e * np.cos(np.pi / 2 + alpha) + np.sqrt(R_e**2 * np.cos(np.pi / 2 + alpha)**2 - (R_e**2 - (H+R_e)**2))
    z = np.sqrt(y**2 + H**2 - 2 * y * H * np.cos(np.pi / 2 - alpha))
    return 2*np.arcsin(z / (2*(H+R_e))) 


height = 10050*(10**(3)) #in m vom Erdmittelpunkt
alpha = np.pi/180*70 #in radiants (Winkel der Rotationsebene zur z-Achse)
#alpha = np.pi/180*0
granularity = 5000 #The number of points that should be plotted between t=0 and t= T_max
Theta0 = math.pi #initial Theta0 in radiants (Winkel des Punktes zur z-Achse); y-Achse auf Projektion von 0 bis 2*pi
Phi0 = math.pi/2 #initial Phi0 in radiants (Winkel des Punktes zur y-Achse); y-Achse auf Projektion von 0 bis pi

T = period(height)

T_max = int(2*T)
omega = 2*math.pi/T
#omega =  math.pi*2/(24*60*60)

plt.figure(figsize = (20,10))
phi_arr, theta_arr = get_orbits(height, alpha, omega, granularity, T_max)
plot_orbits(phi_arr, theta_arr)

plt.show()