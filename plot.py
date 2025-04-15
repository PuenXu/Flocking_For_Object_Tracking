import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file (skip the header row)
data = np.loadtxt('data.csv', delimiter=',', skiprows=1)

# Extract columns
com_x = data[:, 0]
com_y = data[:, 1]
target_x = data[:, 2]
target_y = data[:, 3]

n = len(com_x)

dt = 0.1
time = [0.1 * i for i in range(n)]

mse = np.sqrt(np.subtract(com_x, target_x)**2 + np.subtract(com_y, target_y)**2)

# Plot
plt.figure()
plt.plot(com_x, com_y, marker='o', label='Center of Mass')
plt.plot(target_x, target_y, marker='.', label='Target')
plt.xlabel('x position (m)')
plt.ylabel('y position (m)')
plt.title('CoM & Target Position Trajectory')
plt.legend()
plt.grid(True)
plt.show()

plt.figure()
plt.plot(time, mse)
plt.xlabel('time (s)')
plt.ylabel('mean squared error')
plt.title('Mean Square Error vs Time')
plt.legend()
plt.show()