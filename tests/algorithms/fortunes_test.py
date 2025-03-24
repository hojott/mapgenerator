import unittest
from mapgenerator.algorithms import fortunes

class TestPoint(unittest.TestCase):
    def setUp(self):
        pass

    def test_konstruktorille_pateva_x_luku(self):
        p = fortunes.Point(10, 20)
        self.assertAlmostEqual(p.x, 10)

    def test_konstruktorille_pateva_y_luku(self):
        p = fortunes.Point(10, 20)
        self.assertAlmostEqual(p.y, 20)

    def test_konstruktorille_huono_x_luku(self):
        with self.assertRaises(ValueError):
            fortunes.Point(-10, 20)

    def test_konstruktorille_epaluku_x(self):
        with self.assertRaises(TypeError):
            fortunes.Point("10", 20)


class TestEdge(unittest.TestCase):
    def setUp(self):
        pass

    def test_konstruktorille_pateva_start_luku(self):
        start_point = fortunes.Point(10, 20)
        end_point = fortunes.Point(30, 40)

        e = fortunes.Edge(start_point, end_point)
        self.assertAlmostEqual(e.start, start_point)

    def test_konstruktorille_pateva_end_luku(self):
        start_point = fortunes.Point(10, 20)
        end_point = fortunes.Point(30, 40)

        e = fortunes.Edge(start_point, end_point)
        self.assertAlmostEqual(e.end, end_point)

    def test_konstruktorille_end_none(self):
        start_point = fortunes.Point(10, 20)
        end_point = None

        e = fortunes.Edge(start_point, end_point)
        self.assertAlmostEqual(e.end, end_point)

    def test_lisaa_end_point(self):
        start_point = fortunes.Point(10, 20)
        end_point = None

        e = fortunes.Edge(start_point, end_point)

        new_end_point = fortunes.Point(30, 40)
        e.end = new_end_point

        self.assertAlmostEqual(e.end, new_end_point)


class TestArc(unittest.TestCase):
    def setUp(self):
        "kirjottelen myöhemmin"

class TestBinaryTreeBark(unittest.TestCase):
    def setUp(self):
        "kirjottelen myöhemmin"

class TestBinaryTreeLeaf(unittest.TestCase):
    def setUp(self):
        "kirjottelen myöhemmin"

class TestEvent(unittest.TestCase):
    def setUp(self):
        "kirjottelen myöhemmin"

class TestFortunesAlgorithm(unittest.TestCase):
    def setUp(self):
        "kirjottelen myöhemmin"
