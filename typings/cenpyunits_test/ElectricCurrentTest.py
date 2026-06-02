import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.ElectricCurrent import *

class ElectricCurrentTest(unittest.TestCase):
        
    def test_isDefault(self):
        f = Ampere()
        mf = Milliampere()

        self.assertTrue(f.IsDefault(), "Degree must be default")
        self.assertFalse(mf.IsDefault(), "Radian must not be default")

    def test_UnitGroup(self):
        f = Ampere()
        mf = Milliampere()

        self.assertEqual(f.GetUnitGroup(), UnitGroups.ElectricCurrent)
        self.assertEqual(mf.GetUnitGroup(), UnitGroups.ElectricCurrent)

    def test_convert_a_to_ma(self):
        unit2 = Converter.ConvertUnitToUnit(1, Ampere(), Milliampere())
        self.assertEqual(1000, unit2)

    def test_convert_ma_to_a(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Milliampere(), Ampere())
        self.assertEqual(1, unit2)
      
    def test_convert_a_to_a(self):
        unit2 = Converter.ConvertUnitToUnit(1, Ampere(), Ampere())
        self.assertEqual(1, unit2)

    def test_convert_ma_to_ma(self):
        unit2 = Converter.ConvertUnitToUnit(1, Milliampere(), Milliampere())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()
