from unittest import TestCase
from unittest.mock import Mock

from mapgenerator.algorithms.fortunes import base_structs

class TestPoint(TestCase):
    def setUp(self):
        pass

    def test_konstruktorille_pateva_x_luku(self):
        p = base_structs.Point(10, 20)
        self.assertAlmostEqual(p.x, 10)

    def test_konstruktorille_pateva_y_luku(self):
        p = base_structs.Point(10, 20)
        self.assertAlmostEqual(p.y, 20)

    def test_konstruktorille_epaluku_x(self):
        with self.assertRaises(TypeError):
            base_structs.Point("10", 20)

    def test_point_negatiivinen_x(self):
        p1 = base_structs.Point(10, 20)
        p2 = -p1

        self.assertEqual(p2.x, -(p1.x))

    def test_point_negatiivinen_y(self):
        p1 = base_structs.Point(10, 20)
        p2 = -p1

        self.assertEqual(p2.y, -(p1.y))


class TestEdge(TestCase):
    def setUp(self):
        self.start_point = Mock(spec=base_structs.Point)
        self.end_point = Mock(spec=base_structs.Point)

    def test_konstruktorille_pateva_start_luku(self):
        e = base_structs.Edge(self.start_point, self.end_point)
        self.assertAlmostEqual(e.start, self.start_point)

    def test_konstruktorille_pateva_end_luku(self):
        e = base_structs.Edge(self.start_point, self.end_point)
        self.assertAlmostEqual(e.end, self.end_point)

    def test_konstruktorille_epapateva_start(self):
        start_point = 20

        with self.assertRaises(TypeError):
            e = base_structs.Edge(start_point, self.end_point)

    def test_konstruktorille_epapateva_end(self):
        end_point = 30

        with self.assertRaises(TypeError):
            e = base_structs.Edge(self.start_point, end_point)


class TestRay(TestCase):
    def setUp(self):
        self.start_point = Mock(spec=base_structs.Point)
        self.direction = Mock(spec=base_structs.Point)

    def test_konstruktorille_pateva_start(self):
        r = base_structs.Ray(self.start_point, self.direction)

        self.assertAlmostEqual(r.start, self.start_point)

    def test_konstruktorille_pateva_suunta(self):
        r = base_structs.Ray(self.start_point, self.direction)

        self.assertAlmostEqual(r.direction, self.direction)

    def test_konstruktorille_epapateva_start(self):
        start_point = 10

        with self.assertRaises(TypeError):
            r = base_structs.Ray(start_point, self.direction)

    def test_konstruktorille_epapateva_suunta(self):
        direction = 10

        with self.assertRaises(TypeError):
            r = base_structs.Ray(self.start_point, direction)


class TestArc(TestCase):
    def setUp(self):
        self.focal_point = Mock(spec=base_structs.Point)

    def test_konstruktorille_pateva_focal(self):
        a = base_structs.Arc(self.focal_point)
        self.assertAlmostEqual(a.focal, self.focal_point)

    def test_konstruktorille_epapateva_focal(self):
        focal_point = 30

        with self.assertRaises(TypeError):
            a = base_structs.Arc(focal_point)

    def test_x_patevalle_y(self):
        focal_point = base_structs.Point(5, 10)
        a = base_structs.Arc(focal_point)

        y = 15
        diretrix = 20

        self.assertEqual(a.x(y, diretrix), 12)

    def test_tangent_patevalle_y(self):
        focal_point = base_structs.Point(5, 10)
        a = base_structs.Arc(focal_point)

        y = 15
        diretrix = 20

        self.assertAlmostEqual(a.tangent(y, diretrix).x, 0)

    def test_gaussian_elimination_toimiva_lauseke(self):
        a = base_structs.Arc(self.focal_point)

        matrix = [
            [1, 1,  1, 24],
            [4, 2,  2,  2],
            [1, 1, -1,  6]
        ]

        ans = a._Arc__gauss_elimination(matrix)
        real = [-23, 38, 9]

        self.assertAlmostEqual(ans[0], real[0])
        self.assertAlmostEqual(ans[1], real[1])
        self.assertAlmostEqual(ans[2], real[2])

    def test_ympyra_piste_toimiva_lauseke(self):
        p1 = base_structs.Point(-6, 3)
        p2 = base_structs.Point(-3, 2)
        p3 = base_structs.Point(0, 3)

        a1 = base_structs.Arc(p1)
        a2 = base_structs.Arc(p2)
        a3 = base_structs.Arc(p3)

        raw_ans = a1.circle_point(a2, a3)
        ans = [raw_ans[0].x, raw_ans[0].y, raw_ans[1]]
        real = (-3, 7, 5)

        print(ans)
        self.assertAlmostEqual(ans[0], real[0])
        self.assertAlmostEqual(ans[1], real[1])
        self.assertAlmostEqual(ans[2], real[2])
