import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file (skip the header row)
data = np.loadtxt('data.csv', delimiter=',', skiprows=1)

# Extract columns
com_x = data[:, 0]
com_y = data[:, 1]
target_x = data[:, 2]
target_y = data[:, 3]
connectivity = data[:, 4]
cohesion = data[:, 5]
vel_mismatch = data[:, 6]
en_deviation = data[:, 7]

n = len(com_x)

dt = 0.1
time = [0.1 * i for i in range(n)]

mse = np.sqrt(np.subtract(com_x, target_x)**2 + np.subtract(com_y, target_y)**2)

# x, y = 70, 50     # Center of the circle
# r = 10         # Radius

# # Generate points on the circle
# theta = np.linspace(0, 2*np.pi, 100)
# circle_x = x + r * np.cos(theta)
# circle_y = y + r * np.sin(theta)

plt.figure()
plt.plot(time, en_deviation)
plt.xlabel('time (s)')
plt.ylabel('energy_deviation')
# plt.title('Mean Square Error vs Time')
plt.show()

plt.figure()
plt.plot(time, vel_mismatch)
plt.xlabel('time (s)')
plt.ylabel('velocity_mismatch')
# plt.title('Mean Square Error vs Time')
plt.show()

# Plot
plt.figure()
plt.axes(xlim=(0, 150.0), ylim=(0, 150.0)).set_aspect('equal', 'box')
# plt.plot(circle_x, circle_y, label='Circle')
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
plt.show()

plt.figure()
plt.plot(time, connectivity)
plt.xlabel('time (s)')
plt.ylabel('connectivity')
# plt.title('Mean Square Error vs Time')
plt.show()

plt.figure()
plt.plot(time, cohesion)
plt.xlabel('time (s)')
plt.ylabel('cohesion')
# plt.title('Mean Square Error vs Time')
plt.show()