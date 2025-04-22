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

r = 9 # com radius, interaction range
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

def q_ik(q_i, y_k, R_k):
    mu = R_k / np.linalg.norm(q_i-y_k)
    return mu * q_i + (1-mu) * y_k

def p_ik(q_i, p_i, y_k, R_k):
    a_k = (q_i-y_k) / np.linalg.norm(q_i-y_k)
    P = np.identity(2) - np.outer(a_k, a_k)
    mu = R_k / np.linalg.norm(q_i-y_k)
    return mu * P @ p_i

def n_ik(q_ik, q_i):
    return n_ij(q_ik, q_i)

h_obstacle = 0.9 # rho h obstacle

def rho_h_obstacle(z):
    if 0 <= z < h_obstacle:
        return 1
    elif h_obstacle <= z <= 1:
        return 0.5 * (1 + np.cos(np.pi * (z-h_obstacle) / (1-h_obstacle)))
    else:
        return 0
    
r_prime = 1.2*r
d_beta = sigma_norm(r_prime)

def b_ik(q_ik, q_i):
    return rho_h_obstacle(sigma_norm(q_ik-q_i) / d_beta)

def phi_beta(z):
    return rho_h_obstacle(z/d_beta) * (sigma_1(z-d_beta) - 1)