class IVector():
    def abs(self) -> float:
        pass

    def c_dot(self, param: 'IVector') -> float:
        pass

    def get_components(self) -> list[float]:
        pass

class IPolar2D():
    def get_angle(self) -> float:
        pass

    def abs(self) -> float:
        pass