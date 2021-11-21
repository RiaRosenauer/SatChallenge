#calculating the orbit of a sattelite projected onto earth
import math
import matplotlib.pyplot as plt
import numpy as np
import itertools

import matplotlib.animation as animation


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
    return np.array([np.cos(w * t), np.sin(w * t), 0])

#ensuring the right modulo of phi-omega*t
def convert_angle(angle):
    while angle <= 0:
        angle = angle + 2*math.pi
    return angle


#calculate r, theta, phi depening on time
#wähle tp (t-prime) so, dass 
#tp = T*k/n, n ist anzahl der Sateliten auf einen Ring, k ist der kte-Satelit in dem Ring
def timeEvolution(t,tp, alpha, w, phi0):
    #R_x(alpha).dot(r_vec(t))
    #phi0 is the initial azimuthal offset 
    r, theta, phi = cart_tosphere( *(R_z(phi0).dot(R_x(alpha).dot(r_vec(t+tp, w)))))
    phi2 =  convert_angle(phi - Omega * t)
    return theta, phi2


#returns arrays of theta and phi
def get_current_orbit(t0, height, alpha, omega, granularity, T, tp, phi0):
    phi_arr = []
    theta_arr = []

    for t in np.linspace(max(0, t0-T), t0, granularity):
        theta, phi = timeEvolution(t,tp, alpha, omega, phi0)
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

    
def createConeSection(r, theta, phi, number_of_circles, number_of_points_on_circle):
    R_e = 6.38 * 10**(6)
    theta_min = get_theta(75*np.pi/180, R_e, r-R_e)
    theta_max = get_theta(10*np.pi/180, R_e, r-R_e)

    theta_array2 = np.linspace(theta_min, theta_max,number_of_circles)
    phi_array2 = np.linspace(0, 2*np.pi, number_of_points_on_circle)[:-1] #here vary number of points to make area denser 

    gridSpherical =np.array([ [(i,j) for j in phi_array2] for i in theta_array2]) #np.array([ [(i,j) for i in theta_array2] for j in phi_array2])


    gridCartesian = [np.array(sphere_tocart(r, *i)) for i in list(itertools.chain(*gridSpherical)) ]

    gridEarthFrame = [ R_z(phi).dot(R_y(-theta).dot(vector)) for vector in gridCartesian ]
    
    
    gridEarthFrameSpherical = [ cart_tosphere(*v)[1:] for v in gridEarthFrame]
    #gridEarthFrameSpherical = [ v for v in gridEarthFrame]

    return gridEarthFrameSpherical

def plotConeSections(r, theta, phi):
    A = createConeSection(r,theta, phi)
    theta_section = [a[0] for a in A]
    phi_section = [convert_angle(a[1]) for a in A]
    plt.scatter(phi_section, theta_section, color='blue', s =20)


#returns arrays of theta and phi
def get_current_orbit(t0, height, alpha, omega, granularity, T, tp, phi0):
    phi_arr = []
    theta_arr = []

    for t in np.linspace(max(0, t0-T), t0, granularity):
        theta, phi = timeEvolution(t,tp, alpha, omega, phi0)
        phi_arr.append(phi)
        theta_arr.append(theta)

    return phi_arr, theta_arr


#calculate r, theta, phi depening on time
#wähle tp (t-prime) so, dass 
#tp = T*k/n, n ist anzahl der Sateliten auf einen Ring, k ist der kte-Satelit in dem Ring
def timeEvolution(t,tp, alpha, w, phi0):
    #R_x(alpha).dot(r_vec(t))
    #phi0 is the initial azimuthal offset 
    r, theta, phi = cart_tosphere( *(R_z(phi0).dot(R_x(alpha).dot(r_vec(t+tp, w)))))
    phi2 =  convert_angle(phi - Omega * t)
    return theta, phi2


#for the execution relevant lists

#the length if the video = numberoftimesteps/fps

