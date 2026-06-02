import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Force import *

class ForceTest(unittest.TestCase):

    def test_isDefault(self):
        lbf = Poundforce()
        lbl= Poundal()
        mn = Millinewton()
        newton = Newton()

        self.assertFalse(lbf.IsDefault(), "Poundforce must not be default")
        self.assertFalse(lbl.IsDefault(), "Poundal must not be default")
        self.assertFalse(mn.IsDefault(), "Millinewton must not be default")
        self.assertTrue(newton.IsDefault(), "Newton must be default")

    def test_UnitGroup(self):
        lbf = Poundforce()
        lbl= Poundal()
        mn = Millinewton()
        newton = Newton()

        self.assertEqual(lbf.GetUnitGroup(), UnitGroups.Force)
        self.assertEqual(lbl.GetUnitGroup(), UnitGroups.Force)
        self.assertEqual(mn.GetUnitGroup(), UnitGroups.Force)
        self.assertEqual(newton.GetUnitGroup(), UnitGroups.Force)

    def test_convert_mn_to_lbf(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millinewton(), Poundforce())
        self.assertEqual(0.224799928064023, unit2)

    def test_convert_mn_to_lbl(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millinewton(), Poundal())
        self.assertEqual(7.233011464323171, unit2)

    def test_convert_mn_to_newton(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millinewton(), Newton())
        self.assertEqual(1, unit2)

    def test_converr_lbf_to_mn(self):
        unit2 = Converter.ConvertUnitToUnit(0.224799928064023, Poundforce(), Millinewton())
        self.assertEqual(1000, unit2)

    def test_convert_lbl_to_mn(self):
        unit2 = Converter.ConvertUnitToUnit(7.233011464323171, Poundal(), Millinewton())
        self.assertEqual(1000, unit2)

    def test_convert_newton_to_mn(self):
        unit2 = Converter.ConvertUnitToUnit(1, Newton(), Millinewton())
        self.assertEqual(1000, unit2)

    def test_convert_lbf_to_lbl(self):
        unit2 = Converter.ConvertUnitToUnit(31.0797140544915, Poundforce(), Poundal())
        self.assertEqual(1000, unit2)

    def test_convert_lbf_to_newton(self):
        unit2 = Converter.ConvertUnitToUnit(0.224799928064023, Poundforce(), Newton())
        self.assertEqual(1, unit2)

    def test_convert_lbl_to_newton(self):
        unit2 = Converter.ConvertUnitToUnit(7.233011464323171, Poundal(), Newton())
        self.assertEqual(1, unit2)

    def test_convert_lbl_to_lbf(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Poundal(), Poundforce())
        self.assertEqual(31.0797140544915, unit2)
      
    def test_convert_newton_to_lbl(self):
        unit2 = Converter.ConvertUnitToUnit(1, Newton(), Poundal())
        self.assertEqual(7.233011464323171, unit2)

    def test_convert_newton_to_lbf(self):
        unit2 = Converter.ConvertUnitToUnit(1, Newton(), Poundforce())
        self.assertEqual(0.224799928064023, unit2)
      
    def test_convert_lbf_to_lbf(self):
        unit2 = Converter.ConvertUnitToUnit(1, Poundforce(), Poundforce())
        self.assertEqual(1, unit2)

    def test_convert_lbl_to_lbl(self):
        unit2 = Converter.ConvertUnitToUnit(1, Poundal(), Poundal())
        self.assertEqual(1, unit2)
              
    def test_convert_newton_to_newton(self):
        unit2 = Converter.ConvertUnitToUnit(1, Newton(), Newton())
        self.assertEqual(1, unit2)

    def test_convert_mn_to_mn(self):
        unit2 = Converter.ConvertUnitToUnit(1, Millinewton(), Millinewton())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()