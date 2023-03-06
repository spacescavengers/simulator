from Vector import Vector3D

class InitSatelliteState():
    def __init__(self, initPostion: Vector3D, initVelocity: Vector3D, ) -> None:
        self.position = initPostion
        self.velocity = initVelocity