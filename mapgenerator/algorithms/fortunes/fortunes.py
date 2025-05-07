""" mapgenerator.algorithms.fortunes """

# kato BinaryTreeLeaf.__init__
from __future__ import annotations

from queue import PriorityQueue

from .base_structs import Point, Arc, Ray, Edge
from .binarytree import BinaryTree, BinaryTreeBark, BinaryTreeLeaf, Side

from .event import Event, EventType


class FortunesAlgorithm:
    def __init__(self, size: tuple[int, int], points: list[Point]):
        """ Size is the canvas size, and points are a list of points
            with to run the algorithm """
        self._size = self.__validate_size(size)
        self._event_queue = PriorityQueue()
        self.add_points(points)

        self._complete = set()
        self._diretrix = 0
        self._beachline = BinaryTree(None)

    def add_points(self, points: list[Point]):
        """ Add a number of sites/points to the canvas """

        for point in points:
            self.add_point(point)

    def add_point(self, point: Point):
        """ Add a new site/point to the canvas """

        point = self.__validate_point(point)

        self._event_queue.put(
            Event(
                x=point.x,
                event_type=EventType.SITE_EVENT,
                point=point
            ),
            block=False
        )

    def get_areas(self) -> list[Edge]:
        """ Return the edges that split up the area """
        while not self._event_queue.empty():
            self.__next_event()

        return self._complete

    def __next_event(self):
        """ Get next event from event queue """
        event = self._event_queue.get()

        self._diretrix = event.x

        if not event.active:
            return

        if event.type == EventType.SITE_EVENT:
            self.__site_event(event.point)
        else:
            self.__circle_event(event.point)

    def __site_event(self, point: Point):
        """ Site events are one of the two types of events,
            that happen everytime a new site (point on the map)
            is discovered """

        new_branch = self.__place_new_site(point)

        if isinstance(new_branch, BinaryTreeLeaf):
            return

        self.__create_circle_events(new_branch)

    def __place_new_site(self, point: Point) -> BinaryTreeBark | BinaryTreeLeaf:
        intersect_leaf, side = self._beachline.find_arc(point.y)

        if intersect_leaf is not None:
            intersect_arc = intersect_leaf.arc
            intersect_point = Point(point.x, intersect_arc.x(point.y, self._diretrix))

            new_branch = self.__site_event_binary_tree_branch(point, intersect_point, intersect_arc)
        else:
            new_branch = BinaryTreeLeaf(
                arc=Arc(
                    focal=point
                )
            )

        if intersect_leaf is not None and intersect_leaf.parent is not None:
            if side == Side.LEFT:
                intersect_leaf.parent.left = new_branch
            elif side == Side.RIGHT:
                intersect_leaf.parent.right = new_branch

        else:
            self._beachline.root = new_branch

        return new_branch

    def __site_event_binary_tree_branch(
            self,
            point: Point,
            intersect_point: Point,
            intersect_arc: Arc
        ) -> BinaryTreeBark:
        """ Return a tree branch for a site event """

        arc_new = BinaryTreeLeaf(
            arc=Arc(
                focal=point
            )
        )

        # Koska teemme uudet arc:it vanhan tilalle, vanha
        # arc vaan jää leijuilemaan. Vaikka Pythonissa
        # Garbage collector hoitaa, jää kuitenkin salee
        # riski muistivuodosta
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

    def __create_circle_events(self, new_branch: BinaryTreeBark):
        new_arc_leaf = new_branch.right.left

        for side, side_arc_leaf in zip(
            [Side.LEFT, Side.RIGHT],
            [new_branch.left, new_branch.right.right]
            ):

            new_arc = new_arc_leaf.arc
            side_arc = side_arc_leaf.arc
            other_arc = self._beachline.find_next_arc(side, side_arc_leaf)

            if other_arc is None:
                return

            circle_point, r = side_arc.circle_point(new_arc, other_arc)

            self._event_queue.put(
                Event(
                    x=circle_point.x + r,
                    event_type=EventType.CIRCLE_EVENT,
                    point=circle_point
                ),
                block=False
            )

    def __circle_event(self, point: Point):
        """ Circle events are the other type of event.
            They happen, when an arc is squished between
            two other arcs """

        leaf_to_delete, leaf_side = self._beachline.find_arc(point.y)

        new_branch = self.__remove_arcs(point, leaf_to_delete, leaf_side)

        self.__create_circle_events(new_branch)

        # Add new completed edges
        self._complete.add(
            Edge(
                start=leaf_to_delete.parent.ray.start,
                end=point
            )
        )
        self._complete.add(
            Edge(
                start=leaf_to_delete.parent.parent.ray.start,
                end=point
            )
        )

    def __remove_arcs(
            self,
            circle_point: Point,
            leaf_to_delete: BinaryTreeLeaf,
            leaf_side: Side
        ) -> BinaryTreeBark:

        if leaf_side == Side.LEFT:
            first_child = leaf_to_delete.parent.right
        else:
            first_child = leaf_to_delete.parent.left

        grandparent = leaf_to_delete.parent.parent
        if grandparent.left == leaf_to_delete.parent:
            grandparent_side = Side.RIGHT
            second_child = grandparent.right
        else:
            grandparent_side = Side.LEFT
            second_child = grandparent.left

        new_branch = BinaryTreeBark(
            ray=Ray(
                start=circle_point,
                direction=circle_point # idkk if this is even needed
            ),
            left=first_child if grandparent_side == Side.RIGHT else second_child,
            right=second_child if grandparent_side == Side.RIGHT else first_child
        )

        megaparent = leaf_to_delete.parent.parent.parent
        if megaparent.left == leaf_to_delete.parent.parent:
            megaparent.left = new_branch

        else:
            megaparent.right = new_branch

        return new_branch

    def __validate_size(self, size: tuple[int, int]) -> tuple[int, int]:
        # TODO:
        return size

    def __validate_point(self, point: Point) -> Point:
        # TODO:
        return point
