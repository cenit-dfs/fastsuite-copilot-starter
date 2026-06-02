import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Length import Meter
from cenpyunits.Time import Second

class ConverterTest(unittest.TestCase):

    def test_ConvertDefaultToUnit_wrong_input(self):
        meter = Meter()
        self.assertRaises(ValueError, Converter.ConvertDefaultToUnit, 0.0, None)
        self.assertRaises(ValueError, Converter.ConvertDefaultToUnit, None, None)
        self.assertRaises(ValueError, Converter.ConvertDefaultToUnit, None, meter)
                
    def test_ConvertUnitToDefault_wrong_input(self):
        meter = Meter()
        self.assertRaises(ValueError, Converter.ConvertUnitToDefault, 0.0, None)
        self.assertRaises(ValueError, Converter.ConvertUnitToDefault, None, None)
        self.assertRaises(ValueError, Converter.ConvertUnitToDefault, None, meter)
                
    def test_ConvertUnitToUnit_wrong_target(self):
        meter = Meter()
        second = Second()
        self.assertRaises(ValueError, Converter.ConvertUnitToUnit, 0.0, meter, None)
        self.assertRaises(ValueError, Converter.ConvertUnitToUnit, None, None, None)
        self.assertRaises(ValueError, Converter.ConvertUnitToUnit, None, meter, meter)
        self.assertRaises(TypeError, Converter.ConvertUnitToUnit, 0.0, meter, second)

if __name__ == "__main__":
    unittest.main()