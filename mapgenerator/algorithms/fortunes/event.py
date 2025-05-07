""" mapgenerator.algorithms.fortunes.event """

# kato BinaryTreeLeaf.__init__
from __future__ import annotations

from enum import Enum
from typing import Self

from .base_structs import Point

class EventType(Enum):
    SITE_EVENT = 0
    CIRCLE_EVENT = 1


class Event:
    def __init__(self, x: int, event_type: EventType, point: Point):
        """ The x axis of the event, the events type and a point that
            goes with the event depending on type """
        self._x = self.__validate_int(x)
        self._type = self.__validate_type(event_type)
        self._point = self.__validate_point(point)
        self._active = True

    def __validate_point(self, point: Point) -> Point:
        if not isinstance(point, Point):
            raise TypeError("Event points must be of type Point, was", type(point))

        return point

    def __validate_type(self, event_type: EventType) -> EventType:
        if not isinstance(event_type, EventType):
            raise TypeError("Event type must be of type EventType, was", type(event_type))

        return event_type

    def __validate_int(self, x: int) -> int:
        if not isinstance(x, int):
            raise TypeError("Event x must be of type int, was", type(x))

        return x

    def __lt__(self, other: Self) -> bool:
        # for the priority queue
        return self.x < other.x

    @property
    def type(self) -> EventType:
        return self._type

    @property
    def point(self) -> Point:
        return self._point

    @property
    def x(self) -> int:
        return self._x

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, new_status: bool):
        self._active = new_status
