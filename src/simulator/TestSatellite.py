from Satellite import Satellite


class TestSatellite(Satellite):

    def __init__(self) -> None:
        super().__init__()
        self.crossSectionArea = 10
        self.dragCoef = 2.2
    
    
    def getCrossSectionArea(self):
        return self.crossSectionArea
    
    def getDragCoef(self):
        return self.dragCoef