import logging as log
import numpy as np
import datetime
from datetime import datetime, timedelta

from common.vector import XYZVector
from propagation.state.motion_state import MotionState, SatelliteState
from common.satellite import Satellite

import common.constants as constants


class OrbitPropagator:

    def __init__(self, dt: int) -> None:
        self.__dtInMillis: int = dt  # deltaT (step size) in [ms]
        self.__dtInSeconds: float = dt / 1000

    def __gravity(self, position: XYZVector):
        """Define the acceleration due to gravity function
        """
        a_gravity = -constants.mu / position.getSize()**3 * position.asNpArray()
        log.info(f'Gravity: {a_gravity}')
        return a_gravity

    def __j2(self, position: XYZVector):
        """j2 perturbation
        x = position x
        y = position y
        z = position z
        r_size = np.sqrt(x**2 + y**2 + z**2)
        """
        z2 = position.getZ()**2
        position_size2 = position.getSize()**2

        # a_J2 = -1.5 * constants.J2 * constants.mu / position.getSize()**5 * \
        #     np.array([
        #         position.getX()/position.getSize() * (5*z2/position_size2-1),
        #         position.getY()/position.getSize() * (5*z2/position_size2-1),
        #         position.getZ()/position.getSize() * (5*z2/position_size2-3)
        #     ])

        a_J2 = -1.5 * constants.J2 * constants.mu * constants.R_earth ** 2 \
            / position_size2 ** 2 * \
            np.array([
                position.getX()/position.getSize() * (5*z2/position_size2-1),
                position.getY()/position.getSize() * (5*z2/position_size2-1),
                position.getZ()/position.getSize() * (5*z2/position_size2-3)
            ])

        log.info(f'J2: {a_J2}')
        return a_J2

    def __drag(self, position: XYZVector, velocity: XYZVector, area: float, drag_coef: float) -> float:
        """Atmospheric drag
        r_vector = np.array([x, y, z])
        v_vector = np.array([vx, vy, vz])
        area = Cross-sectional area of satellite (10)
        drag_coef = Drag coefficient of satellite (2.2)
        """
        altitude = position.getNorm() - constants.R_earth
        rho = 1.225 * np.exp(-altitude / 8000)  # Atmospheric density
        a_drag = -0.5 * rho * velocity.getNorm()**2 * area * \
            drag_coef / (constants.mu/constants.R_earth**3) * \
            velocity.asNpArray()
        log.info(f'Drag: {a_drag}')
        return a_drag

    # def __solarRadiationPresure(self, r_vector):
    #     """TODO: review this method
    #     Solar radiation pressure
    #     r_vector = np.array([x, y, z])
    #     """
    #
    #     beta = 1  # Reflectivity coefficient of satellite
    #     P = 4.56e-6  # Solar radiation pressure at 1 AU
    #     d = np.linalg.norm(r)  # Distance from satellite to Sun
    #     A = 10  # Cross-sectional area of satellite
    #     F_srp = -P * beta * A / d**2 * r / np.linalg.norm(r)
    #     return F_srp

    def propagate(self, satellite: Satellite, motionState: MotionState) -> MotionState:
        """Define the simulation function
        TODO: add satelite properties as input param
        """
        log.info(
            f'Input state: [Position: {motionState.getPosition().toString()}, Velocity: {motionState.getVelocity().toString()}]')
        timestamp: datetime = motionState.getTimestamp()
        position: XYZVector = motionState.getPosition()
        stateVelocity: XYZVector = motionState.getVelocity()
        satellitesDeltaV: XYZVector = satellite.getDeltaV()
        velocity = stateVelocity.plus(satellitesDeltaV)

        a_perturb = np.zeros(3)  # Initialize perturbation acceleration
        # Gravitational perturbations
        a_perturb += self.__gravity(position)
        # J2 perturbations
        a_perturb += self.__j2(position)
        # Atmospheric drag
        a_perturb += self.__drag(position, velocity,
                                 satellite.getCrossSectionArea(), satellite.getDragCoef())
        # Solar radiation pressure
        # a_perturb += self.__solarRadiationPresure(x0, y0, z0)

        ax, ay, az = a_perturb

        x = (position.getX() + velocity.getX() *
             self.__dtInSeconds + 0.5 * ax * self.__dtInSeconds**2)
        y = (position.getY() + velocity.getY() *
             self.__dtInSeconds + 0.5 * ay * self.__dtInSeconds**2)
        z = (position.getZ() + velocity.getZ() *
             self.__dtInSeconds + 0.5 * az * self.__dtInSeconds**2)

        vx = (velocity.getX() + ax * self.__dtInSeconds)
        vy = (velocity.getY() + ay * self.__dtInSeconds)
        vz = (velocity.getZ() + az * self.__dtInSeconds)

        newTimestamp = timestamp + timedelta(milliseconds=self.__dtInMillis)
        newPosition = XYZVector(x, y, z)
        newVelocity = XYZVector(vx, vy, vz)
        log.info(
            f'New state: [Position: {newPosition.toString()}, Velocity: {newVelocity.toString()}]')
        return MotionState(newTimestamp, newPosition, newVelocity)
