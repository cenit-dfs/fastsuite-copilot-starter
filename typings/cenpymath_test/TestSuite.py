import unittest
import sys, os, inspect
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from cenpymath_test.Euler.ConverterTest import Test_Converter
from cenpymath_test.Geo.MatrixTest import Test_Matrix
from cenpymath_test.Geo.Point3DTest import Test_Point3D



def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    test_suite.addTests(test_loader.loadTestsFromTestCase(Test_Converter))
    test_suite.addTests(test_loader.loadTestsFromTestCase(Test_Matrix))
    test_suite.addTests(test_loader.loadTestsFromTestCase(Test_Point3D))
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())