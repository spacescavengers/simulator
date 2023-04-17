import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from datetime import datetime

from earth_orbit_propagator import OrbitPropagator
from satellite.satellite_impl.test_satellite import TestSatellite
from base_models.vector import XYZVector
from satellite.satellite import Satellite
from simulation import Simulation
from state.satellite_state import SatelliteState
from state.motion_state import MotionState


# Simulate the motion of the satellite in a geostationary orbit
alt = 35786000  # altitude of geostationary orbit
r = alt + OrbitPropagator.R_earth
v = np.sqrt(OrbitPropagator.mu / r)

# Define Start Timestamp
initTimestamp: datetime = datetime.now()

# Define satellites and their States
satelliteState1: SatelliteState = SatelliteState(TestSatellite("Sat1"), MotionState(initTimestamp, XYZVector(r, 0, 0), XYZVector(0, v, 0)))
satelliteState2: SatelliteState = SatelliteState(TestSatellite("Sat2"), MotionState(initTimestamp, XYZVector(0, r, 0), XYZVector(-v, 0, 0)))

satelliteStates: list[SatelliteState] = [satelliteState1, satelliteState2]


simulation: Simulation = Simulation(initTimestamp, satelliteStates, 30000)

simulation.run()

