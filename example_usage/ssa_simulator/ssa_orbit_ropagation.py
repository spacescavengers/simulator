import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from earth_orbit_propagator import OrbitPropagator
from satellite.satellite_impl.test_satellite import TestSatellite
from base_models.vector import XYZVector
from state.satellite_state import InitSatelliteState
from visualization.visualizer import visualizeInteractiveSatelliteMotion

propagator = OrbitPropagator(5) # 5 seconds
satellite = TestSatellite()

# Simulate the motion of the satellite in a geostationary orbit
alt = 35786000  # altitude of geostationary orbit
r = propagator.__R_earth + alt
v = np.sqrt(propagator.__mu / r)
period = 24 * 60 * 60  # seconds
t = np.linspace(0, period, 10000)

position = XYZVector(r, 0, 0)
velocity = XYZVector(0, v, 0)
initState = InitSatelliteState(position, velocity)

visualizeInteractiveSatelliteMotion(xyzMinMax=40000000,
                                    title='Motion of Geostationary Satellite',
                                    propagator=propagator, 
                                    initState=initState, 
                                    satellite=satellite)
