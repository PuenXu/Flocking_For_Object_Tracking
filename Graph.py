# MEAM 6240, UPenn
from Node import *
from Edge import *

from matplotlib import pyplot as plt
from matplotlib import animation

class Graph:
  def __init__(self, filename = None):
    """ Constructor """
    self.Nv = 0
    self.V = []
    self.E = []
    self.root = None
    
    # for plotting
    self.animatedt = 100 # milliseconds
    self.fig = plt.figure()
    self.ax = plt.axes(xlim=(0, 100.0), ylim=(0, 100.0))
    self.ax.set_aspect('equal', 'box')
    self.pts, = self.ax.plot([], [], 'b.')
    self.anim = None
    
    # for reading in graphs if they come from a file
    if not(filename is None):
      # read the graph from a file
      with open(filename) as f:
        # nodes
        line = f.readline()
        self.Nv = int(line);
        for inode in range(self.Nv):
          self.addNode(Node(inode))

        # edges      
        line = f.readline()
        while line:
          data = line.split()
        
          in_nbr = int(data[0])
          out_nbr = int(data[1])
          cost = float(data[2])
        
          self.addEdge(in_nbr, out_nbr, cost)
        
          line = f.readline()
      
      f.close()
    
  def __str__(self):
    """ Printing """
    return "Graph: %d nodes, %d edges" % (self.Nv, len(self.E))
    
  ################################################
  #
  # Modify the graph
  #
  ################################################

  def addNode(self, n):
    """ Add a node to the graph """
    self.V.append(n)
    self.Nv += 1
    
  def addEdge(self, i, o, c):
    """ Add an edge between two nodes """
    e = Edge(self.V[i], self.V[o], c)
    self.V[i].addOutgoing(e)
    self.V[o].addIncoming(e)
    self.E.append(e)
    
  ################################################
  #
  # Start and Stop computations
  #
  ################################################

  def run(self):
    """ Run the alg on all of the nodes """
    # Start running the threads
    for i in range(self.Nv):
      self.V[i].start()

  def stop(self):
    """ Send a stop signal """
    # Send a stop signal
    for i in range(self.Nv):
      self.V[i].terminate()
    # Wait until all the nodes are done
    for i in range(self.Nv):
      self.V[i].join()
      
  ################################################
  #
  # Animation helpers
  #
  ################################################

  def gatherNodeLocations(self):
    """ Collect state information from all the nodes """
    x = []; y = [];
    for i in range(self.Nv):
      x.append(self.V[i].position[0])
      y.append(self.V[i].position[1])
    return x,y
    
  def setupAnimation(self):
    """ Initialize the animation """
    self.anim = animation.FuncAnimation(self.fig, self.animate, interval=self.animatedt, blit=False)
    
    plt.show()
    
  def animate(self, i):
    """ Animation helper function """
    x,y = self.gatherNodeLocations()
    self.pts.set_data(x, y)
    
    return self.pts, 