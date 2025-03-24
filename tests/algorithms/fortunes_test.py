from unittest import TestCase
from unittest.mock import Mock

from mapgenerator.algorithms import fortunes

class TestPoint(TestCase):
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

    def test_point_pienempi_kuin(self):
        p1 = fortunes.Point(10, 20)
        p2 = fortunes.Point(20, 20)

        self.assertLess(p1, p2)

    def test_point_suurempi_kuin(self):
        p1 = fortunes.Point(10, 20)
        p2 = fortunes.Point(20, 20)

        self.assertGreater(p2, p1)

    def test_point_yhtakuin(self):
        p1 = fortunes.Point(10, 20)
        p2 = fortunes.Point(10, 30)

        self.assertEqual(p2, p1)

class TestEdge(TestCase):
    def setUp(self):
        self.start_point = Mock(spec=fortunes.Point)
        self.end_point = Mock(spec=fortunes.Point)

    def test_konstruktorille_pateva_start_luku(self):
        e = fortunes.Edge(self.start_point, self.end_point)
        self.assertAlmostEqual(e.start, self.start_point)

    def test_konstruktorille_pateva_end_luku(self):
        e = fortunes.Edge(self.start_point, self.end_point)
        self.assertAlmostEqual(e.end, self.end_point)

    def test_konstruktorille_end_none(self):
        end_point = None

        e = fortunes.Edge(self.start_point, end_point)
        self.assertAlmostEqual(e.end, end_point)

    def test_lisaa_end_point(self):
        end_point = None

        e = fortunes.Edge(self.start_point, end_point)

        e.end = self.end_point

        self.assertAlmostEqual(e.end, self.end_point)

    def test_lisaa_end_none(self):
        end_point = None

        e = fortunes.Edge(self.start_point, end_point)

        new_end_point = None

        with self.assertRaises(TypeError):
            e.end = new_end_point

    def test_konstruktorille_start_none(self):
        start_point = None

        with self.assertRaises(TypeError):
            e = fortunes.Edge(start_point, self.end_point)

    def test_konstruktorille_end_epa_point_arvo(self):
        end_point = 30

        with self.assertRaises(TypeError):
            e = fortunes.Edge(self.start_point, end_point)


class TestArc(TestCase):
    def setUp(self):
        self.start_point = Mock(spec=fortunes.Point)
        self.end_point = Mock(spec=fortunes.Point)
        self.focal_point = Mock(spec=fortunes.Point)

    def test_konstruktorille_pateva_start_luku(self):
        a = fortunes.Arc(self.start_point, self.end_point, self.focal_point)
        self.assertAlmostEqual(a.start, self.start_point)

    def test_konstruktorille_pateva_end_luku(self):
        a = fortunes.Arc(self.start_point, self.end_point, self.focal_point)
        self.assertAlmostEqual(a.end, self.end_point)

    def test_konstruktorille_pateva_focal_luku(self):
        a = fortunes.Arc(self.start_point, self.end_point, self.focal_point)
        self.assertAlmostEqual(a.focal, self.focal_point)

    def test_konstruktorille_epa_point_arvo(self):
        end_point = 30

        with self.assertRaises(TypeError):
            a = fortunes.Arc(self.start_point, end_point, self.focal_point)


class TestBinaryTreeLeaf(TestCase):
    def setUp(self):
        self.arc = Mock(spec=fortunes.Arc)

    def test_konstruktorille_pateva_arc(self):
        l = fortunes.BinaryTreeLeaf(self.arc)
        self.assertAlmostEqual(l.arc, self.arc)

    def test_konstruktorille_epapateva_arc(self):
        arc = 10

        with self.assertRaises(TypeError):
            l = fortunes.BinaryTreeLeaf(arc)


