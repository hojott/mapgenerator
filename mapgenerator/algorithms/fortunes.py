""" mapgenerator.algorithms.fortunes """
from queue import PriorityQueue

class FortunesPoint:
    def __init__(self, x: int, y: int):
        # lets try keeping this in ints?
        self._x = self.validate(x)
        self._y = self.validate(y)

    def validate(self, n: int) -> int:
        if not isinstance(n, int):
            raise TypeError("Point attributes must be of type int, was", type(n))
        
        if n < 0:
            raise ValueError("Point attributes must be greater than zero, was", n)

        return n

    def __gt__(self, other):
        return self.x > other.x

    def __lt__(self, other):
        return self.x < other.x

    def __eq__(self, other):
        return self.x == other.x
    
    @property
    def x(self):
        return self._x
        
    @property
    def y(self):
        return self._y

class FortunesAlgorithm:
    def __init__(self, size: tuple[int, int], points: list[FortunesPoint]):
        self._size = self.__validate_size(size)
        self._points = self.__priority_queue(self.__validate_points(points))

    def __priority_queue(self, points: list[FortunesPoint]) -> PriorityQueue[FortunesPoint]:
        pq = PriorityQueue()

        for p in points:
            pq.put(p, block=False) # will raise error if pq is full

        return pq

    def __validate_size(self, size: tuple[int, int]) -> tuple[int, int]:
        # TODO:
        return size

    def __validate_points(self, points: list[FortunesPoint]) -> list[FortunesPoint]:
        # TODO:
        return points

