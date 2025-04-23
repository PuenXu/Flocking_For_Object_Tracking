import numpy as np
import matplotlib.pyplot as plt

main_data = np.loadtxt('main.csv', delimiter=',', skiprows=1)[:150]
random_data = np.loadtxt('random.csv', delimiter=',', skiprows=1)[:150]

static_data = np.loadtxt('static.csv', delimiter=',', skiprows=1)
rows_to_remove = np.arange(4, 150, 5)
rows_to_keep = np.delete(np.arange(static_data.shape[0]), rows_to_remove)
static_data = static_data[rows_to_keep[:150]]

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

main = extract_columns(main_data)
static = extract_columns(static_data)
random = extract_columns(random_data)

n = len(main['com_x'])
dt = 0.1
time = np.arange(n) * dt

mse_main = np.sqrt((main['com_x'] - main['target_x'])**2 + (main['com_y'] - main['target_y'])**2)
mse_static  = np.sqrt((static['com_x'] - static['target_x'])**2 + (static['com_y'] - static['target_y'])**2)
mse_random  = np.sqrt((random['com_x'] - random['target_x'])**2 + (random['com_y'] - random['target_y'])**2)

fig1, axs1 = plt.subplots(2, 2, figsize=(12, 8))

axs1[0, 0].plot(time, main['en_deviation'], label='No Adversary')
axs1[0, 0].plot(time, static['en_deviation'], label='5 Static Adversarial Nodes')
axs1[0, 0].plot(time, random['en_deviation'], label='5 Random Input Nodes')
axs1[0, 0].set_title('Deviation Energy')
axs1[0, 0].set_xlabel('Time (s)')
axs1[0, 0].set_ylabel('Energy')
axs1[0, 0].grid(True)
# axs1[0, 0].legend()

axs1[0, 1].plot(time, main['vel_mismatch'], label='No Adversary')
axs1[0, 1].plot(time, static['vel_mismatch'], label='5 Static Adversarial Nodes')
axs1[0, 1].plot(time, random['vel_mismatch'], label='5 Random Input Nodes')
axs1[0, 1].set_title('Velocity Mismatch')
axs1[0, 1].set_xlabel('Time (s)')
axs1[0, 1].set_ylabel('Mismatch')
axs1[0, 1].grid(True)
axs1[0, 1].legend()

axs1[1, 0].plot(time, main['connectivity'], label='No Adversary')
axs1[1, 0].plot(time, static['connectivity'], label='5 Static Adversarial Nodes')
axs1[1, 0].plot(time, random['connectivity'], label='5 Random Input Nodes')
axs1[1, 0].set_title('Connectivity')
axs1[1, 0].set_xlabel('Time (s)')
axs1[1, 0].set_ylabel('Connectivity')
axs1[1, 0].grid(True)
# axs1[1, 0].legend()

axs1[1, 1].plot(time, mse_main, label='No Adversary')
axs1[1, 1].plot(time, mse_static, label='5 Static Adversarial Nodes')
axs1[1, 1].plot(time, mse_random, label='5 Random Input Nodes')
axs1[1, 1].set_title('Mean Squared Error')
axs1[1, 1].set_xlabel('Time (s)')
axs1[1, 1].set_ylabel('MSE')
axs1[1, 1].grid(True)
# axs1[1, 1].legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()