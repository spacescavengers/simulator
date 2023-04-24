from common.vector import XYZVector, XYZVectors
from common.satellite import Satellite
from typing import Dict
from datetime import datetime
import numpy as np
import spiceypy as spice
import common.constants as constants


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

    @classmethod
    def fromCoes(clazz, timestamp: datetime, 
                 smaInKm: float, ecc: float, incDeg: float,
                 raanDeg: float, argumentOfPeriapsisDeg: float, trueAnomalyDeg: float) -> "MotionState":
        
        r2d = 180.0 / np.pi
        d2r = 1.0 / r2d

        inc = incDeg * d2r
        raan = raanDeg * d2r
        aop = argumentOfPeriapsisDeg * d2r
        ta = trueAnomalyDeg * d2r

        rp = smaInKm * 1000 * (1 - ecc) # * 1000 to convert to [m]

        x, y, z, vx, vy, vz = spice.conics(
            [rp, ecc, inc, raan, aop, ta, 0, constants.mu], timestamp.timestamp())
        return MotionState(timestamp, XYZVector(x, y, z), XYZVector(vx, vy, vz))


class MotionStates:
    def __init__(self) -> None:
        self.__timestampMotionStateMap: Dict[datetime, MotionState] = dict()
        self.__positions = XYZVectors()
        self.__velocities = XYZVectors()

    def addMotionState(self, motionState: MotionState) -> None:
        # add input validation
        self.__timestampMotionStateMap[motionState.getTimestamp(
        )] = motionState
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


