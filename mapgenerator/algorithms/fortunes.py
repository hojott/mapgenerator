""" mapgenerator.algorithms.fortunes """
from queue import PriorityQueue

from typing import Self
from enum import Enum

class Point:
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
        # might be redundant, will fix later
        return self.x > other.x

    def __lt__(self, other):
        return self.x < other.x

    def __eq__(self, other):
        # might be redundant, will fix later
        return self.x == other.x

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Edge:
    def __init__(self, start: Point, end: Point | None):
        self._start = self.__validate_start(start)
        self._end = self.__validate_end(end)

    def __validate_start(self, point: Point) -> Point:
        if not isinstance(point, Point):
            raise TypeError("Edge points must be of type Point, was", type(point))

        return point

    def __validate_end(self, point: Point | None) -> Point | None:
        if not isinstance(point, Point) and point is not None:
            raise TypeError("Edge points must be of type Point, was", type(point))

        return point

    @property
    def start(self) -> Point:
        return self._start

    @property
    def end(self) -> Point | None:
        return self._end

    @end.setter
    def end(self, new_end: Point | None):
        if new_end == self.__validate_end(new_end):
            self._end = new_end


class Arc:
    def __init__(self, start: Point, end: Point, focal: Point):
        self._start = self.__validate(start)
        self._end = self.__validate(end)
        self._focal = self.__validate(focal)

    def __validate(self, point: Point) -> Point:
        if not isinstance(point, Point):
            raise TypeError("Arc points must be of type Point, was", type(point))

        return point

    @property
    def start(self) -> Point:
        return self._start

    @property
    def end(self) -> Point:
        return self._start

    @property
    def focal(self) -> Point:
        return self._focal


class BinaryTreeLeaf: # pylint: disable=too-few-public-methods
    def __init__(self, point: Arc):
        self._point = point

    @property
    def point(self) -> Arc:
        return self._point


class BinaryTreeBark:
    def __init__(
            self,
            point: Edge,
            left: Self | BinaryTreeLeaf,
            right: Self | BinaryTreeLeaf
        ):
        """ The idea is that normal nodes are edges, the leaves are arcs """
        self._point = point
        self._left = left
        self._right = right

    @property
    def point(self) -> Edge:
        return self._point

    @property
    def left(self) -> Self | BinaryTreeLeaf:
        return self._left

    @left.setter
    def left(self, new_left: Self | BinaryTreeLeaf):
        self._left = new_left

    @property
    def right(self) -> Self | BinaryTreeLeaf:
        return self._right

    @right.setter
    def right(self, new_right: Self | BinaryTreeLeaf):
        self._right = new_right


class EventType(Enum):
    SITE_EVENT = 0
    CIRCLE_EVENT = 1


class Event:
    def __init__(self, event_type: EventType, point: Point):
        self._type = event_type
        self._point = point

    @property
    def type(self) -> EventType:
        return self._type

    @property
    def point(self) -> Point:
        return self._point


class FortunesAlgorithm:
    def __init__(self, size: tuple[int, int], points: list[Point]):
        self._size = self.__validate_size(size)
        self._event_queue = PriorityQueue()
        self.add_points(points)

        self._complete = []
        self._diretrix = 0
        self._beachline = None

    def get_areas(self):
        while not self._event_queue.empty():
            self.__next_event()

        return self._complete

    def add_points(self, points: list[Point]):
        """ Add a number of sites/points to the canvas """

        for point in points:
            self.add_point(point)

    def add_point(self, point: Point):
        """ Add a new site/point to the canvas """

        point = self.__validate_point(point)

        self._event_queue.put(
            Event(
                EventType.SITE_EVENT,
                point
            ),
            block=False
        )

    def __next_event(self):
        event = self._event_queue.get()

        self._diretrix = event.point.x

        if event.type == EventType.SITE_EVENT:
            self.__site_event(event.point)
        else:
            self.__circle_event(event.point)

    def __site_event(self, point):
        pass

    def __circle_event(self, point):
        pass

    def __validate_size(self, size: tuple[int, int]) -> tuple[int, int]:
        # TODO:
        return size

    def __validate_point(self, point: Point) -> Point:
        # TODO:
        return point
