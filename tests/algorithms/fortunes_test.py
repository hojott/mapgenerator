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

    def test_point_negatiivinen_x(self):
        p1 = fortunes.Point(10, 20)
        p2 = -p1

        self.assertEqual(p2.x, -(p1.x))

    def test_point_negatiivinen_y(self):
        p1 = fortunes.Point(10, 20)
        p2 = -p1

        self.assertEqual(p2.y, -(p1.y))


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

    def test_konstruktorille_epapateva_start(self):
        start_point = 20

        with self.assertRaises(TypeError):
            e = fortunes.Edge(start_point, self.end_point)

    def test_konstruktorille_epapateva_end(self):
        end_point = 30

        with self.assertRaises(TypeError):
            e = fortunes.Edge(self.start_point, end_point)


class TestRay(TestCase):
    def setUp(self):
        self.start_point = Mock(spec=fortunes.Point)
        self.direction = Mock(spec=fortunes.Point)

    def test_konstruktorille_pateva_start(self):
        r = fortunes.Ray(self.start_point, self.direction)

        self.assertAlmostEqual(r.start, self.start_point)

    def test_konstruktorille_pateva_suunta(self):
        r = fortunes.Ray(self.start_point, self.direction)

        self.assertAlmostEqual(r.direction, self.direction)

    def test_konstruktorille_epapateva_start(self):
        start_point = 10

        with self.assertRaises(TypeError):
            r = fortunes.Ray(start_point, self.direction)

    def test_konstruktorille_epapateva_suunta(self):
        direction = 10

        with self.assertRaises(TypeError):
            r = fortunes.Ray(self.start_point, direction)


class TestArc(TestCase):
    def setUp(self):
        self.focal_point = Mock(spec=fortunes.Point)

    def test_konstruktorille_pateva_focal(self):
        a = fortunes.Arc(self.focal_point)
        self.assertAlmostEqual(a.focal, self.focal_point)

    def test_konstruktorille_epapateva_focal(self):
        focal_point = 30

        with self.assertRaises(TypeError):
            a = fortunes.Arc(focal_point)

    def test_x_patevalle_y(self):
        focal_point = fortunes.Point(5, 10)
        a = fortunes.Arc(focal_point)

        y = 15
        diretrix = 20

        self.assertEqual(a.x(y, diretrix), 11)

    def test_tangent_patevalle_y(self):
        focal_point = fortunes.Point(5, 10)
        a = fortunes.Arc(focal_point)

        y = 15
        diretrix = 20

        self.assertAlmostEqual(a.tangent(y, diretrix).x, -1)


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
        self.ray = Mock(spec=fortunes.Ray)
        self.left_bark = Mock(spec=fortunes.BinaryTreeBark)
        self.right_bark = Mock(spec=fortunes.BinaryTreeBark)
        self.left_leaf = Mock(spec=fortunes.BinaryTreeLeaf)
        self.right_leaf = Mock(spec=fortunes.BinaryTreeLeaf)

    def test_konstruktorille_pateva_ray(self):
        b = fortunes.BinaryTreeBark(self.ray, self.left_bark, self.right_bark)

        self.assertAlmostEqual(b.ray, self.ray)

    def test_konstruktorille_pateva_vasen_bark(self):
        b = fortunes.BinaryTreeBark(self.ray, self.left_bark, self.right_bark)

        self.assertAlmostEqual(b.left, self.left_bark)

    def test_konstruktorille_pateva_oikea_bark(self):
        b = fortunes.BinaryTreeBark(self.ray, self.left_bark, self.right_bark)

        self.assertAlmostEqual(b.right, self.right_bark)

    def test_konstruktorille_pateva_vasen_leaf(self):
        b = fortunes.BinaryTreeBark(self.ray, self.left_leaf, self.right_bark)

        self.assertAlmostEqual(b.left, self.left_leaf)

    def test_konstruktorille_pateva_oikea_leaf(self):
        b = fortunes.BinaryTreeBark(self.ray, self.left_bark, self.right_leaf)

        self.assertAlmostEqual(b.right, self.right_leaf)

    def test_konstruktorille_epapateva_ray(self):
        ray = 10

        with self.assertRaises(TypeError):
            b = fortunes.BinaryTreeBark(ray, self.left_bark, self.right_bark)

    def test_konstruktorille_epapateva_lapsi(self):
        left_bark = 10

        with self.assertRaises(TypeError):
            b = fortunes.BinaryTreeBark(self.ray, left_bark, self.right_bark)

    def test_lisaa_pateva_vasen_lapsi(self):
        b = fortunes.BinaryTreeBark(self.ray, self.left_bark, self.right_bark)

        b.left = self.left_leaf

        self.assertAlmostEqual(b.left, self.left_leaf)

    def test_lisaa_pateva_oikea_lapsi(self):
        b = fortunes.BinaryTreeBark(self.ray, self.left_bark, self.right_bark)

        b.right = self.right_leaf

        self.assertAlmostEqual(b.right, self.right_leaf)

    def test_lisaa_epapateva_vasen_lapsi(self):
        b = fortunes.BinaryTreeBark(self.ray, self.left_bark, self.right_bark)

        with self.assertRaises(TypeError):
            b.left = 10

    def test_lisaa_epapateva_oikea_lapsi(self):
        b = fortunes.BinaryTreeBark(self.ray, self.left_bark, self.right_bark)

        with self.assertRaises(TypeError):
            b.right = 10