class TestBinaryTreeBark(TestCase):
    def setUp(self):
        self.edge = Mock(spec=fortunes.Edge)
        self.left_bark = Mock(spec=fortunes.BinaryTreeBark)
        self.right_bark = Mock(spec=fortunes.BinaryTreeBark)
        self.left_leaf = Mock(spec=fortunes.BinaryTreeLeaf)
        self.right_leaf = Mock(spec=fortunes.BinaryTreeLeaf)

    def test_konstruktorille_pateva_edge(self):
        b = fortunes.BinaryTreeBark(self.edge, self.left_bark, self.right_bark)

        self.assertAlmostEqual(b.edge, self.edge)

    def test_konstruktorille_pateva_vasen_bark(self):
        b = fortunes.BinaryTreeBark(self.edge, self.left_bark, self.right_bark)

        self.assertAlmostEqual(b.left, self.left_bark)

    def test_konstruktorille_pateva_oikea_bark(self):
        b = fortunes.BinaryTreeBark(self.edge, self.left_bark, self.right_bark)

        self.assertAlmostEqual(b.right, self.right_bark)

    def test_konstruktorille_pateva_vasen_leaf(self):
        b = fortunes.BinaryTreeBark(self.edge, self.left_leaf, self.right_bark)

        self.assertAlmostEqual(b.left, self.left_leaf)

    def test_konstruktorille_pateva_oikea_leaf(self):
        b = fortunes.BinaryTreeBark(self.edge, self.left_bark, self.right_leaf)

        self.assertAlmostEqual(b.right, self.right_leaf)

    def test_konstruktorille_epapateva_edge(self):
        edge = 10

        with self.assertRaises(TypeError):
            b = fortunes.BinaryTreeBark(edge, self.left_bark, self.right_bark)

    def test_konstruktorille_epapateva_lapsi(self):
        left_bark = 10

        with self.assertRaises(TypeError):
            b = fortunes.BinaryTreeBark(self.edge, left_bark, self.right_bark)

    def test_lisaa_pateva_vasen_lapsi(self):
        b = fortunes.BinaryTreeBark(self.edge, self.left_bark, self.right_bark)

        b.left = self.left_leaf

        self.assertAlmostEqual(b.left, self.left_leaf)

    def test_lisaa_pateva_oikea_lapsi(self):
        b = fortunes.BinaryTreeBark(self.edge, self.left_bark, self.right_bark)

        b.right = self.right_leaf

        self.assertAlmostEqual(b.right, self.right_leaf)

    def test_lisaa_epapateva_vasen_lapsi(self):
        b = fortunes.BinaryTreeBark(self.edge, self.left_bark, self.right_bark)

        with self.assertRaises(TypeError):
            b.left = 10

    def test_lisaa_epapateva_oikea_lapsi(self):
        b = fortunes.BinaryTreeBark(self.edge, self.left_bark, self.right_bark)

        with self.assertRaises(TypeError):
            b.right = 10


class TestEvent(TestCase):
    def setUp(self):
        self.event_type = Mock(spec=fortunes.EventType)
        self.point = Mock(spec=fortunes.Point)

    def test_konstruktorille_pateva_piste(self):
        e = fortunes.Event(self.event_type, self.point)

        self.assertAlmostEqual(e.point, self.point)

    def test_konstruktorille_pateva_site_event(self):
        event_type = fortunes.EventType.SITE_EVENT

        e = fortunes.Event(event_type, self.point)

        self.assertAlmostEqual(e.type, event_type)

    def test_konstruktorille_pateva_circle_event(self):
        event_type = fortunes.EventType.CIRCLE_EVENT

        e = fortunes.Event(event_type, self.point)

        self.assertAlmostEqual(e.type, fortunes.EventType.CIRCLE_EVENT)

    def test_konstruktorille_epapateva_piste(self):
        point = 10

        with self.assertRaises(TypeError):
            e = fortunes.Event(self.event_type, point)

    def test_konstruktorille_epapateva_event_tyyppi(self):
        event_type = 10

        with self.assertRaises(TypeError):
            e = fortunes.Event(event_type, self.point)


class TestFortunesAlgorithm(TestCase):
    def setUp(self):
        "kirjottelen myöhemmin"
