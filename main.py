# MEAM 6240, UPenn
# Homework 2

from Node import *
from Edge import *
from Graph import *

import numpy as np
import time

def generateRandomGraph(N):
  G = Graph()

  for inode in range(N):
    # randomly generate node states
    n = Node(inode)
    n.setPosition(np.random.rand(2))
    G.addNode(n)
  
    # add all-to-all edges
    for iedge in range(inode):
      G.addEdge(iedge, inode, 0)
      G.addEdge(inode, iedge, 0)
  
  return G


### MAIN
if __name__ == '__main__':

  # generate a random graph with 30 nodes
  G = generateRandomGraph(30)
  
  print("========== Starting now ==========")
  print("Close the figure to stop the simulation")
  G.run()             # start threads in nodes
  G.setupAnimation()  # set up plotting
  print("Sending stop signal.....")
  G.stop()            # send stop signal
  print("========== Terminated ==========")