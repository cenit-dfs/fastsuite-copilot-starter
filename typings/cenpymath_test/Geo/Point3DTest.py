import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

from cenpymath import *

class Test_Point3D(unittest.TestCase):

    def test_constructor_no_input(self):
        testPoint = Point3D.Point3D()
        self.assertIsNotNone(testPoint, "Point constructor failed")

    def test_constructor_tuple_input(self):
        testPoint = Point3D.Point3D((1.0, 2.0, 3.0))
        self.assertIsNotNone(testPoint, "Point constructor failed")
        
    def test_constructor_no_input_zero_point(self):
        testPoint = Point3D.Point3D()
        self.assertIsNotNone(testPoint, "Point constructor failed")

        self.assertTupleEqual(testPoint.GetXYZ(), (0.0, 0.0, 0.0), "Point is at wrong position")

    def test_constructor_tuple_input_correct(self):
        testPoint = Point3D.Point3D((1.0, 2.0, 3.0))
        self.assertIsNotNone(testPoint, "Point constructor failed")

        self.assertTupleEqual(testPoint.GetXYZ(), (1.0, 2.0, 3.0), "Point is at wrong position")

    def test_get_x(self):
        testPoint = Point3D.Point3D((1.0, 2.0, 3.0))
        self.assertIsNotNone(testPoint, "Point constructor failed")

        self.assertEqual(testPoint.GetX(), 1.0, "Point.GetX() is wrong")

    def test_get_y(self):
        testPoint = Point3D.Point3D((1.0, 2.0, 3.0))
        self.assertIsNotNone(testPoint, "Point constructor failed")

        self.assertEqual(testPoint.GetY(), 2.0, "Point.GetY() is wrong")
        
    def test_get_z(self):
        testPoint = Point3D.Point3D((1.0, 2.0, 3.0))
        self.assertIsNotNone(testPoint, "Point constructor failed")

        self.assertEqual(testPoint.GetZ(), 3.0, "Point.GetX() is wrong")

    def test_set_xyz(self):
        testPoint = Point3D.Point3D((1.0, 2.0, 3.0))
        position = (7.0, 8.0, 9.0)
        testPoint.SetXYZ(position)

        self.assertTupleEqual(testPoint.GetXYZ(), position, "Point SetXYZ() failed")

    def test_set_xyz_fail_wrong_type_input(self):
        testPoint = Point3D.Point3D((1.0, 2.0, 3.0))
        position = "(7.0, 8.0, 9.0)"
        self.assertRaises(TypeError, testPoint.SetXYZ, position)

    def test_set_xyz_fail_wrong_type_in_tuple1(self):
        testPoint = Point3D.Point3D((1.0, 2.0, 3.0))
        position = ("7.0", 8.0, 9.0)
        self.assertRaises(TypeError, testPoint.SetXYZ, position)

    def test_set_xyz_fail_wrong_type_in_tuple2(self):
        testPoint = Point3D.Point3D((1.0, 2.0, 3.0))
        position = (7.0, "8.0", 9.0)
        self.assertRaises(TypeError, testPoint.SetXYZ, position)


    def test_set_xyz_fail_wrong_type_in_tuple3(self):
        testPoint = Point3D.Point3D((1.0, 2.0, 3.0))
        position = (7.0, 8.0, "9.0")
        self.assertRaises(TypeError, testPoint.SetXYZ, position)

    def test_set_xyz_fail_wrong_type_in_tuple4(self):
        testPoint = Point3D.Point3D((1.0, 2.0, 3.0))
        position = (7, 8.0, 9.0)
        self.assertRaises(TypeError, testPoint.SetXYZ, position)

    def test_set_xyz_fail_too_few(self):
        testPoint = Point3D.Point3D((1.0, 2.0, 3.0))
        position = (8.0, 9.0)
        self.assertRaises(IndexError, testPoint.SetXYZ, position)

    def test_set_xyz_fail_too_many(self):
        testPoint = Point3D.Point3D((1.0, 2.0, 3.0))
        position = (6.0, 7.0, 8.0, 9.0)
        self.assertRaises(IndexError, testPoint.SetXYZ, position)


if __name__ == "__main__":
    unittest.main()