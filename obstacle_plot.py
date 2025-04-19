import matplotlib.pyplot as plt
import numpy as np

# Circle parameters
x, y = 85, 50     # Center of the circle
r = np.sqrt(100+(85-50)**2)            # Radius
theta = np.linspace(0, 2*np.pi, 100)
circle_x = x + r * np.cos(theta)
circle_y = y + r * np.sin(theta)

rec_x = [50, 120, 120, 50, 50]
rec_y = [40, 40, 60, 60, 40]

target_x, target_y = 20, 50
target_x_end, target_y_end = 150, 50

# Create figure and axes
fig, ax = plt.subplots()
ax.set_xlim(0, 200)
ax.set_ylim(0, 120)
ax.set_aspect('equal', 'box')

# Plot the obstacle and points
ax.plot(rec_x, rec_y, color='black', linewidth=1, label='Obstacle')
ax.plot([], [], color='black', label='Wall', linewidth=2)
ax.plot(circle_x, circle_y, 'b--', label='Bounding Circle')
ax.plot(target_x, target_y, 'y*', label='Target Init Pos')
ax.plot(target_x_end, target_y_end, 'r*', label='Target End Pos')

# Function to draw a horizontal wall with hatch lines
def draw_wall(y_wall, direction='down', length=200, num_lines=40, hatch_length=3):
    spacing = length / num_lines
    for i in range(num_lines + 1):
        x0 = i * spacing
        x1 = x0 + hatch_length
        y0 = y_wall
        y1 = y_wall - hatch_length if direction == 'down' else y_wall + hatch_length
        ax.plot([x0, x1], [y0, y1], color='black', linewidth=1)
    ax.plot([0, length], [y_wall, y_wall], color='black', linewidth=2)

# Draw wall at y = 20 (bottom wall)
draw_wall(y_wall=20, direction='down')

# Draw wall at y = 80 (top wall)
draw_wall(y_wall=80, direction='up')

# Labels, title, legend
ax.set_xlabel('x position (m)')
ax.set_ylabel('y position (m)')
ax.set_title('Tracking with Rectangular Obstacle')
legend = ax.legend(loc='upper right')
legend.get_frame().set_facecolor('white')   # Solid white background
legend.get_frame().set_alpha(1.0) 
ax.grid(True)

plt.show()