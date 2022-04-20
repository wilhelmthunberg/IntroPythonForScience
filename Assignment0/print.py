#sphere, u235, capture, fission elastic scattering, Cm-isotropic, nubar neutrons, sample watt sidt from dl 4
#no time track, inital launch from center, save and use fission sites as new source


import random

def XS(E,xs_arr):
    """Function to sample cross section based on Energy
    
    Parameters
    ----------
    E : array
        Energies of incident neutrons
    xs_arr : np.array
        Array containing energies with respective cross section
    
    Returns
    -------
    x : float or array-like
        Random distance between collisions
    """
    xs = []
    for i in range(len(E)):
        if E[i] > max(xs_arr[0]) or E[i] <min(xs_arr[0]):
            raise ValueError('The chosen energy is outside the bounds of given array')
        diff= abs(xs_arr[0] - E[i])
        closest_val = min(diff)
        xs.append(xs_arr[1][np.where(diff==closest_val)])
        
    return np.array(xs)

def nu(E, nu_b, E_nu_bar):
    if E > max(E_nu_bar) or E <min(E_nu_bar):
        raise ValueError('The chosen energy is outside the bounds of given array')
    E = np.float64(E)
    diff= abs(E_nu_bar[0] - E)
    closest_val = min(diff)
    return nu_b[np.where(diff==closest_val)]
    


def distanceToCollision(xs_c, xs_f, xs_e,N=1):
    """Function to sample the distance to collision inside U235.
    
    Parameters
    ----------
    xs_c,xs_f, xs_e: list,array. All must be same length.
        microscopic cross sections
    N : int
        Number of events to be sampled per neutron (default=1)
    
    Returns
    -------
    x : float or array-like
        Random distance between collisions in m based on cross sections(which are based on energy) of specific neutron
    """
    x=[]
    M=235
    N_av=6.022e23
    rho = 19.1e3
    n= (N_av * rho)/M
    for i in range(len(xs_f)):
        SigT = 1e-28*(xs_c[i]+xs_f[i]+xs_e[i])*n #convert to m2
        r = np.random.uniform(0,1,N)
        dist = -np.log(r)/SigT# Complete the line
        x.append(np.random.choice(dist))
    return np.array(x) 

def elasticScatter(E, A):
    """
    Funcition to find direction and final energy of elastically scattred neutron.
    
    Parameters: 
    --------------
    E: float
        incident energy
    
    Returns:
    E: float
        Final energy
        
    muL: float
        cosine of scattering angle in lab frame
    """
    alpha = ((A-1)/(A+1))**2
    muC=np.random.uniform(-1,1)
    thetaC=np.arccos(muC)
    E=(((1+alpha)+(1-alpha)*muC)/2)*E
    thetaL=np.arctan2(np.sin(thetaC),((1/A)+muC))
    muL=np.cos(thetaL)
    return E, muL

def randomDir():
    mu=np.random.uniform(-1,1)
    theta=np.arccos(mu)
    phi=np.random.uniform(0,2*np.pi)

    u=np.sin(theta)*np.cos(phi)
    v=np.sin(theta)*np.sin(phi)
    w=np.cos(theta)
    return np.array([u,v,w])

def watt(x): 
    C1 = 0.453
    C2 = 0.965
    C3 = 2.29
    return C1*np.exp(-x/C2)*np.sinh(np.sqrt(C3*x))#complete the line


def run(R,NGEN,NPG,NSKIP):
    """Function to perform a criticality calculation in a U-235 sphere.
    
    Parameters
    ----------
    R : float
        Radius of the sphere
    NGEN : int
        Number of neutron generations
    NPG : int
        Number of neutrons per generation
    NSKIP : int
        Number of inactive generations which will not be taken into account for estimating the k-eigenvalue
    
    Returns
    -------
    keff : float
        The estimated mean k-eigenvalue of the system
    kstd : float
        The standard deviation of the estimated k-eigenvalue
    """
    keff = []

    E =np.ones(NPG)*1e6
    neutrons=NPG
    
    
    xs_c = XS(E,xs_cap)
    xs_f= XS(E,xs_fiss)
    xs_e= XS(E,xs_el)
    
    r = distanceToCollision(xs_c, xs_f, xs_e,1000)#distance to collision for all neutrons

    mu=np.random.uniform(-1,1,neutrons)        ### CORRECT
    theta=np.arccos(mu)
    phi=np.random.uniform(0,2*np.pi,neutrons)
    x=r*np.sin(theta)*np.cos(phi)
    y=r*np.sin(theta)*np.sin(phi)
    z=r*np.cos(theta)
    
    ###---####
    new_x = []
    new_y = []
    new_z = []
    new_E = []
    new_mu=[]
    
    for _ in range(NGEN):
        old_neutrons = neutrons
        for i in range(len(x)):

            if np.sqrt(x[i]**2+y[i]**2+z[i]**2)>R:
                #escaped
                neutrons -=1
            else:
                rand=np.random.uniform(0,xs_c[i]+xs_e[i]+xs_f[i])
                if rand < xs_c[i]:
                    #capture
                    neutrons-=1
                elif xs_c[i]<rand<xs_c[i]+xs_e[i]:
                    #elastic
                    E,muL=elasticScatter(E[i], 235)
                    new_E.append(E)
                    new_mu.append(muL)
                    new_x.append(x[i])
                    new_y.append(y[i])
                    new_z.append(z[i])
                    
                else:
                    #fission#####################################CONTINUE HERE
                    for _ in range(round(nu(E,nu_bar_val))):
                        new_x.append(x[i])
                        new_y.append(y[i])
                        new_z.append(z[i])
                        E_fiss = np.linspace(0,20,1000) #in MeV
                        maxW=np.max(watt(E))
                        xi=np.random.uniform(0,20)
                        yi=np.random.uniform(0,maxW)
                        while watt(xi)<yi:
                            xi=np.random.uniform(0,20)
                            yi=np.random.uniform(0,maxW)
                        new_E.append(xi*1e6)#in eV
        if neutrons <1:
            break
        else:
            keff.append(neutrons/old_neutrons)
            print('length',len(x))
            print('new_x',new_x)
            E=new_E
            xs_c = XS(E,xs_cap)
            xs_f= XS(E,xs_fiss)
            xs_e= XS(E,xs_el)
            r = distanceToCollision(xs_c, xs_f, xs_e,neutrons)
           ### CORRECT
            theta=np.arccos(new_mu)
            phi=np.random.uniform(0,2*np.pi,neutrons)
            x=new_x+r*np.sin(theta)*np.cos(phi)
            y=new_y+r*np.sin(theta)*np.sin(phi)
            z=new_z+r*np.cos(theta)

            pp.pprint(y)


    return np.mean(keff), np.std(keff)