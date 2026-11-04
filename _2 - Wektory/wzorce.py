import math
from interfejsy import IVector, IPolar2D
from modele import Vector2D, Vector3D

#Adapter
class Polar2DAdapter(IVector, IPolar2D):
    def __init__(self, src_vector: Vector2D):
        self._src_vector = src_vector

    def get_angle(self) -> float:
        c = self._src_vector.get_components()
        return math.atan2(c[1], c[0])

    def abs(self) -> float:
        return self._src_vector.abs()

    def c_dot(self, param: IVector) -> float:
        return self._src_vector.c_dot(param)

    def get_components(self) -> list[float]:
        return self._src_vector.get_components()


#Dekorator
class Vector3DDecorator(IVector):
    def __init__(self, src_vector: IVector, z: float):
        self._src_vector = src_vector
        self._z = z

    def get_components(self) -> list[float]:
        b = self._src_vector.get_components()
        bx = b[0] if len(b) > 0 else 0.0
        by = b[1] if len(b) > 1 else 0.0
        return [bx, by, self._z]

    def abs(self) -> float:
        c = self.get_components()
        return math.sqrt(c[0]**2 + c[1]**2 + self._z**2)

    def c_dot(self, param: IVector) -> float:
        c = self.get_components()
        p = param.get_components()
        py = p[1] if len(p) > 1 else 0.0
        pz = p[2] if len(p) > 2 else 0.0
        return c[0] * p[0] + c[1] * py + self._z * pz

    def cross(self, param: IVector) -> Vector3D:
        a = self.get_components()
        b = param.get_components()
        
        #jeśli parametr jest 2D, jego z = 0
        bz = b[2] if len(b) > 2 else 0.0
        by = b[1] if len(b) > 1 else 0.0
        
        #metoda macierzowa
        return Vector3D(
            a[1] * bz - a[2] * by,
            a[2] * b[0] - a[0] * bz,
            a[0] * by - a[1] * b[0]
        )

    def get_src_v(self) -> IVector:
        return self._src_vector

#Dziedziczenie
class Vector3DInheritance(Vector2D):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y)
        self._z = z

    def get_components(self) -> list[float]:
        b = super().get_components()
        return [b[0], b[1], self._z]

    def abs(self) -> float:
        b = super().get_components()
        return math.sqrt(b[0]**2 + b[1]**2 + self._z**2)

    def c_dot(self, param: IVector) -> float:
        b = super().get_components()
        p = param.get_components()
        py = p[1] if len(p) > 1 else 0.0
        pz = p[2] if len(p) > 2 else 0.0
        return b[0] * p[0] + b[1] * py + self._z * pz

    def cross(self, param: IVector) -> Vector3D:
        a = self.get_components()
        b = param.get_components()
        
        bz = b[2] if len(b) > 2 else 0.0
        by = b[1] if len(b) > 1 else 0.0
        
        return Vector3D(
            a[1] * bz - a[2] * by,
            a[2] * b[0] - a[0] * bz,
            a[0] * by - a[1] * b[0]
        )

    def get_src_v(self) -> IVector:
        return self