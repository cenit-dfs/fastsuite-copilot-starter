import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.AngularAcceleration import *

class AngularAccelerationTest(unittest.TestCase):

    def test_isDefault(self):
        degsecsec = DegreeSecondSecond()
        radsecsec= RadianSecondSecond()

        self.assertFalse(degsecsec.IsDefault(), "DegreeSecondSecond must not be default")
        self.assertTrue(radsecsec.IsDefault(), "RadianSecondSecond must be default")

    def test_UnitGroup(self):
        degsecsec = DegreeSecondSecond()
        radsecsec = RadianSecondSecond()

        self.assertEqual(degsecsec.GetUnitGroup(), UnitGroups.AngularAcceleration)
        self.assertEqual(radsecsec.GetUnitGroup(), UnitGroups.AngularAcceleration)

    def test_convert_rad_to_deg(self):
        radsecsec = Converter.ConvertDefaultToUnit(1, DegreeSecondSecond())
        self.assertEqual(57.29578778556937, radsecsec)

    def test_convert_deg_to_rad(self):
        degsecsec = Converter.ConvertUnitToDefault(57.29578778556937, DegreeSecondSecond())
        self.assertEqual(1, degsecsec)
      
    def test_convert_rad_to_rad(self):
        degsecsec = Converter.ConvertDefaultToUnit(1.0, RadianSecondSecond())
        self.assertEqual(1.0, degsecsec)

    def test_convert_deg_to_deg(self):
        radsecsec = Converter.ConvertUnitToUnit(1.0, DegreeSecondSecond(), DegreeSecondSecond())
        self.assertEqual(1.0, radsecsec)  

if __name__ == "__main__":
    unittest.main()