class TestBinaryTree(TestCase):
    def setUp(self):
        self.bark = Mock(spec=fortunes.BinaryTreeBark)
        self.leaf = Mock(spec=fortunes.BinaryTreeLeaf)

        self.bark_oikea = Mock(spec=fortunes.BinaryTreeBark)
        self.leaf_vasen = Mock(spec=fortunes.BinaryTreeLeaf)
        self.leaf_oikea = Mock(spec=fortunes.BinaryTreeLeaf)

    def test_konstruktorille_none(self):
        root = None
        b = fortunes.BinaryTree(root=root)

        self.assertAlmostEqual(b.root, root)

    def test_konstruktorille_lehti(self):
        root = self.leaf
        b = fortunes.BinaryTree(root=root)

        self.assertAlmostEqual(b.root, root)

    def test_konstruktorille_bark(self):
        root = self.bark
        b = fortunes.BinaryTree(root=root)

        self.assertAlmostEqual(b.root, root)

    def test_konstruktorille_epapateva_root(self):
        root = 10

        with self.assertRaises(TypeError):
            b = fortunes.BinaryTree(root=root)

    def test_aseta_uusi_lehti(self):
        root = None
        b = fortunes.BinaryTree(root=root)

        root = self.leaf
        b.root = root

        self.assertAlmostEqual(b.root, root)

    def test_aseta_uusi_none(self):
        root = None
        b = fortunes.BinaryTree(root=root)

        root = None

        with self.assertRaises(TypeError):
            b.root = root

    def test_etsi_arc_root_on_none(self):
        root = None
        b = fortunes.BinaryTree(root=root)

        self.assertAlmostEqual(b.find_arc(10), (None, None))

    def test_etsi_arc_root_on_leaf(self):
        root = self.leaf
        b = fortunes.BinaryTree(root=root)

        self.assertAlmostEqual(b.find_arc(10), (self.leaf, None))

    def test_etsi_arc_root_on_bark_leaf_on_vasen(self):
        root = self.bark
        y = 10
        self.bark.left = self.leaf_vasen
        self.bark.right = self.leaf_oikea
        self.bark.ray.y = 15
        b = fortunes.BinaryTree(root=root)

        self.assertAlmostEqual(b.find_arc(y)[0], self.leaf_vasen)
        self.assertAlmostEqual(b.find_arc(y)[1], fortunes.Side.LEFT)

    def test_etsi_arc_root_on_bark_leaf_on_oikea(self):
        root = self.bark
        y = 10
        self.bark.left = self.leaf_vasen
        self.bark.right = self.leaf_oikea
        self.bark.ray.y = 5
        b = fortunes.BinaryTree(root=root)

        self.assertAlmostEqual(b.find_arc(y)[0], self.leaf_oikea)
        self.assertAlmostEqual(b.find_arc(y)[1], fortunes.Side.RIGHT)

    def test_etsi_arc_root_on_bark_leaf_on_oikea_y_on_sama(self):
        root = self.bark
        y = 10
        self.bark.left = self.leaf_vasen
        self.bark.right = self.leaf_oikea
        self.bark.ray.y = y
        b = fortunes.BinaryTree(root=root)

        self.assertAlmostEqual(b.find_arc(y)[0], self.leaf_oikea)
        self.assertAlmostEqual(b.find_arc(y)[1], fortunes.Side.RIGHT)

    def test_etsi_arc_root_on_kaksi_tasoa_bark_sitten_leaf(self):
        root = self.bark
        y = 10
        self.bark.left = self.leaf_vasen
        self.bark.right = self.bark_oikea
        self.bark.ray.y = 5
        self.bark.right.ray.y = 9
        self.bark.right.right = self.leaf_oikea
        b = fortunes.BinaryTree(root=root)

        self.assertAlmostEqual(b.find_arc(y)[0], self.leaf_oikea)
        self.assertAlmostEqual(b.find_arc(y)[1], fortunes.Side.RIGHT)


class TestEvent(TestCase):
    def setUp(self):
        self.event_type = Mock(spec=fortunes.EventType)
        self.point = Mock(spec=fortunes.Point)

    def test_konstruktorille_pateva_piste(self):
        e = fortunes.Event(10, self.event_type, self.point)

        self.assertAlmostEqual(e.point, self.point)

    def test_konstruktorille_pateva_site_event(self):
        event_type = fortunes.EventType.SITE_EVENT

        e = fortunes.Event(10, event_type, self.point)

        self.assertAlmostEqual(e.type, event_type)

    def test_konstruktorille_pateva_circle_event(self):
        event_type = fortunes.EventType.CIRCLE_EVENT

        e = fortunes.Event(10, event_type, self.point)

        self.assertAlmostEqual(e.type, fortunes.EventType.CIRCLE_EVENT)

    def test_konstruktorille_epapateva_piste(self):
        point = 10

        with self.assertRaises(TypeError):
            e = fortunes.Event(10, self.event_type, point)

    def test_konstruktorille_epapateva_event_tyyppi(self):
        event_type = 10

        with self.assertRaises(TypeError):
            e = fortunes.Event(10, event_type, self.point)


class TestFortunesAlgorithm(TestCase):
    def setUp(self):
        "kirjottelen myöhemmin"
