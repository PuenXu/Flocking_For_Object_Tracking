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
    self.ax = plt.axes(xlim=(0, 200.0), ylim=(0, 100.0))
    self.ax.set_aspect('equal', 'box')
    self.pts, = self.ax.plot([], [], 'b.')
    self.gamma, = self.ax.plot([], [], 'r*')
    self.beta, = self.ax.plot([], [], 'go')
    self.anim = None

    # obstacle
    x, y = 100, 50     # Center of the circle
    r = 10         # Radius

    # Generate points on the circle
    theta = np.linspace(0, 2*np.pi, 100)
    circle_x = x + r * np.cos(theta)
    circle_y = y + r * np.sin(theta)

    self.ax.plot(circle_x, circle_y, 'k--', label='Obstacle')

    # for analysis
    self.com_x_traj = []
    self.com_y_traj = []
    self.target_x_traj = []
    self.target_y_traj = []
    self.connectivity_traj = []
    self.cohesion_traj = []
    self.vel_mismatch_traj = []
    self.en_deviation_traj = []
    
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
      
    # for analysis
    # data = np.column_stack((self.com_x_traj, self.com_y_traj, self.target_x_traj, self.target_y_traj, self.connectivity_traj, self.cohesion_traj, self.vel_mismatch_traj, self.en_deviation_traj))
    # np.savetxt('data.csv', data, delimiter=',', header='com_x, com_y, target_x, target_y, connectivity, cohesion, vel_mismatch, en_deviation', comments='')

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
  
  def gatherNodeVelocity(self):
    """ Collect state information from all the nodes """
    vx = []; vy = [];
    for i in range(self.Nv):
      vx.append(self.V[i].velocity[0])
      vy.append(self.V[i].velocity[1])
    return vx, vy
  
  def gatherBetaLocations(self):
    """ Collect state information from all the nodes """
    x = []; y = [];
    for i in range(self.Nv):
      x.append(self.V[i].q_ik_var[0])
      y.append(self.V[i].q_ik_var[1])
    return x,y
    
  def setupAnimation(self):
    """ Initialize the animation """
    self.anim = animation.FuncAnimation(self.fig, self.animate, interval=self.animatedt, blit=False)
    
    plt.show()

  def animate(self, i):
    """ Animation helper function """
    # Gather positions
    x, y = self.gatherNodeLocations()
    self.pts.set_data(x, y)

    beta_x, beta_y = self.gatherBetaLocations()
    self.beta.set_data(beta_x, beta_y)

    # Gamma (target) location
    gamma_pos = self.V[0].gamma_pos
    self.gamma.set_data([gamma_pos[0]], [gamma_pos[1]])

    # q = np.column_stack((x, y))
    # n = q.shape[0]

    # A = np.zeros((n, n))
    # q_avg = np.mean(q, axis=0)
    # diff_q = q - q_avg
    # distances = np.linalg.norm(diff_q, axis=1)
    # max_distance = np.max(distances)

    # r = 9
    # d = 9 / 1.2
    # total = 0
    # edge_count = 0

    # for i in range(n):
    #     for j in range(i + 1, n):  # Exploit symmetry
    #         a = a_ij(q[i], q[j])
    #         A[i, j] = A[j, i] = a
            
    #         dist = np.linalg.norm(q[i] - q[j])
    #         if dist < r:
    #             total += (dist - d) ** 2
    #             edge_count += 1

    # # Normalize by number of edges + 1
    # E_q = total / (edge_count + 1)
    # E_q_normalized = E_q / d**2
    # self.en_deviation_traj.append(E_q_normalized)

    # # Connectivity (normalized matrix rank)
    # connectivity = np.linalg.matrix_rank(A) / n
    # self.connectivity_traj.append(connectivity)

    # # Cohesion (max distance to center)
    # self.cohesion_traj.append(max_distance)

    # # Gather velocity and compute mismatch
    # vx, vy = self.gatherNodeVelocity()
    # v = np.column_stack((vx, vy))
    # v_avg = np.mean(v, axis=0)
    # diff_v = v - v_avg
    # K_v_normalized = np.sum(np.linalg.norm(diff_v, axis=1)**2) / n
    # self.vel_mismatch_traj.append(K_v_normalized)

    # # Center of mass trajectory
    # com_x = np.mean(x)
    # com_y = np.mean(y)
    # self.com_x_traj.append(com_x)
    # self.com_y_traj.append(com_y)

    # # Target trajectory
    # self.target_x_traj.append(gamma_pos[0])
    # self.target_y_traj.append(gamma_pos[1])

    return self.pts, self.gamma, self.beta