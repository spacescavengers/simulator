import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from EarthOrbitPropagator import OrbitPropagator
from TestSatellite import TestSatellite
from Vector import Vector3D
from InitSatelliteState import InitSatelliteState
from Visualizer import visualizeInteractiveSatelliteMotion

propagator = OrbitPropagator(5) # 5 seconds
satellite = TestSatellite()

# Simulate the motion of the satellite in a geostationary orbit
alt = 35786000  # altitude of geostationary orbit
r = propagator.R_earth + alt
v = np.sqrt(propagator.mu / r)
period = 24 * 60 * 60  # seconds
t = np.linspace(0, period, 10000)

position = Vector3D(r, 0, 0)
velocity = Vector3D(0, v, 0)
initState = InitSatelliteState(position, velocity)

visualizeInteractiveSatelliteMotion(40000000, 'Motion of Geostationary Satellite',propagator, initState, satellite)
