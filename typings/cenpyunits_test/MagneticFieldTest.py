import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.MagneticField import *

class MagneticFieldTest(unittest.TestCase):

    def test_isDefault(self):
        tesla = Tesla()
        wmm2= Weberpersquaremillimeter()
        win2 = Weberpersquareinch()


        self.assertTrue(tesla.IsDefault(), "Tesla must be default")
        self.assertFalse(wmm2.IsDefault(), "Weberpersquaremillimeter must not be default")
        self.assertFalse(win2.IsDefault(), "Weberpersquareinch must not be default")

    def test_UnitGroup(self):
        tesla = Tesla()
        wmm2= Weberpersquaremillimeter()
        win2 = Weberpersquareinch()

        self.assertEqual(tesla.GetUnitGroup(), UnitGroups.MagneticField)
        self.assertEqual(wmm2.GetUnitGroup(), UnitGroups.MagneticField)
        self.assertEqual(win2.GetUnitGroup(), UnitGroups.MagneticField)

    def test_convert_win2_to_tesla(self):
        unit2 = Converter.ConvertUnitToUnit(1, Weberpersquareinch(), Tesla())
        self.assertEqual(1550.003, unit2)

    def test_convert_win2_to_wmm2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Weberpersquareinch(), Weberpersquaremillimeter())
        self.assertEqual(0.01550003, unit2)

    def test_converr_tesla_to_win2(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Tesla(), Weberpersquareinch())
        self.assertEqual(0.6451600416257259, unit2)

    def test_convert_wmm2_to_win2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Weberpersquaremillimeter(), Weberpersquareinch())
        self.assertEqual(64.51600416257259, unit2)

    def test_convert_tesla_to_wmm2(self):
        unit2 = Converter.ConvertUnitToUnit(100000, Tesla(), Weberpersquaremillimeter())
        self.assertEqual(1, unit2)

    def test_convert_wmm2_to_tesla(self):
        unit2 = Converter.ConvertUnitToUnit(1, Weberpersquaremillimeter(), Tesla())
        self.assertEqual(100000, unit2)
      
    def test_convert_tesla_to_tesla(self):
        unit2 = Converter.ConvertUnitToUnit(1, Tesla(), Tesla())
        self.assertEqual(1, unit2)

    def test_convert_wmm2_to_wmm2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Weberpersquaremillimeter(), Weberpersquaremillimeter())
        self.assertEqual(1, unit2)

    def test_convert_win2_to_win2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Weberpersquareinch(), Weberpersquareinch())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()

