import numpy as np
import matplotlib.pyplot as plt

# Load data from both CSVs
free_data = np.loadtxt('good_free.csv', delimiter=',', skiprows=1)[:90]
obs_data = np.loadtxt('good_obstacle.csv', delimiter=',', skiprows=1)[:90]

def extract_columns(data):
    return {
        'com_x': data[:, 0],
        'com_y': data[:, 1],
        'target_x': data[:, 2],
        'target_y': data[:, 3],
        'connectivity': data[:, 4],
        'cohesion': data[:, 5],
        'vel_mismatch': data[:, 6],
        'en_deviation': data[:, 7],
    }

free = extract_columns(free_data)
obs = extract_columns(obs_data)

n = len(free['com_x'])
dt = 0.1
time = np.arange(n) * dt

# === Plot: Deviation Energy ===
plt.figure()
plt.plot(time, free['en_deviation'], label='Free Space')
plt.plot(time, obs['en_deviation'], label='Obstacle')
plt.xlabel('Time (s)')
plt.ylabel('Deviation Energy')
plt.legend()
plt.grid(True)
plt.title('Deviation Energy vs Time')
plt.show()

# === Plot: Velocity Mismatch ===
plt.figure()
plt.plot(time, free['vel_mismatch'], label='Free Space')
plt.plot(time, obs['vel_mismatch'], label='Obstacle')
plt.xlabel('Time (s)')
plt.ylabel('Velocity Mismatch')
plt.legend()
plt.grid(True)
plt.title('Velocity Mismatch vs Time')
plt.show()

# === Plot: Mean Squared Error ===
mse_free = np.sqrt((free['com_x'] - free['target_x'])**2 + (free['com_y'] - free['target_y'])**2)
mse_obs  = np.sqrt((obs['com_x'] - obs['target_x'])**2 + (obs['com_y'] - obs['target_y'])**2)

plt.figure()
plt.plot(time, mse_free, label='Free Space')
plt.plot(time, mse_obs, label='Obstacle')
plt.xlabel('Time (s)')
plt.ylabel('Mean Squared Error')
plt.legend()
plt.grid(True)
plt.title('Mean Squared Error vs Time')
plt.show()

# === Plot: Connectivity ===
plt.figure()
plt.plot(time, free['connectivity'], label='Free Space')
plt.plot(time, obs['connectivity'], label='Obstacle')
plt.xlabel('Time (s)')
plt.ylabel('Connectivity')
plt.legend()
plt.grid(True)
plt.title('Connectivity vs Time')
plt.show()

# === Plot: Cohesion ===
plt.figure()
plt.plot(time, free['cohesion'], label='Free Space')
plt.plot(time, obs['cohesion'], label='Obstacle')
plt.xlabel('Time (s)')
plt.ylabel('Cohesion')
plt.legend()
plt.grid(True)
plt.title('Cohesion vs Time')
plt.show()

# === Trajectory Plot: Separate Figures ===
def plot_trajectory(data, label):
    x, y = 100, 50  # Center of circle
    r = 10
    theta = np.linspace(0, 2*np.pi, 100)
    circle_x = x + r * np.cos(theta)
    circle_y = y + r * np.sin(theta)

    plt.figure()
    plt.axes(xlim=(0, 150.0), ylim=(0, 150.0)).set_aspect('equal', 'box')
    plt.plot(circle_x, circle_y, '--', label='Goal Circle')
    plt.plot(data['com_x'], data['com_y'], 'o-', label='Center of Mass')
    plt.plot(data['target_x'], data['target_y'], '.-', label='Target')
    plt.xlabel('x position (m)')
    plt.ylabel('y position (m)')
    plt.title(f'CoM & Target Trajectory: {label}')
    plt.legend()
    plt.grid(True)
    plt.show()

plot_trajectory(free, 'Free Space')
plot_trajectory(obs, 'Obstacle')