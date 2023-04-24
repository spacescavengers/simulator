
class PhysicalModel:

    def __init__(self, x: int, y: int, z: int, crossSectionArea: int, dragCoeficient: int) -> None:
        # x, y, z - to be replaced by a real model
        self.x = x
        self.y = y
        self.z = z
        self.crossSectionArea = crossSectionArea # should be calculated based on the real model
        self.dragCoeficient = dragCoeficient # should be calculated based on the real model
        
    