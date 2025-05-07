""" mapgenerator.algorithms.fortunes.binarytree """

# kato BinaryTreeLeaf.__init__
from __future__ import annotations

from enum import Enum
from typing import Self

from .base_structs import Arc, Ray

class BinaryTreeLeaf:
    def __init__(self, arc: Arc):
        self._arc = self.__validate_arc(arc)

        # kuulemma miten pitää tehä jos viel undefined t. pep-0484
        # self._parent: 'BinaryTreeBark | None' = None
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
        self._left = None
        self._right = None
        self.left = self.__validate_child(left)
        self.right = self.__validate_child(right)
        self._parent: Self | None = None

    def __validate_ray(self, ray: Ray) -> Ray:
        if not isinstance(ray, Ray):
            raise TypeError("BinaryTreeLeaf ray must be of type Ray, was", type(ray))

        return ray

    def __validate_child(self, child: Self | BinaryTreeLeaf) -> Self | BinaryTreeLeaf:
        if not isinstance(child, (BinaryTreeBark, BinaryTreeLeaf)):
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
        new_left._parent = self # pylint: disable=protected-access

    @property
    def right(self) -> Self | BinaryTreeLeaf:
        return self._right

    @right.setter
    def right(self, new_right: Self | BinaryTreeLeaf):
        self._right = self.__validate_child(new_right)
        new_right._parent = self # pylint: disable=protected-access

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
            if child.ray.start.y > y:
                child = child.left
                side = Side.LEFT
            else:
                child = child.right
                side = Side.RIGHT

        return (child, side)

    def find_next_arc(self, side: Side, leaf: BinaryTreeLeaf) -> BinaryTreeLeaf | None:

        # öhh mä en iha tykkää täst implementaatiost,
        # täs tulee joko paljon toistoo tai sit
        # paljon if-lauseit
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

            if isinstance(child, (BinaryTreeLeaf, BinaryTreeBark)):
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

            if isinstance(child, (BinaryTreeLeaf, BinaryTreeBark)):
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

        if not isinstance(root, (BinaryTreeBark, BinaryTreeLeaf)) \
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

        if not isinstance(root, (BinaryTreeBark, BinaryTreeLeaf)):
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
