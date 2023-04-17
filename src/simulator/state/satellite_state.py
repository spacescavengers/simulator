from satellite.satellite import Satellite
from state.motion_state import MotionState

class SatelliteState:
    def __init__(self, satellite: Satellite, motionState: MotionState) -> None:
        self.__satellite: Satellite = satellite
        self.__motionState: MotionState = motionState
    
    def getSatellite(self) -> Satellite:
        return self.__satellite
    
    def getMotionState(self) -> MotionState:
        return self.__motionState
    
    def toString(self):
        return f'Satellite Id: {self.getSatellite().getName()}, \
            Timestamp: {self.getMotionState().getTimestamp()} \
            Posiotion: {self.getMotionState().getPosition().toString()}, \
            Velocity: {self.getMotionState().getVelocity().toString()}'
    

# class SatelliteStates():
#     def __init__(self, satelliteStates: list[SatelliteMotionState]) -> None:
#         self.__satelliteStates = Dict[str, SatelliteMotionState] = dict()
#         self.updateStates(satelliteStates)

#     def updateStates(self, satelliteStates: list[SatelliteMotionState]) -> None:
#         for satelliteState in satelliteStates:
#             self.__satelliteStates[satelliteState.getSatellite().getName()] = satelliteState # possibly add history?

#     def getIterator(self):
#         return iter(self)

#     def __iter__(self):
#         self.__iterator = iter(self.__satelliteStates)
#         return self
    
#     def __next__(self) -> dict_items[str, SatelliteMotionState]:
#         return next(self.__iterator)


