""" mapgenerator.algorithms.fortunes """
from __future__ import annotations

from math import floor
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

        return n

    def __gt__(self, other):
        # might be redundant, will fix later
        return self.x > other.x

    def __lt__(self, other):
        return self.x < other.x

    def __eq__(self, other):
        # might be redundant, will fix later
        return self.x == other.x

    def __neg__(self):
        return Point(-self.x, -self.y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Edge:
    def __init__(self, start: Point, end: Point):
        """ Edges are defined by their start- and endpoint, and are set in stone """
        self._start = self.__validate(start)
        self._end = self.__validate(end)

    def __validate(self, point: Point) -> Point:
        if not isinstance(point, Point):
            raise TypeError("Edge points must be of type Point, was", type(point))

        return point

    @property
    def start(self) -> Point:
        return self._start

    @property
    def end(self) -> Point:
        return self._end


class Ray:
    def __init__(self, start: Point, direction: Point):
        """ Rays are defined by their startpoint and direction """
        self._start = self.__validate(start)
        self._direction = self.__validate(direction)

    def __validate(self, point: Point) -> Point:
        if not isinstance(point, Point):
            raise TypeError("Edge points must be of type Point, was", type(point))

        return point

    @property
    def start(self) -> Point:
        return self._start

    @property
    def direction(self) -> Point:
        return self._direction


class Arc:
    def __init__(self, focal: Point):
        """ Arcs are defined by their focal point and their (grand)parents on the binary tree """
        self._focal = self.__validate(focal)

    def x(self, y: int, diretrix: int) -> int:
        """ Magic math for the arc """
        x = floor(
            1/2 * \
            1/(self.focal.x - diretrix) * \
            (y - self.focal.y)**2 + \
            1/2 *\
            (self.focal.x + diretrix)
        )

        return x

    def tangent(self, y: int, diretrix: int) -> Point:
        """ Even magicer math for the arc """
        dx = floor(
            1/(self.focal.x - diretrix) * \
            (y - self.focal.y)
        )

        return Point(dx, 1)

    def __validate(self, point: Point) -> Point:
        if not isinstance(point, Point):
            raise TypeError("Arc points must be of type Point, was", type(point))

        return point

    @property
    def focal(self) -> Point:
        return self._focal


class BinaryTreeLeaf: # pylint: disable=too-few-public-methods
    def __init__(self, arc: Arc):
        self._arc = self.__validate_arc(arc)

        # kuulemma miten pitää tehä jos viel undefined t. pep-0484
        # self._parent: 'BinaryTreeBark' | None = None
        # ...
        # https://stackoverflow.com/a/55344418
        # mä vihaan python tyypitystä
        self._parent: BinaryTreeBark | None = None

    def __validate_arc(self, arc: Arc) -> Arc:
        if not isinstance(arc, Arc):
            raise TypeError("BinaryTreeLeaf arc must be of type Arc, was", type(arc))

        return arc

    @property
    def arc(self) -> Arc:
        return self._arc

    @property
    def parent(self) -> BinaryTreeBark | None:
        """" will be set by binary tree bark """
        return self._parent


class BinaryTreeBark:
    def __init__(
            self,
            ray: Ray,
            left: Self | BinaryTreeLeaf,
            right: Self | BinaryTreeLeaf
        ):
        """ The idea is that normal nodes are rays, the leaves are arcs """
        self._ray = self.__validate_ray(ray)
        self._left = self.__validate_child(left)
        self._right = self.__validate_child(right)
        self._parent: Self | None = None

    def __validate_ray(self, ray: Ray) -> Ray:
        if not isinstance(ray, Ray):
            raise TypeError("BinaryTreeLeaf ray must be of type Ray, was", type(ray))

        return ray

    def __validate_child(self, child: Self | BinaryTreeLeaf) -> Self | BinaryTreeLeaf:
        if not isinstance(child, BinaryTreeBark) and not isinstance(child, BinaryTreeLeaf):
            raise TypeError(
                "BinaryTreeBark child must be of type BinaryTreeBark or BinaryTreeLeaf, was",
                type(child)
            )

        return child

    @property
    def ray(self) -> Ray:
        return self._ray

    @property
    def left(self) -> Self | BinaryTreeLeaf:
        return self._left

    @left.setter
    def left(self, new_left: Self | BinaryTreeLeaf):
        self._left = self.__validate_child(new_left)
        new_left._parent = self

    @property
    def right(self) -> Self | BinaryTreeLeaf:
        return self._right

    @right.setter
    def right(self, new_right: Self | BinaryTreeLeaf):
        self._right = self.__validate_child(new_right)
        new_right._parent = self

    @property
    def parent(self) -> Self | None:
        return self._parent


class Side(Enum):
    LEFT = 0
    RIGHT = 1


class BinaryTree:
    def __init__(self, root: BinaryTreeBark | BinaryTreeLeaf | None):
        self._root = self.__validate_initial(root)

    def find_arc(self, y: int) -> tuple[BinaryTreeLeaf | None, BinaryTreeBark | None, Side | None]:
        child: BinaryTreeBark | BinaryTreeLeaf | None = self.root
        side: Side | None = None

        while isinstance(child, BinaryTreeBark):
            if child.ray.y > y:
                child = child.left
                side = Side.LEFT
            else:
                child = child.right
                side = Side.RIGHT

        return (child, side)

    def find_next_arc(self, side: Side, leaf: BinaryTreeLeaf) -> BinaryTreeLeaf | None:
        if side == Side.LEFT:
            return self.__find_next_arc_left(leaf)

        return self.__find_next_arc_right(leaf)

    def __find_next_arc_left(self, leaf: BinaryTreeLeaf) -> BinaryTreeLeaf | None:
        if leaf.parent is None:
            return None

        parent = leaf.parent
        while parent.parent is not None:
            parent = parent.parent
            child = parent.left

            if child is None:
                continue

            if isinstance(child, BinaryTreeLeaf) \
            or isinstance(child, BinaryTreeBark):
                break

        if parent.parent is None:
            return None

        child = parent.parent
        while not isinstance(child, BinaryTreeLeaf):
            if child.right is not None:
                child = child.right
            else:
                child = child.left

        return child

    def __find_next_arc_right(self, leaf: BinaryTreeLeaf) -> BinaryTreeLeaf | None:
        if leaf.parent is None:
            return None

        parent = leaf.parent
        while parent.parent is not None:
            parent = parent.parent
            child = parent.right

            if child is None:
                continue

            if isinstance(child, BinaryTreeLeaf) \
            or isinstance(child, BinaryTreeBark):
                break

        if parent.parent is None:
            return None

        child = parent.parent
        while not isinstance(child, BinaryTreeLeaf):
            if child.left is not None:
                child = child.left
            else:
                child = child.right

        return child


    def __validate_initial(
        self,
        root: BinaryTreeBark | BinaryTreeLeaf | None
    ) -> BinaryTreeBark | BinaryTreeLeaf | None:

        if not isinstance(root, BinaryTreeBark) \
        and not isinstance(root, BinaryTreeLeaf) \
        and root is not None:
            raise TypeError(
                "BinaryTree root must be of type BinaryTreeBark, BinaryTreeLeaf or None was",
                type(root)
            )

        return root

    def __validate_new(
        self,
        root: BinaryTreeBark | BinaryTreeLeaf
    ) -> BinaryTreeBark | BinaryTreeLeaf:

        if not isinstance(root, BinaryTreeBark) and not isinstance(root, BinaryTreeLeaf):
            raise TypeError(
                "BinaryTree root must be of type BinaryTreeBark or BinaryTreeLeaf was",
                type(root)
            )

        return root

    @property
    def root(self) -> BinaryTreeBark | BinaryTreeLeaf | None:
        return self._root

    @root.setter
    def root(self, new_root: BinaryTreeBark | BinaryTreeLeaf):
        self._root = self.__validate_new(new_root)


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
        self._beachline = BinaryTree(None)

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
        """ Site events are one of the two types of events,
            that happen everytime a new site (point on the map)
            is discovered """

        # TODO: Siivoa :D

        intersect_leaf, side = self._beachline.find_arc(point.y)

        if intersect_leaf is not None:
            intersect_arc = intersect_leaf.arc
            intersect_point = Point(point.x, intersect_arc.y(point.x, self._diretrix))

            new_branch = self.__new_binary_tree_branch(point, intersect_point, intersect_arc)
        else:
            new_branch = BinaryTreeLeaf(
                arc=Arc(
                    focal=point
                )
            )

        if intersect_leaf.parent is not None:
            if side == Side.LEFT:
                intersect_leaf.parent.left = new_branch
            elif side == Side.RIGHT:
                intersect_leaf.parent.right = new_branch

        else:
            self._beachline.root = new_branch

        # Find circle events for new branch
        new_arc = new_branch.right.left
        for side, side_arc in zip(
            [Side.LEFT, Side.RIGHT],
            [new_branch.left, new_branch.right.right]
        ):
            #other_arc = self._beachline.find_next_arc(side, side_arc)

            #circle_point = side_arc.circle_point(new_arc, other_arc)
            circle_point = Point(10, 10)

            self._event_queue.put(
                Event(
                    event_type=EventType.CIRCLE_EVENT,
                    point=circle_point
                ),
                block=False
            )


    def __new_binary_tree_branch(
        self,
        point: Point,
        intersect_point: Point,
        intersect_arc: Arc
    ) -> BinaryTreeBark:

        arc_new = BinaryTreeLeaf(
            arc=Arc(
                focal=point
            )
        )

        # Koska teemme uudet arc:it vanhan tilalle, vanha
        # arc vaan jää leijuilemaan. Vaikka Pythonissa
        # Garbage collector hoitaa, jää kuitenkin
        # muistivuodosta
        arc_left = BinaryTreeLeaf(
            arc=Arc(
                focal=intersect_arc.focal
            )
        )

        arc_right = BinaryTreeLeaf(
            arc=Arc(
                focal=intersect_arc.focal
            )
        )

        ray_right = BinaryTreeBark(
            ray=Ray(
                start=intersect_point,
                direction=intersect_arc.tangent(intersect_point.y, self._diretrix)
            ),
            left=arc_new,
            right=arc_right
        )

        ray_left = BinaryTreeBark(
            ray=Ray(
                start=intersect_point,
                direction=-intersect_arc.tangent(intersect_point.y, self._diretrix)
            ),
            left=arc_left,
            right=ray_right
        )

        return ray_left

    def __circle_event(self, point):
        pass

    def __validate_size(self, size: tuple[int, int]) -> tuple[int, int]:
        # TODO:
        return size

    def __validate_point(self, point: Point) -> Point:
        # TODO:
        return point
