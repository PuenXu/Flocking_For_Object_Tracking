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
    
    self.position = [0,0]   # position ([rx, ry])
    self.done = False # termination flag
    
    self.nominaldt = 0.05           # time step
    
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

  def setPosition(self, s):
    """ update the position of the node """
    self.position = s
    
  def getPosition(self):
    """ return the position of the node """
    return self.position

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
  # YOUR CODE GOES HERE
  #
  ################################################
  def send(self):
    """ Send messages """
    # REPLACE WITH YOUR CODE
    for inbr in self.out_nbr:
      inbr.put(0) # send 0 to all neigbors

  def transition(self):      
    """ Receive messages, update Voronoi Cell """
    # REPLACE WITH YOUR CODE

    for inbr in self.in_nbr:
      # retrieve most recent message (timeout = 1s)
      data = inbr.get()
      if (not (data is None)):
        print("Node %d received data from %d " % (self.uid, inbr.in_nbr.uid))
  
  def dynamics(self):
    """ Move towards the centroid """
    # self.position = self.position - self.nominaldt # move to bottom left
    self.position = self.position + 0.1*([0.5, 0.5] - self.position) # gather in the middle