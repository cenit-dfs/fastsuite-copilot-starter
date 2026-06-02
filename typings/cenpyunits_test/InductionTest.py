import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Induction import *

class InductionTest(unittest.TestCase):

    def test_isDefault(self):
        henry = Henry()
        kh= Millihenry()
        wpa = Weberperampere()


        self.assertTrue(henry.IsDefault(), "Henry must be default")
        self.assertFalse(kh.IsDefault(), "Millihenry must not be default")
        self.assertFalse(wpa.IsDefault(), "Weberperampere must not be default")

    def test_UnitGroup(self):
        henry = Henry()
        kh= Millihenry()
        wpa = Weberperampere()

        self.assertEqual(henry.GetUnitGroup(), UnitGroups.Induction)
        self.assertEqual(kh.GetUnitGroup(), UnitGroups.Induction)
        self.assertEqual(wpa.GetUnitGroup(), UnitGroups.Induction)

    def test_convert_wpa_to_henry(self):
        unit2 = Converter.ConvertUnitToUnit(1, Weberperampere(), Henry())
        self.assertEqual(1, unit2)

    def test_convert_wpa_to_kh(self):
        unit2 = Converter.ConvertUnitToUnit(1, Weberperampere(), Millihenry())
        self.assertEqual(1000, unit2)

    def test_converr_henry_to_wpa(self):
        unit2 = Converter.ConvertUnitToUnit(1, Henry(), Weberperampere())
        self.assertEqual(1, unit2)

    def test_convert_kh_to_wpa(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millihenry(), Weberperampere())
        self.assertEqual(1, unit2)

    def test_convert_henry_to_kh(self):
        unit2 = Converter.ConvertUnitToUnit(1, Henry(), Millihenry())
        self.assertEqual(1000, unit2)

    def test_convert_kh_to_henry(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millihenry(), Henry())
        self.assertEqual(1, unit2)
      
    def test_convert_henry_to_henry(self):
        unit2 = Converter.ConvertUnitToUnit(1, Henry(), Henry())
        self.assertEqual(1, unit2)

    def test_convert_kh_to_kh(self):
        unit2 = Converter.ConvertUnitToUnit(1, Millihenry(), Millihenry())
        self.assertEqual(1, unit2)

    def test_convert_wpa_to_wpa(self):
        unit2 = Converter.ConvertUnitToUnit(1, Weberperampere(), Weberperampere())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()
