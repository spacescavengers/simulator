import logging as log
from typing import Dict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

from common.satellite import Satellite
from propagation.state.motion_state import MotionState


class SimpleVisualizer:

    def __init__(self, satelliteMotionStateMap: Dict[Satellite, MotionState], redrawStepSize: int) -> None:
        self.__fig = None
        self.__ax = None
        self.__step = 0
        self.__redrawStepSize = redrawStepSize

        self.__intializePlot(40000000, "SSA Simulation")

        self.__satellitesMap: Dict[Satellite,
                                   SatelliteVisualizationState] = dict()
        for satellite, motionState in satelliteMotionStateMap.items():
            log.info(
                f'Initializing Visualization State: Satellite Name: {satellite.getName()} - Possion: {motionState.getPosition()}')
            self.__satellitesMap[satellite] = SatelliteVisualizationState(
                self.__ax, satellite, motionState)

    # def addSatellite(self, satellite: Satellite, motionState: MotionState) -> None:
    #     self.__satelites[]

    def updateFig(self, satelliteMotionStateMap: Dict[Satellite, MotionState]):
        redraw: bool = self.__step % self.__redrawStepSize == 0
        for satellite, motionState in satelliteMotionStateMap.items():
            if self.__satellitesMap.get(satellite) is not None:
                self.__satellitesMap.get(satellite).addState(motionState)
                if(redraw):
                    self.__satellitesMap.get(satellite).updatePlot()
            else:
                log.warn(
                    f'Could not find satellite with name: {satellite.getName()}')

        if(redraw):
            # self.__fig.canvas.draw()
            self.__fig.canvas.flush_events()
        
        self.__step += 1

    # def on_key_press(event):
    #     # increase abs velocity in x direction by 50
    #     if event.key == '7':
    #         if vxs[-1] > 0:
    #             vxs[-1] = vxs[-1] + 50
    #         else:
    #             vxs[-1] = vxs[-1] - 50

    #     if event.key == '4':  # decrease abs velocity in x direction by 50
    #         if vxs[-1] > 0:
    #             vxs[-1] = vxs[-1] - 50
    #         else:
    #             vxs[-1] = vxs[-1] + 50

    #     elif event.key == '8':  # increase abs velocity in y direction by 50
    #         if vys[-1] > 0:
    #             vys[-1] = vys[-1] + 50
    #         else:
    #             vys[-1] = vys[-1] - 50

    #     elif event.key == '5':  # decrease abs velocity in y direction by 50
    #         if vys[-1] > 0:
    #             vys[-1] = vys[-1] - 50
    #         else:
    #             vys[-1] = vys[-1] + 50

    #     elif event.key == '9':  # increase abs velocity in z direction by 50
    #         if vzs[-1] > 0:
    #             vzs[-1] = vzs[-1] + 50
    #         else:
    #             vzs[-1] = vzs[-1] - 50

    #     elif event.key == '6':  # decrease abs velocity in z direction by 50
    #         if vzs[-1] > 0:
    #             vzs[-1] = vzs[-1] - 50
    #         else:
    #             vzs[-1] = vzs[-1] + 50
    #     else:
    #         xmin, xmax = ax.get_xlim()
    #         ymin, ymax = ax.get_ylim()
    #         if event.key == 'up':
    #             ax.set_ylim(ymin + 1000000, ymax + 1000000)
    #         elif event.key == 'down':
    #             ax.set_ylim(ymin - 1000000, ymax - 1000000)
    #         elif event.key == 'left':
    #             ax.set_xlim(xmin - 1000000, xmax - 1000000)
    #         elif event.key == 'right':
    #             ax.set_xlim(xmin + 1000000, xmax + 1000000)

    def __intializePlot(self,
                        xyzMinMax: int,
                        title: str):
        plt.ion()
        # Plot the motion of the satellite
        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        self.__fig, self.__ax = plt.subplots(subplot_kw=dict(projection="3d"))
        self.__ax.set_xlim(-xyzMinMax, xyzMinMax)  # 40000000
        self.__ax.set_ylim(-xyzMinMax, xyzMinMax)
        self.__ax.set_zlim(-xyzMinMax, xyzMinMax)
        self.__ax.set_aspect('equal')
        self.__ax.set_xlabel('X (m)')
        self.__ax.set_ylabel('Y (m)')
        self.__ax.set_zlabel('Z (m)')
        self.__ax.set_title(title)  # 'Motion of Geostationary Satellite'

        # Add a simple visualization of the Earth
        theta = np.linspace(0, 2*np.pi, 100)
        phi = np.linspace(0, np.pi, 100)
        R_earth = 6.371e6  # Radius of Earth (create constant class)
        x_earth = R_earth * np.outer(np.cos(theta), np.sin(phi))
        y_earth = R_earth * np.outer(np.sin(theta), np.sin(phi))
        z_earth = R_earth * np.outer(np.ones(100), np.cos(phi))
        self.__ax.plot_surface(x_earth, y_earth, z_earth, cmap='Blues')

        # plt.show()
        # ani.save('animation.gif', writer='imagemagick', fps=10)


class SatelliteVisualizationState:
    def __init__(self, axes: Axes, satellite: Satellite, motionState: MotionState) -> None:
        self.__name = satellite.getName()
        self.__axes = axes
        self.__xPositions = []
        self.__yPositions = []
        self.__zPositions = []
        self.__xVelocity: float
        self.__yVelocity: float
        self.__zVelocity: float
        self.__orbit = None
        self.__vX = None
        self.__vY = None
        self.__vZ = None
        self.addState(motionState)
        self.__updatePlot()

    def getName(self):
        return self.__name

    def __updatePlot(self) -> None:
        log.info(f'Drawing satellite at possion: [{self.__xPositions[-1]}, {self.__yPositions[-1]}, {self.__zPositions[-1]}]')
        self.__orbit, = self.__axes.plot(
            self.__xPositions, self.__yPositions, self.__zPositions)
        self.__satellite, = self.__axes.plot(
            self.__xPositions[-1], self.__yPositions[-1], self.__zPositions[-1], 'o')
        
        self.__vX = self.__axes.quiver(self.__xPositions[-1], self.__yPositions[-1], self.__zPositions[-1],
                                       self.__xVelocity, 0, 0, length=abs(self.__xVelocity), color='black')
        self.__vY = self.__axes.quiver(self.__xPositions[-1], self.__yPositions[-1], self.__zPositions[-1],
                                       0, self.__yVelocity, 0, length=abs(self.__yVelocity), color='green')
        self.__vZ = self.__axes.quiver(self.__xPositions[-1], self.__yPositions[-1], self.__zPositions[-1],
                                       0, 0, self.__zVelocity, length=abs(self.__zVelocity), color='purple')

    def updatePlot(self) -> None:
        self.__orbit.remove()
        self.__satellite.remove()
        self.__vX.remove()
        self.__vY.remove()
        self.__vZ.remove()
        self.__updatePlot()

    def addState(self, motionState: MotionState):
        self.__xPositions.append(motionState.getPosition().getX())
        self.__yPositions.append(motionState.getPosition().getY())
        self.__zPositions.append(motionState.getPosition().getZ())
        self.__xVelocity = motionState.getVelocity().getX()
        self.__yVelocity = motionState.getVelocity().getY()
        self.__zVelocity = motionState.getVelocity().getZ()
