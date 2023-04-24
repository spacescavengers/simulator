from abc import ABC, abstractmethod

from common.vector import XYZVector

class Satellite(ABC):

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'getCrossSectionalArea') and 
                callable(subclass.getCrossSectionalArea) and 
                hasattr(subclass, 'getDragCoef') and 
                callable(subclass.getDragCoef) or
                NotImplemented)
    
    @abstractmethod
    def getName(self) -> str:
        """Return name of the satelite"""
        raise NotImplemented
    
    @abstractmethod
    def getCrossSectionArea(self) -> int:
        """Return cross section area of the satellite in [m2]"""
        raise NotImplemented
    
    @abstractmethod
    def getDragCoef(self) -> int:
        """Return cross section area of the satellite"""
        raise NotImplemented
        
    @abstractmethod
    def getMass(self) -> int:
        """Return mass of the satelite in [kg]"""
        raise NotImplemented
    
    # @abstractmethod
    # def getThrustThrustVector(self) -> XYZVector:
    #     """Return the vector of thrust in [N]"""
    #     raise NotImplemented
    
    @abstractmethod
    def getDeltaV(self) -> XYZVector:
        """Return delta V as Vector3D in [m\s]"""
        raise NotImplemented