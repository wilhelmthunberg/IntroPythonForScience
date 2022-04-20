#Extra code for live animation of orbit

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time

years =3
axlim=(-47e11, 47e11 )
plt.style.use('dark_background')
fig = plt.figure()
ax = plt.axes(xlim =axlim, ylim =axlim )
ax.set_aspect('equal')
ax.axis('off')

def gforce(p1,ss):
    """
    Function to calculate forces on body p1 from other bodies in solarsystem ss.
    -------------
    Parameters: 
                p1: Class Body
                ss: Class Solarsystem
    Returns: 
                force_vec: force vector for the body in shape of array 

    """
    G = 6.67e-11 # Gravitational constant
    
    force_vec=0
    for p2 in ss.bodies: #all bodies in system extert some force on p1
        if p2 !=p1:
            r = p1.r-p2.r #distance-vector between bodies
            r_mag = np.linalg.norm(r) #magnitude of distance-vector
            r_hat = r/r_mag #unit vector for direction
            force_mag = G*p1.mass*p2.mass/r_mag**2 #total force
            force_vec += -force_mag*r_hat #forcevector
    
    return force_vec
    
def vel_at_aphelion(r):
    """Function to calc speed at aphelion. Can be used to set initial velocities.
    ----------
    Parameters: 
                r: length of semi-major axis, type=float,int,double
    Returns:
                v: speed, type=float
    
    """
    G = 6.67e-11
    mu = G*1.989e30
    v= np.sqrt(mu/r)
    return v

class Body(): 
    def __init__(self, name, radius , mass, r , v , color):
        self.name = name
        self.radius = radius
        self.mass = mass
        self.v = np.array(v,dtype=np.float32)
        self.r = np.array(r,dtype=np.float32)
        self.color=color
        self.xs = []#used to draw lines
        self.ys = []#used to draw lines
        self.plot = ax.scatter (r[0], r[1], color = color, s = np.pi*radius**2)
        self.line, = ax.plot([], [], color=color, linewidth=0.3)

class SolarSystem():
    def __init__(self,bodies=None):

        self.bodies = []
        self.time = 0
    def add_body(self,p):
        """
        Function to add planetary or stelllar bodies to solar systems
        ----
        Parameter: 
                    p: Class Body to be added. 
        """
        self.bodies.append(p)
     
    def orbit(self):
        """
        Function to make orbital step in SolarSystem. 
        Uses gforce() function to calculate accelerationg and can thus
        edit r and v of the Body.
        """
        dt = 3*24*3600
        self.time+=3
        plots=[]#to be returned and used for animation
        lines=[]#to be returned and used for animation
        for b in self.bodies:
            b.force = gforce(b,self)
    # Update momenta.
            b.v = b.v + b.force*dt/b.mass
    # Update positions.
            b.r = b.r + b.v*dt
            #t = t + dt
            b.plot.set_offsets(b.r[:2])#update plot
            plots.append(b.plot)#
            b.xs.append(b.r[0])#line coordinates
            b.ys.append(b.r[1])
            b.line.set_xdata(b.xs)
            b.line.set_ydata(b.ys)
            lines.append(b.line)
        

        if self.time % 365 ==0:
            print(str(self.time))
           
        return plots+lines


ss = SolarSystem()


ss.add_body(Body( 'Sun', radius=7, color='yellow',
               mass = 1.989e30, v=[0,0,0], r= [0,0,0]))
ss.add_body(Body('Mercury', radius=0.4, color='gray',
               mass = 0.330e24, v=[0,vel_at_aphelion(69.8e9),0], r= [69.8e9,0,0]))

ss.add_body(Body( 'Venus', radius=1, color='orange',
               mass =4.87e24, v=[0,vel_at_aphelion(1.089e11),0], r= [1.089e11,0,0]))

ss.add_body(Body( 'Earth', radius=1, color='blue',
               mass = 5.972e24, v=[0,vel_at_aphelion(1.521e11),0], r= [1.521e11,0,0]))
ss.add_body(Body( 'Mars', radius=1, color='red',
               mass =0.642e24, v=[0,vel_at_aphelion(2.492e11),0], r= [2.492e11,0,0]))

ss.add_body(Body( 'Jupiter', radius=3, color='darkorange',
               mass =1898e24, v=[0,vel_at_aphelion(8.166e11),0], r= [8.166e11,0,0]))
ss.add_body(Body( 'Saturn', radius=1, color='navajowhite',
               mass =568e24, v=[0,vel_at_aphelion(15.145e11),0], r= [15.145e11,0,0]))
ss.add_body(Body( 'Uranus', radius=1, color='mediumturquoise',
               mass =86.8e24, v=[0,vel_at_aphelion(30.036e11),0], r= [30.036e11,0,0]))
ss.add_body(Body( 'Neptune', radius=1, color='cornflowerblue',
               mass =102e24, v=[0,vel_at_aphelion(45.457e11),0], r= [45.457e11,0,0]))

rand = random.uniform(69.8e9, 45.457e11)
ss.add_body(Body( 'NewStar', radius=7, color='darkred',
              mass = 1.989e30, v=[-2*rand/(24*3600*365*years),0,0], r= [0.71*rand,0.3*rand,0]))




def animate(i):#artist for animation
    return ss.orbit()
ani = animation.FuncAnimation(fig, animate, repeat=False, frames=int(365*years/3), blit=False, interval=20) #animate orbit
#ani.save('Normal_orbit.gif', writer='imagemagick', fps=1)
plt.show()






    
