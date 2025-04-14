import numpy as np

# Parameters
epsilon = 0.1 # sigma norm
h = 0.2 # rho h

a, b = 5, 5  # phi, 0<a<=b
c = np.abs(a-b) / np.sqrt(4*a*b) # phi

# Functions
def sigma_norm(z):
    return 1 / epsilon * (np.sqrt(1 + epsilon * np.linalg.norm(z)**2) - 1)

def rho_h(z):
    if 0 <= z < h:
        return 1
    elif h <= z <= 1:
        return 0.5 * (1 + np.cos(np.pi * (z-h) / (1-h)))
    else:
        return 0

def sigma_1(z):
    return z / np.sqrt(1 + z**2)

def phi(z):
    return 0.5 * ((a+b) * sigma_1(z+c) + (a-b))

r = 12 # com radius, interaction range
r_alpha = sigma_norm(r) # phi alpha
k = 1.2 # phi alpha, scaling factor
d = r / k # phi alpha
d_alpha = sigma_norm(d) # phi alpha

def phi_alpha(z):
    return rho_h(z/r_alpha) * phi(z-d_alpha)

def a_ij(q_j, q_i):
    return rho_h(sigma_norm(q_j-q_i) / r_alpha)

def n_ij(q_j, q_i):
    return (q_j-q_i) / np.sqrt(1 + epsilon * np.linalg.norm(q_j-q_i)**2)