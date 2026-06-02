import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.ElectricCapacity import *

class ElectricCapacityTest(unittest.TestCase):
    
    def test_isDefault(self):
        f = Farad()
        mf = Millifarad()

        self.assertTrue(f.IsDefault(), "Degree must be default")
        self.assertFalse(mf.IsDefault(), "Radian must not be default")

    def test_UnitGroup(self):
        f = Farad()
        mf = Millifarad()

        self.assertEqual(f.GetUnitGroup(), UnitGroups.ElectricCap)
        self.assertEqual(mf.GetUnitGroup(), UnitGroups.ElectricCap)

    def test_convert_f_to_mf(self):
        unit2 = Converter.ConvertUnitToUnit(1, Farad(), Millifarad())
        self.assertEqual(1000, unit2)

    def test_convert_mf_to_f(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millifarad(), Farad())
        self.assertEqual(1, unit2)
      
    def test_convert_f_to_f(self):
        unit2 = Converter.ConvertUnitToUnit(1, Farad(), Farad())
        self.assertEqual(1, unit2)

    def test_convert_mf_to_mf(self):
        unit2 = Converter.ConvertUnitToUnit(1, Millifarad(), Millifarad())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()
