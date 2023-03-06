import numpy as np


class Vector3D:

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.array = np.array([x, y, z])
        self.size = np.sqrt(x**2 + y**2 + z**2)
        self.norm = np.linalg.norm(self.array)
