import numpy as np

# Create an abstract class vector if needed for the future


class XYZVector:

    def __init__(self, x: float, y: float, z: float) -> None:
        self.__x = x
        self.__y = y
        self.__z = z
        self.__asarray = [self.__x, self.__y, self.__z]
        self.__asnparray = np.array(self.asList())
        # self.__size = np.sqrt(x**2 + y**2 + z**2)
        self.__size = np.sqrt(self.__asnparray.dot(self.__asnparray))
        self.__norm = self.__size    

    def getX(self) -> float:
        return self.__x

    def getY(self) -> float:
        return self.__y

    def getZ(self) -> float:
        return self.__z

    def getSize(self) -> float:
        return self.__size

    def getNorm(self) -> float:
        return self.__norm

    def asList(self) -> list[float]:
        """Returns [x, y, z] coordinates as array"""
        return self.__asarray

    def asNpArray(self) -> np.ndarray:
        """Returns [x, y, z] coordinates as numpy array"""
        return self.__asnparray

    def plus(self, other: 'XYZVector') -> 'XYZVector':
        """Returns a new vector that is addition of self plus other"""
        return XYZVector(self.__x + other.getX(), self.__y + other.getY(), self.__z + other.getZ())

    def __str__(self) -> str:
        return f'[{self.__x},{self.__y},{self.__z}]'

    def toString(self):
        return self.__str__()


class XYZVectors:

    def __init__(self, vectors: list[XYZVector] = []) -> None:
        self.__vectors = vectors

    def addVector(self, vector: XYZVector) -> None:
        self.__vectors.append(vector)

    def getXs(self) -> list[float]:
        return [vector.getX() for vector in self.__vectors]

    def getYs(self) -> list[float]:
        return [vector.getY() for vector in self.__vectors]

    def getZs(self) -> list[float]:
        return [vector.getZ() for vector in self.__vectors]

    def getXsAsNpArray(self) -> np.ndarray:
        return np.array(self.getXs())

    def getYsAsNpArray(self) -> np.ndarray:
        return np.array(self.getYs())

    def getZsAsNpArray(self) -> np.ndarray:
        return np.array(self.getZs())

    def getListOfLists(self) -> list[float]:
        return [vector.asList() for vector in self.__vectors]

    def getNpArrayOfNpArrays(self) -> np.ndarray:
        return np.array([vector.asNpArray() for vector in self.__vectors])

    def getLastVector(self) -> XYZVector:
        return self.__vectors[-1]
