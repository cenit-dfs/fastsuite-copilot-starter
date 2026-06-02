import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.ElectricResist import *

class ElectricResistTest(unittest.TestCase):
        
    def test_isDefault(self):
        f = Ohm()
        mf = Milliohm()

        self.assertTrue(f.IsDefault(), "Degree must be default")
        self.assertFalse(mf.IsDefault(), "Radian must not be default")

    def test_UnitGroup(self):
        f = Ohm()
        mf = Milliohm()

        self.assertEqual(f.GetUnitGroup(), UnitGroups.ElectricResist)
        self.assertEqual(mf.GetUnitGroup(), UnitGroups.ElectricResist)

    def test_convert_ohm_to_mohm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Ohm(), Milliohm())
        self.assertEqual(1000, unit2)

    def test_convert_mohm_to_ohm(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Milliohm(), Ohm())
        self.assertEqual(1, unit2)
      
    def test_convert_ohm_to_ohm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Ohm(), Ohm())
        self.assertEqual(1, unit2)

    def test_convert_mohm_to_mohm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Milliohm(), Milliohm())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()
