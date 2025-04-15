# MEAM 6240, UPenn
from threading import Thread
from queue import Empty
import numpy as np
import time
from matplotlib import pyplot as plt
from functions import phi_alpha, a_ij, n_ij, sigma_norm

class Node(Thread):
  def __init__(self, uid):
    """ Constructor """
    Thread.__init__(self)
    
    # basic information about network connectivity
    self.uid = uid    # node UID (an integer)
    self.out_nbr = [] # list of outgoing edges (see Edge class)
    self.in_nbr = []  # list of incoming edges (see Edge class)
    
    self.position = np.array([0, 0])   # position ([rx, ry])
    self.velocity = np.array([0, 0])   # position ([vx, vy])

    self.done = False # termination flag
    
    self.nominaldt = 0.03          # time step

    self.u = np.array([0, 0]) # control input

    self.c1_alpha = 3
    self.c2_alpha = 2 * np.sqrt(self.c1_alpha)
    self.c1_mt = 10
    self.c2_mt = 2 * np.sqrt(self.c1_mt)
    self.c1_mc = 10
    self.c2_mc = 2 * np.sqrt(self.c1_mt)

    # self.c1_alpha = 1
    # self.c2_alpha = 2 * np.sqrt(self.c1_alpha)
    # self.c1_mt = 5
    # self.c2_mt = 2 * np.sqrt(self.c1_mt)

    # self.c1_alpha = 1
    # self.c2_alpha = 1
    # self.c1_mt = 1
    # self.c2_mt = 1
    # self.c1_mc = 1
    # self.c2_mc = 1

    self.gamma_pos = np.array([20, 50])
    self.gamma_vel = np.array([0, 0])
    # self.gamma_u = np.array([0.5, 0.3])
    
    self.start_time = time.time()

  def __str__(self):
    """ Printing """
    return "Node %d has %d in_nbr and %d out_nbr" % (self.uid, len(self.in_nbr), len(self.out_nbr))

  ################################################
  #
  # Modify the graph
  #
  ################################################

  def addOutgoing(self, e):
    """ Add an edge for outgoing messages """
    self.out_nbr.append(e)
    
  def addIncoming(self, e):
    """ Add an edge for incoming messages """
    self.in_nbr.append(e)
    
  ################################################
  #
  # Set states externally
  #
  ################################################
  
  def getState(self):
    """ return the state of the node """
    return np.concatenate([self.position, self.velocity])

  def terminate(self):
    """ stop sim """
    self.done = True
 
  ################################################
  #
  # Run the vehicle
  #
  ################################################

  def run(self):
    """ Send messages, Retrieve message, Transition """
    while (not self.done):
      start = time.time()
      self.send()
      
      self.transition()
      
      self.dynamics()
      
      end = time.time()
      time.sleep(max(self.nominaldt - (end-start), 0))
    
  ################################################
  #
  # Implementation
  #
  ################################################
  def send(self):
    """ Send messages """
    for inbr in self.out_nbr:
      inbr.put(self.getState()) # send states (pos & vel) to all neigbors

  def transition(self):      
    """ Receive messages """

    f_alpha = 0

    count = 1
    total_pos = self.position
    total_vel = self.velocity

    for inbr in self.in_nbr:
      # retrieve most recent message (timeout = 1s)
      data = inbr.get()

      if (not (data is None)):

        pos = data[0:2]
        vel = data[2:4]

        f_alpha += self.c1_alpha * phi_alpha(sigma_norm(pos - self.position)) * n_ij(pos, self.position)
        f_alpha += self.c2_alpha * a_ij(pos, self.position) * (vel - self.velocity)

        total_pos = total_pos + pos
        total_vel = total_vel + vel
        count += 1

    f_gamma = -self.c1_mt * (self.position - self.gamma_pos) - self.c2_mt * (self.velocity - self.gamma_vel)

    avg_pos = total_pos / count
    avg_vel = total_vel / count

    print(count)

    f_gamma = f_gamma - self.c1_mc * (avg_pos - self.gamma_pos) - self.c2_mc * (avg_vel - self.gamma_vel)

    # print("uid", self.uid)
    # print("f alpha", f_alpha)
    # print("f gamma", f_gamma)

    self.u = f_alpha + f_gamma
  
  def dynamics(self):
    """ Move towards the centroid """
    self.velocity = self.velocity + self.u * self.nominaldt
    self.position = self.position + self.velocity * self.nominaldt

    # self.gamma_vel = self.gamma_vel + self.gamma_u * self.nominaldt
    # if self.gamma_pos[0] > 100:
    #   self.gamma_vel = np.array([-30, 10])
    # if self.gamma_pos[0] < 40:
    #   self.gamma_vel = np.array([30, 10])
    curr_time = time.time() - self.start_time
    self.gamma_vel = np.array([15, 50 * np.sin(2 * np.pi * curr_time / 15)])
    self.gamma_pos = self.gamma_pos + self.gamma_vel * self.nominaldt