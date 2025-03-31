import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Rotor and stator parameters
R = 36   # Stator radius
E = 2    # Eccentricity
Rr = 8   # Roller radius
N = 6    # Number of rotor lobes
sharpness = 6.5

# Number of stator pins (one extra)
t = np.linspace(0, 2 * np.pi, 1000)  # Angle parameter

# Reduction factor (eccentricity motion ratio)
reduction_ratio = N / (N - 1)

# Cycloidal rotor equations
def cycloid_rotor(t, theta, posX, posY):
    X = (R * np.cos(t)) - (Rr * np.cos(t + np.arctan(np.sin((1 - N) * t) / ((R / (E * N)) - np.cos((1 - N) * t))))) - (E * np.cos(N * t))
    Y = (-R * np.sin(t)) + (Rr * np.sin(t + np.arctan(np.sin((1 - N) * t) / ((R / (E * N)) - np.cos((1 - N) * t))))) + (E * np.sin(N * t))
    
    # Rotor rotation and translation
    X_rot = X * np.cos(theta) - Y * np.sin(theta) + posX
    Y_rot = X * np.sin(theta) + Y * np.cos(theta) + posY
    
    return X_rot, Y_rot

# Stator equations (fixed)
def cycloid_stator(t):
    Xs = ((R + E - sharpness) * np.cos(t)) - ((Rr - sharpness) * np.cos(t + np.arctan(np.sin((-N) * t) / (((R + E - sharpness) / (E * (N+1))) - np.cos((-N) * t))))) - (E * np.cos((N+1) * t))
    Ys = (-(R + E - sharpness) * np.sin(t)) + ((Rr - sharpness) * np.sin(t + np.arctan(np.sin((-N) * t) / (((R + E - sharpness) / (E * (N+1))) - np.cos((-N) * t))))) + (E * np.sin((N+1) * t))
    return Xs, Ys

# Stator pin positions
theta_pins = np.linspace(0, 2 * np.pi, N, endpoint=False)
pins_x = (R) * np.cos(theta_pins)  
pins_y = (R) * np.sin(theta_pins)

# Eccentricity rotation circle
circle_ex_x = E * np.cos(t)
circle_ex_y = E * np.sin(t)

# Animation setup
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-R - 20, R + 20)
ax.set_ylim(-R - 20, R + 20)
ax.set_aspect('equal')
ax.grid()

# Initial plot
line_rotor, = ax.plot([], [], 'b', lw=2, label="Rotor")
line_stator, = ax.plot([], [], 'r', lw=2, label="Stator (fixed)")
line_ex, = ax.plot([], [], 'g--', lw=1, label="Eccentricity")  # Eccentricity circle
point_ex, = ax.plot([], [], 'go', markersize=5)  # Eccentricity position
pins = [plt.Circle((px, py), Rr, color='r', fill=False) for px, py in zip(pins_x, pins_y)]

# Add pins to the plot
for pin in pins:
    ax.add_patch(pin)

# Initialization function
def init():
    line_rotor.set_data([], [])
    line_stator.set_data([], [])
    line_ex.set_data([], [])
    point_ex.set_data([], [])
    return [line_rotor, line_stator, line_ex, point_ex] + pins

# Animation function
def update(frame):
    theta = -frame * (2 * np.pi / (N * 100))  # Rotor rotation
    posX = E * np.cos(frame * (2 * np.pi / (N * 100)) * (N-1)) 
    posY = E * np.sin(frame * (2 * np.pi / (N * 100)) * (N-1)) 
    
    # Compute rotor curve
    X_rot, Y_rot = cycloid_rotor(t, theta, posX, posY)
    line_rotor.set_data(X_rot, Y_rot)

    # Compute stator curve (fixed)
    Xs, Ys = cycloid_stator(t)
    line_stator.set_data(Xs, Ys)
    
    # Update eccentricity circle
    line_ex.set_data(circle_ex_x, circle_ex_y)  # Fixed circle
    point_ex.set_data([posX], [posY])  # Current eccentricity position
    
    return [line_rotor, line_stator, line_ex, point_ex] + pins

# Create animation
ani = animation.FuncAnimation(fig, update, frames=300, init_func=init, blit=True, interval=50)

plt.title("Animation of cycloidal rotor with eccentricity")
plt.legend()
plt.show()
