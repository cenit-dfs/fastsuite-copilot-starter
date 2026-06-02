import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

from cenpymath import *

class Test_Matrix(unittest.TestCase):

    def test_construct(self):
        testMatrix = Matrix.Matrix()
        self.assertIsNotNone(testMatrix, "Matrix constructor failed")

    def test_is_unit_after_construct(self):
        testMatrix = Matrix.Matrix()
        array = testMatrix.GetArray()
        
        testArray = [ 1.0, 0.0, 0.0, 0.0, \
                      0.0, 1.0, 0.0, 0.0, \
                      0.0, 0.0, 1.0, 0.0, \
                      0.0, 0.0, 0.0, 1.0 ]
        
        self.assertListEqual(array, testArray, "matrix is not unit")

    def test_no_rotation_on_unit(self):
        testMatrix = Matrix.Matrix()
        orientation = testMatrix.GetOrientation()

        self.assertTupleEqual(orientation, (0.0,0.0,0.0), "default orientation is not 0.0 degree")

    def test_position_is_zero(self):
        testMatrix = Matrix.Matrix()
        position = testMatrix.GetPosition().GetXYZ()

        self.assertTupleEqual(position, (0.0,0.0,0.0), "default position is not 0.0")

    def test_set_position_pass(self):
        testMatrix = Matrix.Matrix()
        testPosition = Point3D.Point3D((1.2, 2.3, 3.4))
        testMatrix.SetPosition(testPosition)

        position = testMatrix.GetPosition()

        self.assertTupleEqual(position.GetXYZ(), testPosition.GetXYZ(), "position was not set correct")

if __name__ == "__main__":
    unittest.main()