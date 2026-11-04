import math
from interfejsy import IVector

class Vector2D(IVector):
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def get_components(self) -> list[float]:
        return [self._x, self._y]

    def abs(self) -> float:
        return math.sqrt(self._x**2 + self._y**2)

    def c_dot(self, param: IVector) -> float:
        p = param.get_components()
        #obsługa wektorów, które mogą mieć mniej wymiarów
        py = p[1] if len(p) > 1 else 0.0
        return self._x * p[0] + self._y * py

class Vector3D(IVector):

    def __init__(self, x: float, y: float, z: float):
        self._x = x
        self._y = y
        self._z = z

    def get_components(self) -> list[float]:
        return [self._x, self._y, self._z]

    def abs(self) -> float:
        return math.sqrt(self._x**2 + self._y**2 + self._z**2)

    def c_dot(self, param: IVector) -> float:
        p = param.get_components()
        py = p[1] if len(p) > 1 else 0.0
        pz = p[2] if len(p) > 2 else 0.0
        return self._x * p[0] + self._y * py + self._z * pz

    def __str__(self) -> str:
        return f"[{self._x:.4f}, {self._y:.4f}, {self._z:.4f}]"