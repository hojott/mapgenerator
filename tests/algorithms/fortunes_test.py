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
        "kirjottelen myöhemmin"

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
