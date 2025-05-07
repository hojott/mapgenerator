""" mapgenerator.algorithms.fortunes.base_structs """

# kato BinaryTreeLeaf.__init__
from __future__ import annotations

from math import sqrt

class Point:
    def __init__(self, x: int, y: int):
        # lets try keeping this in ints?
        # floats suck (and might not really work
        # with this alg)
        # https://jacquesheunis.com/post/fortunes-algorithm-implementation/#edge-case-3-precision-issues-with-determining-intersections-of-curves-unsolved
        self._x = self.__validate(x)
        self._y = self.__validate(y)

    def __validate(self, n: int) -> int:
        if not isinstance(n, int):
            raise TypeError("Point attributes must be of type int, was", type(n))

        return n

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
        x = round(
            1/2 * \
            1/(self.focal.x - diretrix) * \
            (y - self.focal.y)**2 + \
            1/2 *\
            (self.focal.x + diretrix)
        )

        return x

    def tangent(self, y: int, diretrix: int) -> Point:
        """ Even magicer math for the arc """
        dx = round(
            1/(self.focal.x - diretrix) * \
            (y - self.focal.y)
        )

        return Point(dx, 1)

    def circle_point( # pylint: disable=too-many-locals
            self,
            arc_one: Arc,
            arc_two: Arc
        ) -> tuple[Point, int]:
        """ Returns radius and center of circle """

        p1 = self.focal
        p2 = arc_one.focal
        p3 = arc_two.focal

        a, b, c, *_ = self.__circle_from_points(p1, p2, p3)

        x = -round(a)
        y = -round(b)
        r = round(sqrt(a**2 + b**2 - c))

        return Point(x, y), r

    def __circle_from_points(self, p1: Point, p2: Point, p3: Point) -> tuple[float, float, float]:
        """ This method takes the equation x² + y² + 2ax + 2by + c = 0,
            and with 3 points return (a, b, c) """

        matrix = [
            [2*p1.x, 2*p1.y, 1, -(p1.x**2 + p1.y**2)],
            [2*p2.x, 2*p2.y, 1, -(p2.x**2 + p2.y**2)],
            [2*p3.x, 2*p3.y, 1, -(p3.x**2 + p3.y**2)],
        ]

        values = self.__gauss_elimination(matrix)

        return tuple(values)

    @staticmethod
    def __gauss_elimination(matrix: list[list[int]]) -> list[int]:
        """ Solve a equation group by gaussian elimination.
            Please don't input groups with less or more than 1 solution
        
            for example...
            matrix w with 3 unknowns:  
                [[00, 01, 02, 03],
                [10, 11, 12, 13],
                [20, 21, 22, 23]]
                
            where X0 is a's scalar, X1 b's, X2 c's and X3 is constant
        """

        for i, _ in enumerate(matrix):

            # first divide by ik / ii
            if matrix[i][i] == 0:
                raise ZeroDivisionError("Stupid sexy division by zero")

            for k, _ in enumerate(matrix[i]):
                if i == k:
                    continue

                matrix[i][k] /= matrix[i][i]

            matrix[i][i] /= matrix[i][i]

            # then divide jk / ji and subtract jk - ik
            for j, _ in enumerate(matrix):
                if j == i:
                    continue

                if matrix[j][i] == 0:
                    continue

                for k, _ in enumerate(matrix[j]):
                    if i == k:
                        continue

                    matrix[j][k] /= matrix[j][i]
                    matrix[j][k] -= matrix[i][k]
                
                matrix[j][i] -= matrix[j][i]

        values = []

        # finally, divide jk / jj
        for j, _ in enumerate(matrix):
            if matrix[j][j] == 0:
                raise RuntimeError("No solutions or something idk")

            # actually only needs jj / jj and j(-1) / jj
            matrix[j][-1] /= matrix[j][j]
            matrix[j][j] /= matrix[j][j]

            # also store the j(-1), cause we need to return them
            values.append(matrix[j][-1])

        return values

    def __validate(self, point: Point) -> Point:
        if not isinstance(point, Point):
            raise TypeError("Arc points must be of type Point, was", type(point))

        return point

    @property
    def focal(self) -> Point:
        return self._focal
