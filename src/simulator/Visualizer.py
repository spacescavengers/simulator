import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from EarthOrbitPropagator import OrbitPropagator
from InitSatelliteState import InitSatelliteState
from Vector import Vector3D
from Satellite import Satellite


orbit = satellite_dot = qx = qy = qz = None

def visualizeInteractiveSatelliteMotion(xyzMinMax: int, title: str,
                                        propagator: OrbitPropagator, initState: InitSatelliteState, 
                                        satellite: Satellite):
    # Plot the motion of the satellite
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
    ax.set_xlim(-xyzMinMax, xyzMinMax) # 40000000
    ax.set_ylim(-xyzMinMax, xyzMinMax)
    ax.set_zlim(-xyzMinMax, xyzMinMax)
    ax.set_aspect('equal')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title(title) # 'Motion of Geostationary Satellite'

    # Add a simple visualization of the Earth
    theta = np.linspace(0, 2*np.pi, 100)
    phi = np.linspace(0, np.pi, 100)
    x_earth = propagator.R_earth * np.outer(np.cos(theta), np.sin(phi))
    y_earth = propagator.R_earth * np.outer(np.sin(theta), np.sin(phi))
    z_earth = propagator.R_earth * np.outer(np.ones(100), np.cos(phi))
    ax.plot_surface(x_earth, y_earth, z_earth, cmap='Blues')


    xs = [initState.position.x]
    ys = [initState.position.y]
    zs = [initState.position.z]
    vxs = [initState.velocity.x]
    vys = [initState.velocity.y]
    vzs = [initState.velocity.z]

    def updateFig(i):
        # global satellite
        for i in range(1, 100): # redraw after 100 propagations
            position = Vector3D(xs[-1], ys[-1], zs[-1])
            velocity = Vector3D(vxs[-1], vys[-1], vzs[-1])
            newPosition, newVelocity = propagator.propagate(position, velocity, satellite)

            xs.append(newPosition.x)
            ys.append(newPosition.y)
            zs.append(newPosition.z)
            vxs.append(newVelocity.x)
            vys.append(newVelocity.y)
            vzs.append(newVelocity.z)

        global orbit
        if(orbit is not None):
            orbit.remove()
        orbit, = ax.plot(xs, ys, zs, 'b')

        # Plot satellite position
        global satellite_dot
        if(satellite_dot is not None):
            satellite_dot.remove()
        satellite_dot, = ax.plot(xs[-1], ys[-1], zs[-1], 'ro')

        # Add velocity vectors to the plot
        global qx
        if(qx is not None):
            qx.remove()
        qx = ax.quiver(xs[-1], ys[-1], zs[-1], vxs[-1], 0, 0, length=abs(vxs[-1]), color='purple')
        global qy
        if(qy is not None):
            qy.remove()
        qy = ax.quiver(xs[-1], ys[-1], zs[-1], 0, vys[-1], 0, length=abs(vys[-1]), color='green')
        global qz
        if(qz is not None):
            qz.remove()
        qz = ax.quiver(xs[-1], ys[-1], zs[-1], 0, 0, vzs[-1], length=abs(vzs[-1]), color='black')

    def on_key_press(event):
        # increase abs velocity in x direction by 50
        if event.key == '7':
            if vxs[-1] > 0:
                vxs[-1] = vxs[-1] + 50
            else:
                vxs[-1] = vxs[-1] - 50

        if event.key == '4': # decrease abs velocity in x direction by 50
            if vxs[-1] > 0:
                vxs[-1] = vxs[-1] - 50
            else:
                vxs[-1] = vxs[-1] + 50
        
        elif event.key == '8': # increase abs velocity in y direction by 50
            if vys[-1] > 0:
                vys[-1] = vys[-1] + 50
            else:
                vys[-1] = vys[-1] - 50

        elif event.key == '5': # decrease abs velocity in y direction by 50
            if vys[-1] > 0:
                vys[-1] = vys[-1] - 50
            else:
                vys[-1] = vys[-1] + 50

        elif event.key == '9': # increase abs velocity in z direction by 50
            if vzs[-1] > 0:
                vzs[-1] = vzs[-1] + 50
            else:
                vzs[-1] = vzs[-1] - 50

        elif event.key == '6': # decrease abs velocity in z direction by 50
            if vzs[-1] > 0:
                vzs[-1] = vzs[-1] - 50
            else:
                vzs[-1] = vzs[-1] + 50
        else:
            xmin, xmax = ax.get_xlim()
            ymin, ymax = ax.get_ylim()
            if event.key == 'up':
                ax.set_ylim(ymin + 1000000, ymax + 1000000)
            elif event.key == 'down':
                ax.set_ylim(ymin - 1000000, ymax - 1000000)
            elif event.key == 'left':
                ax.set_xlim(xmin - 1000000, xmax - 1000000)
            elif event.key == 'right':
                ax.set_xlim(xmin + 1000000, xmax + 1000000)


    # Connect the key press event to the figure
    fig.canvas.mpl_connect('key_press_event', on_key_press)

    ani = FuncAnimation(fig, updateFig, interval=20, blit=False) # frames=steps
    plt.show()
    # ani.save('animation.gif', writer='imagemagick', fps=10) 