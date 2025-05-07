from unittest import TestCase
from unittest.mock import Mock

from mapgenerator.algorithms.fortunes import binarytree, base_structs

class TestBinaryTreeLeaf(TestCase):
    def setUp(self):
        self.arc = Mock(spec=base_structs.Arc)

    def test_konstruktorille_pateva_arc(self):
        l = binarytree.BinaryTreeLeaf(self.arc)
        self.assertAlmostEqual(l.arc, self.arc)

    def test_konstruktorille_epapateva_arc(self):
        arc = 10

        with self.assertRaises(TypeError):
            l = binarytree.BinaryTreeLeaf(arc)


class TestBinaryTreeBark(TestCase):
    def setUp(self):
        self.ray = Mock(spec=base_structs.Ray)
        self.left_bark = Mock(spec=binarytree.BinaryTreeBark)
        self.right_bark = Mock(spec=binarytree.BinaryTreeBark)
        self.left_leaf = Mock(spec=binarytree.BinaryTreeLeaf)
        self.right_leaf = Mock(spec=binarytree.BinaryTreeLeaf)

    def test_konstruktorille_pateva_ray(self):
        b = binarytree.BinaryTreeBark(self.ray, self.left_bark, self.right_bark)

        self.assertAlmostEqual(b.ray, self.ray)

    def test_konstruktorille_pateva_vasen_bark(self):
        b = binarytree.BinaryTreeBark(self.ray, self.left_bark, self.right_bark)

        self.assertAlmostEqual(b.left, self.left_bark)

    def test_konstruktorille_pateva_oikea_bark(self):
        b = binarytree.BinaryTreeBark(self.ray, self.left_bark, self.right_bark)

        self.assertAlmostEqual(b.right, self.right_bark)

    def test_konstruktorille_pateva_vasen_leaf(self):
        b = binarytree.BinaryTreeBark(self.ray, self.left_leaf, self.right_bark)

        self.assertAlmostEqual(b.left, self.left_leaf)

    def test_konstruktorille_pateva_oikea_leaf(self):
        b = binarytree.BinaryTreeBark(self.ray, self.left_bark, self.right_leaf)

        self.assertAlmostEqual(b.right, self.right_leaf)

    def test_konstruktorille_epapateva_ray(self):
        ray = 10

        with self.assertRaises(TypeError):
            b = binarytree.BinaryTreeBark(ray, self.left_bark, self.right_bark)

    def test_konstruktorille_epapateva_lapsi(self):
        left_bark = 10

        with self.assertRaises(TypeError):
            b = binarytree.BinaryTreeBark(self.ray, left_bark, self.right_bark)

    def test_lisaa_pateva_vasen_lapsi(self):
        b = binarytree.BinaryTreeBark(self.ray, self.left_bark, self.right_bark)

        b.left = self.left_leaf

        self.assertAlmostEqual(b.left, self.left_leaf)

    def test_lisaa_pateva_oikea_lapsi(self):
        b = binarytree.BinaryTreeBark(self.ray, self.left_bark, self.right_bark)

        b.right = self.right_leaf

        self.assertAlmostEqual(b.right, self.right_leaf)

    def test_lisaa_epapateva_vasen_lapsi(self):
        b = binarytree.BinaryTreeBark(self.ray, self.left_bark, self.right_bark)

        with self.assertRaises(TypeError):
            b.left = 10

    def test_lisaa_epapateva_oikea_lapsi(self):
        b = binarytree.BinaryTreeBark(self.ray, self.left_bark, self.right_bark)

        with self.assertRaises(TypeError):
            b.right = 10


class TestBinaryTree(TestCase):
    def setUp(self):
        self.bark = Mock(spec=binarytree.BinaryTreeBark)
        self.leaf = Mock(spec=binarytree.BinaryTreeLeaf)

        self.bark_oikea = Mock(spec=binarytree.BinaryTreeBark)
        self.leaf_vasen = Mock(spec=binarytree.BinaryTreeLeaf)
        self.leaf_oikea = Mock(spec=binarytree.BinaryTreeLeaf)

    def test_konstruktorille_none(self):
        root = None
        b = binarytree.BinaryTree(root=root)

        self.assertAlmostEqual(b.root, root)

    def test_konstruktorille_lehti(self):
        root = self.leaf
        b = binarytree.BinaryTree(root=root)

        self.assertAlmostEqual(b.root, root)

    def test_konstruktorille_bark(self):
        root = self.bark
        b = binarytree.BinaryTree(root=root)

        self.assertAlmostEqual(b.root, root)

    def test_konstruktorille_epapateva_root(self):
        root = 10

        with self.assertRaises(TypeError):
            b = binarytree.BinaryTree(root=root)

    def test_aseta_uusi_lehti(self):
        root = None
        b = binarytree.BinaryTree(root=root)

        root = self.leaf
        b.root = root

        self.assertAlmostEqual(b.root, root)

    def test_aseta_uusi_none(self):
        root = None
        b = binarytree.BinaryTree(root=root)

        root = None

        with self.assertRaises(TypeError):
            b.root = root

    def test_etsi_arc_root_on_none(self):
        root = None
        b = binarytree.BinaryTree(root=root)

        self.assertAlmostEqual(b.find_arc(10), (None, None))

    def test_etsi_arc_root_on_leaf(self):
        root = self.leaf
        b = binarytree.BinaryTree(root=root)

        self.assertAlmostEqual(b.find_arc(10), (self.leaf, None))

    def test_etsi_arc_root_on_bark_leaf_on_vasen(self):
        root = self.bark
        y = 10
        self.bark.left = self.leaf_vasen
        self.bark.right = self.leaf_oikea
        self.bark.ray.start.y = 15
        b = binarytree.BinaryTree(root=root)

        self.assertAlmostEqual(b.find_arc(y)[0], self.leaf_vasen)
        self.assertAlmostEqual(b.find_arc(y)[1], binarytree.Side.LEFT)

    def test_etsi_arc_root_on_bark_leaf_on_oikea(self):
        root = self.bark
        y = 10
        self.bark.left = self.leaf_vasen
        self.bark.right = self.leaf_oikea
        self.bark.ray.start.y = 5
        b = binarytree.BinaryTree(root=root)

        self.assertAlmostEqual(b.find_arc(y)[0], self.leaf_oikea)
        self.assertAlmostEqual(b.find_arc(y)[1], binarytree.Side.RIGHT)

    def test_etsi_arc_root_on_bark_leaf_on_oikea_y_on_sama(self):
        root = self.bark
        y = 10
        self.bark.left = self.leaf_vasen
        self.bark.right = self.leaf_oikea
        self.bark.ray.start.y = y
        b = binarytree.BinaryTree(root=root)

        self.assertAlmostEqual(b.find_arc(y)[0], self.leaf_oikea)
        self.assertAlmostEqual(b.find_arc(y)[1], binarytree.Side.RIGHT)

    def test_etsi_arc_root_on_kaksi_tasoa_bark_sitten_leaf(self):
        root = self.bark
        y = 10
        self.bark.left = self.leaf_vasen
        self.bark.right = self.bark_oikea
        self.bark.ray.start.y = 5
        self.bark.right.ray.start.y = 9
        self.bark.right.right = self.leaf_oikea
        b = binarytree.BinaryTree(root=root)

        self.assertAlmostEqual(b.find_arc(y)[0], self.leaf_oikea)
        self.assertAlmostEqual(b.find_arc(y)[1], binarytree.Side.RIGHT)
