import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

from cenpymath import *

class Test_Converter(unittest.TestCase):

    def test_constructor(self):
        testConverter = Converter.Converter()
        self.assertIsNotNone(testConverter, "Converter constructor failed")

    def test_getMatrixFromEuler_get_unit(self):
        testConverter = Converter.Converter()
        resultMatrix = testConverter.GetMatrixFromEuler(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        array = resultMatrix.GetArray()
        
        testArray = [ 1.0, 0.0, 0.0, 0.0, \
                      0.0, 1.0, 0.0, 0.0, \
                      0.0, 0.0, 1.0, 0.0, \
                      0.0, 0.0, 0.0, 1.0 ]
        
        self.assertListEqual(array, testArray, "matrix is not unit")

    def test_getMatrixFromEuler_get_position(self):
        testConverter = Converter.Converter()
        resultMatrix = testConverter.GetMatrixFromEuler(0.0, 0.0, 0.0, 1.0, 2.0, 3.0)
        array = resultMatrix.GetArray()
        
        testArray = [ 1.0, 0.0, 0.0, 1.0, \
                      0.0, 1.0, 0.0, 2.0, \
                      0.0, 0.0, 1.0, 3.0, \
                      0.0, 0.0, 0.0, 1.0 ]
        
        self.assertListEqual(array, testArray, "matrix is not unit")
        self.assertTupleEqual(resultMatrix.GetPosition().GetXYZ(), (1.0, 2.0, 3.0), "matrix position is wrong")

    def test_getMatrixFromEuler_get_orientation_rot_x_90(self):
        testConverter = Converter.Converter()
        resultMatrix = testConverter.GetMatrixFromEuler(0.0, 0.0, 90.0, 1.0, 2.0, 3.0)
        
        self.assertTupleEqual(resultMatrix.GetOrientation(), (90.0, 0.0, 0.0), "matrix orientation is wrong")
        self.assertTupleEqual(resultMatrix.GetPosition().GetXYZ(), (1.0, 2.0, 3.0), "matrix position is wrong")

    def test_getMatrixFromEuler_get_orientation_rot_y_90(self):
        testConverter = Converter.Converter()
        resultMatrix = testConverter.GetMatrixFromEuler(0.0, 90.0, 0.0, 1.0, 2.0, 3.0)
        
        self.assertTupleEqual(resultMatrix.GetOrientation(), (0.0, 90.0, 0.0), "matrix orientation is wrong")
        self.assertTupleEqual(resultMatrix.GetPosition().GetXYZ(), (1.0, 2.0, 3.0), "matrix position is wrong")

    def test_getMatrixFromEuler_get_orientation_rot_z_90(self):
        testConverter = Converter.Converter()
        resultMatrix = testConverter.GetMatrixFromEuler(90.0, 0.0, 0.0, 1.0, 2.0, 3.0)
        
        self.assertTupleEqual(resultMatrix.GetOrientation(), (0.0, 0.0, 90.0), "matrix orientation is wrong")
        self.assertTupleEqual(resultMatrix.GetPosition().GetXYZ(), (1.0, 2.0, 3.0), "matrix position is wrong")

    def test_getMatrixFromEuler_get_orientation_rot_z_80_rot_y_70(self):
        testConverter = Converter.Converter()
        resultMatrix = testConverter.GetMatrixFromEuler(80.0, 70.0, 0.0, 1.0, 2.0, 3.0)
        
        self.assertTupleEqual(resultMatrix.GetOrientation(), (0.0, 70.0, 80.0), "matrix orientation is wrong")
        self.assertTupleEqual(resultMatrix.GetPosition().GetXYZ(), (1.0, 2.0, 3.0), "matrix position is wrong")

    def test_getMatrixFromEuler_get_orientation_rot_z_80_rot_y_70_rot_x_60(self):
        testConverter = Converter.Converter()
        resultMatrix = testConverter.GetMatrixFromEuler(80.0, 70.0, 60.0, 1.0, 2.0, 3.0)
        
        self.assertTupleEqual(resultMatrix.GetOrientation(), (60.0, 70.0, 80.0), "matrix orientation is wrong")
        self.assertTupleEqual(resultMatrix.GetPosition().GetXYZ(), (1.0, 2.0, 3.0), "matrix position is wrong")

    def test_getMatrixFromEuler_get_orientation_rot_z_90_rot_y_90_rot_x_90(self):
        testConverter = Converter.Converter()
        resultMatrix = testConverter.GetMatrixFromEuler(90.0, 90.0, 90.0, 0.0, 0.0, 0.0)
        
        self.assertTupleEqual(resultMatrix.GetOrientation(), (0.0, 90.0, 0.0), "matrix orientation is wrong")
        self.assertTupleEqual(resultMatrix.GetPosition().GetXYZ(), (0.0, 0.0, 0.0), "matrix position is wrong")

    def test_convertEulerToMatrix_rot_x_90(self):
        testConverter = Converter.Converter()
        resultMatrix = testConverter.ConvertEulerToMatrix(90.0, 00.0, 0.0, Notations.Notations.Euler_XYZs)
        self.assertTupleEqual(resultMatrix.GetOrientation(), (90.0, 0.0, 0.0), "matrix orientation is wrong")

    def test_convertEulerToMatrix_rot_y_90(self):
        testConverter = Converter.Converter()
        resultMatrix = testConverter.ConvertEulerToMatrix(0.0, 90.0, 0.0, Notations.Notations.Euler_XYZs)
        self.assertTupleEqual(resultMatrix.GetOrientation(), (0.0, 90.0, 0.0), "matrix orientation is wrong")

    def test_convertEulerToMatrix_rot_z_90(self):
        testConverter = Converter.Converter()
        resultMatrix = testConverter.ConvertEulerToMatrix(0.0, 0.0, 90.0, Notations.Notations.Euler_XYZs)
        self.assertTupleEqual(resultMatrix.GetOrientation(), (0.0, 0.0, 90.0), "matrix orientation is wrong")


if __name__ == "__main__":
    unittest.main()