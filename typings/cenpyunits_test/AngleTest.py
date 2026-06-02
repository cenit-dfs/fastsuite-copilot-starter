import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Angle import *

class AngleTest(unittest.TestCase):

    def test_isDefault(self):
        deg = Degree()
        rad = Radian()

        self.assertTrue(deg.IsDefault(), "Degree must be default")
        self.assertFalse(rad.IsDefault(), "Radian must not be default")

    def test_UnitGroup(self):
        deg = Degree()
        rad = Radian()

        self.assertEqual(deg.GetUnitGroup(), UnitGroups.Angle)
        self.assertEqual(rad.GetUnitGroup(), UnitGroups.Angle)

    def test_convert_deg_to_rad(self):
        rad = Converter.ConvertDefaultToUnit(90.0, Radian())
        self.assertEqual(1.570796313445772, rad)

    def test_convert_rad_to_deg(self):
        deg = Converter.ConvertUnitToDefault(1.570796313445772, Radian())
        self.assertEqual(90.0, deg)
      
    def test_convert_deg_to_deg(self):
        deg = Converter.ConvertDefaultToUnit(90.0, Degree())
        self.assertEqual(90.0, deg)

    def test_convert_rad_to_rad(self):
        rad = Converter.ConvertUnitToUnit(1.0, Radian(), Radian())
        self.assertEqual(1.0, rad)  

if __name__ == "__main__":
    unittest.main()
