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
        self._start = self.__validate_point(start)
        self._end = self.__validate_maybe_none(end)

    def __validate_point(self, point: Point) -> Point:
        if not isinstance(point, Point):
            raise TypeError("Edge points must be of type Point, was", type(point))

        return point

    def __validate_maybe_none(self, point: Point | None) -> Point | None:
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
        if new_end == self.__validate_point(new_end):
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
        return self._end

    @property
    def focal(self) -> Point:
        return self._focal


class BinaryTreeLeaf: # pylint: disable=too-few-public-methods
    def __init__(self, arc: Arc):
        self._arc = self.__validate_arc(arc)

    def __validate_arc(self, arc: Arc) -> Arc:
        if not isinstance(arc, Arc):
            raise TypeError("BinaryTreeLeaf arc must be of type Arc, was", type(arc))

        return arc

    @property
    def arc(self) -> Arc:
        return self._arc


class BinaryTreeBark:
    def __init__(
            self,
            edge: Edge,
            left: Self | BinaryTreeLeaf,
            right: Self | BinaryTreeLeaf
        ):
        """ The idea is that normal nodes are edges, the leaves are arcs """
        self._edge = self.__validate_edge(edge)
        self._left = self.__validate_child(left)
        self._right = self.__validate_child(right)

    def __validate_edge(self, edge: Edge) -> Edge:
        if not isinstance(edge, Edge):
            raise TypeError("BinaryTreeLeaf edge must be of type Edge, was", type(edge))

        return edge

    def __validate_child(self, child: Self | BinaryTreeLeaf) -> Self | BinaryTreeLeaf:
        if not isinstance(child, BinaryTreeBark) and not isinstance(child, BinaryTreeLeaf):
            raise TypeError(
                "BinaryTreeBark child must be of type BinaryTreeBark or BinaryTreeLeaf, was",
                type(child)
            )

        return child

    @property
    def edge(self) -> Edge:
        return self._edge

    @property
    def left(self) -> Self | BinaryTreeLeaf:
        return self._left

    @left.setter
    def left(self, new_left: Self | BinaryTreeLeaf):
        self._left = self.__validate_child(new_left)

    @property
    def right(self) -> Self | BinaryTreeLeaf:
        return self._right

    @right.setter
    def right(self, new_right: Self | BinaryTreeLeaf):
        self._right = self.__validate_child(new_right)


class EventType(Enum):
    SITE_EVENT = 0
    CIRCLE_EVENT = 1


class Event:
    def __init__(self, event_type: EventType, point: Point):
        self._type = self.__validate_type(event_type)
        self._point = self.__validate_point(point)

    def __validate_point(self, point: Point) -> Point:
        if not isinstance(point, Point):
            raise TypeError("Arc points must be of type Point, was", type(point))

        return point

    def __validate_type(self, event_type: EventType) -> EventType:
        if not isinstance(event_type, EventType):
            raise TypeError("Event type must be of type EventType, was", type(event_type))

        return event_type

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
