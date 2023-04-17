from satellite.satellite import Satellite
from satellite.physical_model import PhysicalModel
from base_models.vector import XYZVector


class TestSatellite(Satellite):

    def __init__(self, name:str) -> None:
        super().__init__()
        # self.physicalModel = PhysicalModel()
        self.__name = name
        self.__crossSectionArea = 10
        self.__dragCoef = 2.2
        self.__mass = 150

        self.__stepCounter = 0
        self.__zeroDeltaV = XYZVector(0, 0, 0)
    
    def getName(self) -> str:
        return self.__name
    
    def getCrossSectionArea(self):
        return self.__crossSectionArea
    
    def getDragCoef(self):
        return self.__dragCoef
    
    def getMass(self):
        return self.__mass
    
    def getDeltaV(self) -> XYZVector:
        self.__stepCounter+=1

        # if(self.__stepCounter % 25 == 0):
        #     return XYZVector(25, 25, 25)
        return self.__zeroDeltaV