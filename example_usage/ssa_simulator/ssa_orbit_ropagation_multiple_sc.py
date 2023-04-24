from datetime import datetime
from satellite.satellite_impl.test_satellite import TestSatellite
from propagation.state.motion_state import MotionState, SatelliteState
from simulation import Simulation


# Define Start Timestamp
initTimestamp: datetime = datetime.now()

satelliteStates: list[SatelliteState] = []

# Define satellites and their States
sat1MotionState: MotionState = MotionState.fromCoes(initTimestamp, 9000, 0.01, 30.0, 0.0, 0.0, 0.0)
sat1State: SatelliteState = SatelliteState(TestSatellite("Sat1"), sat1MotionState)
satelliteStates.append(sat1State)

# sat2MotionState: MotionState = MotionState.fromCoes(initTimestamp, 40000, 0.35, 10.0, 0.0, 0.0, 0.0)
# sat2State: SatelliteState = SatelliteState(TestSatellite("Sat2"), sat2MotionState)
# satelliteStates.append(sat2State)

simulation: Simulation = Simulation(initTimestamp, satelliteStates, 30000)

simulation.run()
