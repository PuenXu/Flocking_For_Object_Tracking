# MEAM 6240, UPenn
from threading import Thread
from queue import Empty
import numpy as np
import time
from matplotlib import pyplot as plt


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
    
    self.nominaldt = 0.05           # time step

    self.u = np.array([0, 0]) # control input
    
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

    for inbr in self.in_nbr:
      # retrieve most recent message (timeout = 1s)
      data = inbr.get()

      if (not (data is None)):
        print("Node %d received data from %d " % (self.uid, inbr.in_nbr.uid))
        pos = data[0:2]
        vel = data[2:4]
  
  def dynamics(self):
    """ Move towards the centroid """
    self.velocity = self.velocity + self.u * self.nominaldt
    self.position = self.position + self.velocity * self.nominaldt