import unittest
from mapgenerator.algorithms import fortunes

class TestFortunesPoint(unittest.TestCase):
    def setUp(self):
        pass

    def test_konstruktorille_pateva_x_luku(self):
        p = fortunes.FortunesPoint(10, 20)
        self.assertAlmostEqual(p.x, 10)

    def test_konstruktorille_pateva_y_luku(self):
        p = fortunes.FortunesPoint(10, 20)
        self.assertAlmostEqual(p.y, 20)

    def test_konstruktorille_huono_x_luku(self):
        with self.assertRaises(ValueError):
            fortunes.FortunesPoint(-10, 20)
    
    def test_konstruktorille_epaluku_x(self):
        with self.assertRaises(TypeError):
            fortunes.FortunesPoint("10", 20)

    def test_konstruktorille_liian_suuri_x(self):
        # TODO:
        # x isompi kuin algoritmille annettu koko
        self.assertTrue(True)

class TestFortunesEdge(unittest.TestCase):
    def setUp(self):
        "kirjottelen myöhemmin"

class TestFortunesArc(unittest.TestCase):
    def setUp(self):
        "kirjottelen myöhemmin"

class TestFortunesBinaryTreeBark(unittest.TestCase):
    def setUp(self):
        "kirjottelen myöhemmin"

class TestFortunesBinaryTreeLeaf(unittest.TestCase):
    def setUp(self):
        "kirjottelen myöhemmin"
