from abc import ABC, abstractmethod

class Satellite(ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'getCrossSectionalArea') and 
                callable(subclass.getCrossSectionalArea) and 
                hasattr(subclass, 'getDragCoef') and 
                callable(subclass.getDragCoef) or
                NotImplemented)
    
    @abstractmethod
    def getCrossSectionArea(self):
        """Return cross section area of the satellite"""
        raise NotImplemented
    
    @abstractmethod
    def getDragCoef(self):
        """Return cross section area of the satellite"""
        raise NotImplemented