from base_models.vector import XYZVector, XYZVectors
from satellite.satellite import Satellite
from typing import Dict
from datetime import datetime

class MotionState:
    def __init__(self, timestamp: datetime, position: XYZVector, velocity: XYZVector) -> None:
        self.__timestamp = timestamp
        self.__position = position
        self.__velocity = velocity

    def getTimestamp(self) -> datetime:
        return self.__timestamp

    def getPosition(self) -> XYZVector:
        return self.__position
    
    def getVelocity(self) -> XYZVector:
        return self.__velocity
    
class MotionStates:
    def __init__(self) -> None:
        self.__timestampMotionStateMap: Dict[datetime, MotionState] = dict()
        self.__positions = XYZVectors()
        self.__velocities = XYZVectors()

    def addMotionState(self, motionState: MotionState) -> None:
        # add input validation
        self.__timestampMotionStateMap[motionState.getTimestamp()] = motionState
        self.__positions.addVector(motionState.getPosition())
        self.__velocities.addVector(motionState.getVelocity())

    def getTimestamps(self) -> list[datetime]:
        return self.__timestampMotionStateMap.keys()

    def getPositions(self) -> XYZVectors:
        return self.__positions
    
    def getVelocities(self) -> XYZVectors:
        return self.__velocities
    
    def getMotionStateAt(self, timestamp: datetime) -> MotionState:
        return self.__timestampMotionStateMap.get(timestamp)
    
class MotionTracker:
    def __init__(self, satellite: Satellite) -> None:
        self.__satellite: Satellite = satellite
        self.__motionStates: MotionStates = MotionStates()

    def addMotionState(self, motionState: MotionState) -> None:
        self.__motionStates.addMotionState(motionState)
        
    def getSatellite(self) -> Satellite:
        return self.__satellite
    
    def getPositions(self) -> XYZVectors:
        return self.__motionStates.getPositions()
    
    def getVelocities(self) -> XYZVectors:
        return self.__motionStates.getVelocities()
    
    def getMotionStateAt(self, timestamp: datetime) -> MotionState:
        return self.__motionStates.getMotionStateAt(timestamp)