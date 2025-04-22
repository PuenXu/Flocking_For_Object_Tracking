import numpy as np
import matplotlib.pyplot as plt

free_data = np.loadtxt('flock_free.csv', delimiter=',', skiprows=1)[:135]
obs_data = np.loadtxt('flock_main.csv', delimiter=',', skiprows=1)[:135]

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

mse_free = np.sqrt((free['com_x'] - free['target_x'])**2 + (free['com_y'] - free['target_y'])**2)
mse_obs  = np.sqrt((obs['com_x'] - obs['target_x'])**2 + (obs['com_y'] - obs['target_y'])**2)

fig1, axs1 = plt.subplots(2, 2, figsize=(12, 8))
# fig1.suptitle('Flocking Verification', fontsize=14)

axs1[0, 0].plot(time, free['en_deviation'], label='Free Space')
axs1[0, 0].plot(time, obs['en_deviation'], label='Obstacle')
axs1[0, 0].set_title('Deviation Energy')
axs1[0, 0].set_xlabel('Time (s)')
axs1[0, 0].set_ylabel('Energy')
axs1[0, 0].grid(True)
axs1[0, 0].legend()

axs1[0, 1].plot(time, free['vel_mismatch'], label='Free Space')
axs1[0, 1].plot(time, obs['vel_mismatch'], label='Obstacle')
axs1[0, 1].set_title('Velocity Mismatch')
axs1[0, 1].set_xlabel('Time (s)')
axs1[0, 1].set_ylabel('Mismatch')
axs1[0, 1].grid(True)
axs1[0, 1].legend()

axs1[1, 0].plot(time, free['cohesion'], label='Free Space')
axs1[1, 0].plot(time, obs['cohesion'], label='Obstacle')
axs1[1, 0].set_title('Cohesion Radius')
axs1[1, 0].set_xlabel('Time (s)')
axs1[1, 0].set_ylabel('Cohesion Radius (m)')
axs1[1, 0].grid(True)
axs1[1, 0].legend()

axs1[1, 1].plot(time, free['connectivity'], label='Free Space')
axs1[1, 1].plot(time, obs['connectivity'], label='Obstacle')
axs1[1, 1].set_title('Connectivity')
axs1[1, 1].set_xlabel('Time (s)')
axs1[1, 1].set_ylabel('Connectivity')
axs1[1, 1].grid(True)
axs1[1, 1].legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()


fig2, axs2 = plt.subplots(1, 3, figsize=(18, 5))
# fig2.suptitle('Tracking Performance', fontsize=14)

def plot_trajectory(ax, data, title):
    if title == 'Trajectory with Obstacle':
        x, y, r = 100, 50, 10
        theta = np.linspace(0, 2 * np.pi, 100)
        circle_x = x + r * np.cos(theta)
        circle_y = y + r * np.sin(theta)
        ax.plot(circle_x, circle_y, '--', label='Goal Circle')
    ax.plot(data['com_x'], data['com_y'], 'o-', label='Center of Mass')
    ax.plot(data['target_x'], data['target_y'], '.-', label='Target')
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 150)
    ax.set_aspect('equal')
    ax.set_title(title)
    ax.set_xlabel('x position (m)')
    ax.set_ylabel('y position (m)')
    ax.grid(True)
    ax.legend()

plot_trajectory(axs2[0], free, 'Trajectory in Free Space')
plot_trajectory(axs2[1], obs, 'Trajectory with Obstacle')

axs2[2].plot(time, mse_free, label='Free Space')
axs2[2].plot(time, mse_obs, label='Obstacle')
axs2[2].set_title('Mean Squared Error')
axs2[2].set_xlabel('Time (s)')
axs2[2].set_ylabel('MSE')
axs2[2].grid(True)
axs2[2].legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()