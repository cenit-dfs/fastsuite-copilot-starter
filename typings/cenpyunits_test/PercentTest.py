import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Percent import *

class PercentTest(unittest.TestCase):
        
    def test_isDefault(self):
        f = Percentage()
        mf = PercentageDecimal()

        self.assertTrue(f.IsDefault(), "Percentage must be default")
        self.assertFalse(mf.IsDefault(), "PercentageDecimal must not be default")

    def test_UnitGroup(self):
        f = Percentage()
        mf = PercentageDecimal()

        self.assertEqual(f.GetUnitGroup(), UnitGroups.Percent)
        self.assertEqual(mf.GetUnitGroup(), UnitGroups.Percent)

    def test_convert_ohm_to_mohm(self):
        unit2 = Converter.ConvertUnitToUnit(100, Percentage(), PercentageDecimal())
        self.assertEqual(1, unit2)

    def test_convert_mohm_to_ohm(self):
        unit2 = Converter.ConvertUnitToUnit(1, PercentageDecimal(), Percentage())
        self.assertEqual(100, unit2)
      
    def test_convert_ohm_to_ohm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Percentage(), Percentage())
        self.assertEqual(1, unit2)

    def test_convert_mohm_to_mohm(self):
        unit2 = Converter.ConvertUnitToUnit(1, PercentageDecimal(), PercentageDecimal())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()
