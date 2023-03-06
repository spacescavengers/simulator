import numpy as np
from Vector import Vector3D
from Satellite import Satellite


class OrbitPropagator:

    def __init__(self, dt: float) -> None:
        # Constants
        self.G = 6.67408e-11  # Gravitational constant
        self.M_earth = 5.972e24  # Mass of Earth
        self.R_earth = 6.371e6  # Radius of Earth
        self.J2 = 1.08263e-3  # J2 coefficient for Earth's oblateness
        self.mu = self.G * self.M_earth  # Standard gravitational parameter of Earth
        self.dt = dt

    def __gravity(self, position: Vector3D):
        """Define the acceleration due to gravity function
        """
        a_gravity = -self.mu / position.size**3 * position.array
        return a_gravity

    def __j2(self, position: Vector3D):
        """j2 perturbation
        x = position x
        y = position y
        z = position z
        r_size = np.sqrt(x**2 + y**2 + z**2)
        """
        a_J2 = -3/2 * self.J2 * self.mu / position.size**5 * \
            np.array([
                position.x/position.size*(5*position.z**2/position.size**2-1),
                position.y/position.size*(5*position.z**2/position.size**2-1),
                position.z/position.size*(5*position.z**2/position.size**2-3)
            ])
        return a_J2

    def __drag(self, position: Vector3D, velocity: Vector3D, area: float, drag_coef: float):
        """Atmospheric drag
        r_vector = np.array([x, y, z])
        v_vector = np.array([vx, vy, vz])
        area = Cross-sectional area of satellite (10)
        drag_coef = Drag coefficient of satellite (2.2)
        """
        altitude = position.norm - self.R_earth
        rho = 1.225 * np.exp(-altitude / 8000)  # Atmospheric density
        a_drag = -0.5 * rho * velocity.norm**2 * area * \
            drag_coef / (self.mu/self.R_earth**3) * velocity.array
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

    def propagate(self, position: Vector3D, velocity: Vector3D, satellite: Satellite):
        """Define the simulation function
        TODO: add satelite properties as input param
        """

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

        x = (position.x + velocity.x * self.dt + 0.5 * ax * self.dt**2)
        y = (position.y + velocity.y * self.dt + 0.5 * ay * self.dt**2)
        z = (position.z + velocity.z * self.dt + 0.5 * az * self.dt**2)

        vx = (velocity.x + ax * self.dt)
        vy = (velocity.y + ay * self.dt)
        vz = (velocity.z + az * self.dt)

        newPosition = Vector3D(x, y, z)
        newVelocity = Vector3D(vx, vy, vz)

        return newPosition, newVelocity