#initial phi0, height, alpha, number of sattelites per bahn, color
sats = [[math.pi*2/6, 42050*(10**(3)), 47*math.pi/180, 8, 'blue'],[0,42050*(10**(3)), 47*math.pi/180, 8, 'red']]

fig = plt.figure(figsize = (20,10))
ax1 = plt.axes()
granularity = 5000

number_of_circles = 32
number_of_points_on_circle = 64

#representing the discrete timesteps, that are plotted and put together as an animation
T = period(max([i[1] for i in sats]))
ts = np.linspace(0, 2*T, 200)


modus_Fill = '''
def plotConeSections2(r, theta, phi, colors):
    A = createConeSection(r,theta, phi, 2, 64)
    theta_section = [a[0] for a in A]
    phi_section = [convert_angle(a[1]) for a in A]
    half = int(round(len(phi_section)/2))
    #ax1.plot(phi_section, theta_section,  marker = '.', markersize = 10, color=colors)
    ax1.plot(phi_section[:half]+[phi_section[0]], theta_section[:half] + [theta_section[0]],  marker = '.', markersize = 0.5, color=colors, alpha=0.2)
    ax1.plot(phi_section[half:]+[phi_section[half]], theta_section[half:]+[theta_section[half]],  marker = '.', markersize = 0.5, color=colors, alpha=0.8)
    ax1.fill(phi_section[:half]+[phi_section[0]], theta_section[:half] + [theta_section[0]], color='white', alpha=0.2)
    ax1.fill(phi_section[half:]+[phi_section[half]], theta_section[half:]+[theta_section[half]], color=colors, alpha=0.1)
    
    #plot.set_data()'''

#modus_points = '''
def plotConeSections2(r, theta, phi, colors):
    A = createConeSection(r,theta, phi, number_of_circles, number_of_points_on_circle)
    theta_section = [a[0] for a in A]
    phi_section = [convert_angle(a[1]) for a in A]
    plt.scatter(phi_section, theta_section, color=colors,alpha=0.5, s =20)
#'''

    
def plot_orbits2(phi_arr, theta_arr, colors):
    ax1.scatter(phi_arr, theta_arr, color=colors, s = 20) 


modus_1 = '''
def animate(t):
    ax1.clear()
    for sat in sats: 
        img = plt.imread("Equirectangular_projection_SW.jpg")
        ax1.imshow(img, extent=[0, math.pi*2, 0, math.pi])
        for k in range(1,sat[3]+1):
            height = sat[1]
            T = period(height)
            phi_arr, theta_arr = get_current_orbit(t, height, sat[2], omega, granularity, T, T*k/sat[3], sat[0])
            plot_orbits2(phi_arr, theta_arr, sat[4])
            ax1.scatter(phi_arr[-1],theta_arr[-1],color='red')
            plotConeSections2(height, theta_arr[-1], phi_arr[-1], sat[4])
    return ax1'''

#modus_2='''
def animate(t):
    ax1.clear()
    for num, sat in enumerate(sats): 
        img = plt.imread("Equirectangular_projection_SW.jpg")
        ax1.imshow(img, extent=[0, math.pi*2, 0, math.pi])
        height = sat[1]
        T = period(height)
        for k in range(1,4):
            phi_arr, theta_arr = get_current_orbit(t, height, sat[2], 2*math.pi/T, granularity, T, T*k/sat[3], sat[0])
            plot_orbits2(phi_arr, theta_arr, sat[4])
            ax1.scatter(phi_arr[-1],theta_arr[-1],color='red')
            plotConeSections2(height, theta_arr[-1], phi_arr[-1], sat[4])
    return ax1
#'''


Writer = animation.writers['ffmpeg']
writer = Writer(fps=19, metadata=dict(artist='Me'), bitrate=-1)
ani = animation.FuncAnimation(fig, animate, frames=ts, interval=10)
print('proceeding to save')
#length of video in seconds: number of frames/fps
ani.save('YourAnimation.mp4', writer=writer)
              
print('saved')






