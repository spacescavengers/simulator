import logging as log
from typing import Dict, List
import datetime
from datetime import datetime, timedelta

from state.motion_state import MotionState, MotionTracker
from state.satellite_state import SatelliteState
from earth_orbit_propagator import OrbitPropagator
from satellite.satellite import Satellite
from visualization.visualizer import SimpleVisualizer

class Simulation:

    def __init__(self, initialTimestamp: datetime, initialSatelliteStates: list[SatelliteState], stepCount: int) -> None:
        self.__configureLogging()

        self.__timestamp: datetime = initialTimestamp
        self.__stepCount: int = stepCount
        self.__stepSize: int = 10000 # time in [ms] (default to 10s)
        self.__propagator: OrbitPropagator = OrbitPropagator(self.__stepSize)

        # to be intialized
        self.__satellites: list[Satellite] = []

        # Define satellite state maps
        self.__satelliteMotionTrackerMap: Dict[Satellite, MotionTracker] = dict()
        # ...
        self.__visualizer: SimpleVisualizer

        self.__init(initialSatelliteStates)

    def run(self):
        for step in range(0, self.__stepCount):
            log.info(f'step: {str(step)}')
            self.__step()

    def __step(self) -> None:
        for sattelite in self.__satellites:
            self.__satelliteStep(sattelite)

        # update timestamp
        self.__timestamp = self.__timestamp + timedelta(milliseconds=self.__stepSize)

        self.__visualizer.updateFig(self.__extractSatelliteLastMotionStateMap())



    def __satelliteStep(self, satellite: Satellite) -> None:
        # Here we will call satellite performAction method

        # update individual trackers
        self.__updateSatellitesMotion(satellite)

    def __init(self, initialSatelliteStates: list[SatelliteState]) -> None:
        log.info(f'Initializing SateliteMotionTrackerMap')
        for satelliteState in initialSatelliteStates:
            self.__satellites.append(satelliteState.getSatellite())
            # add id motion tracker entry
            log.info(f'adding entry: {satelliteState.toString()}')
            self.__satelliteMotionTrackerMap[satelliteState.getSatellite()] = self.__initMotionTracker(satelliteState)

        self.__visualizer = SimpleVisualizer(self.__extractSatelliteLastMotionStateMap(), 100)

    def __initMotionTracker(self, satelliteState: SatelliteState) -> MotionTracker:
        motionTracker: MotionTracker = MotionTracker(satelliteState.getSatellite())
        motionTracker.addMotionState(satelliteState.getMotionState())
        return motionTracker
    
    def __updateSatellitesMotion(self, satellite: Satellite):
        motionTracker: MotionTracker = self.__satelliteMotionTrackerMap.get(satellite)
        currentMotionState: MotionState = motionTracker.getMotionStateAt(self.__timestamp)
        newMotionSate: MotionState = self.__propagator.propagate(satellite, currentMotionState)
        motionTracker.addMotionState(newMotionSate)

    def __extractSatelliteLastMotionStateMap(self) -> Dict[Satellite, MotionState]:
        satelliteMotionStateMap: Dict[Satellite, MotionState] = dict()

        for satellite, motionTracker in self.__satelliteMotionTrackerMap.items():
            satelliteMotionStateMap[satellite] = motionTracker.getMotionStateAt(self.__timestamp)

        return satelliteMotionStateMap
    
    def __configureLogging(self):
        log.basicConfig(format='%(asctime)s - %(message)s', level=log.INFO)
        log.debug("Logger was set up")