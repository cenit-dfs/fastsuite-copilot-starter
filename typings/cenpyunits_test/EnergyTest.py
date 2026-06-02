import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Energy import *

class EnergyTest(unittest.TestCase):

    def test_isDefault(self):
        btu = Britishthermalunit()
        fp= Footpound()
        kj = Kilojoule()
        j = Joule()

        self.assertFalse(btu.IsDefault(), "Britishthermalunit must not be default")
        self.assertFalse(fp.IsDefault(), "Footpound must not be default")
        self.assertFalse(kj.IsDefault(), "Kilojoule must not be default")
        self.assertTrue(j.IsDefault(), "Joule must be default")

    def test_UnitGroup(self):
        btu = Britishthermalunit()
        fp= Footpound()
        kj = Kilojoule()
        j = Joule()

        self.assertEqual(btu.GetUnitGroup(), UnitGroups.Energy)
        self.assertEqual(fp.GetUnitGroup(), UnitGroups.Energy)
        self.assertEqual(kj.GetUnitGroup(), UnitGroups.Energy)
        self.assertEqual(j.GetUnitGroup(), UnitGroups.Energy)

    def test_convert_kj_to_btu(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilojoule(), Britishthermalunit())
        self.assertEqual(0.9477999194370068, unit2)

    def test_convert_kj_to_fp(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilojoule(), Footpound())
        self.assertEqual(737.5991148810622, unit2)

    def test_convert_kj_to_j(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilojoule(), Joule())
        self.assertEqual(1000, unit2)

    def test_converr_btu_to_kj(self):
        unit2 = Converter.ConvertUnitToUnit(1, Britishthermalunit(), Kilojoule())
        self.assertEqual(1.055075, unit2)

    def test_convert_fp_to_kj(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Footpound(), Kilojoule())
        self.assertEqual(1.35575, unit2)

    def test_convert_j_to_kj(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Joule(), Kilojoule())
        self.assertEqual(1, unit2)

    def test_convert_btu_to_fp(self):
        unit2 = Converter.ConvertUnitToUnit(1, Britishthermalunit(), Footpound())
        self.assertEqual(778.2223861331366, unit2)

    def test_convert_btu_to_j(self):
        unit2 = Converter.ConvertUnitToUnit(1, Britishthermalunit(), Joule())
        self.assertEqual(1055.075, unit2)

    def test_convert_fp_to_j(self):
        unit2 = Converter.ConvertUnitToUnit(0.7375991148810621, Footpound(), Joule())
        self.assertEqual(1, unit2)

    def test_convert_fp_to_btu(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Footpound(), Britishthermalunit())
        self.assertEqual(1.284979740776722, unit2)
      
    def test_convert_j_to_fp(self):
        unit2 = Converter.ConvertUnitToUnit(1, Joule(), Footpound())
        self.assertEqual(0.7375991148810621, unit2)

    def test_convert_j_to_btu(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Joule(), Britishthermalunit())
        self.assertEqual(0.9477999194370068, unit2)
      
    def test_convert_btu_to_btu(self):
        unit2 = Converter.ConvertUnitToUnit(1, Britishthermalunit(), Britishthermalunit())
        self.assertEqual(1, unit2)

    def test_convert_fp_to_fp(self):
        unit2 = Converter.ConvertUnitToUnit(1, Footpound(), Footpound())
        self.assertEqual(1, unit2)
              
    def test_convert_j_to_j(self):
        unit2 = Converter.ConvertUnitToUnit(1, Joule(), Joule())
        self.assertEqual(1, unit2)

    def test_convert_kj_to_kj(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilojoule(), Kilojoule())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()
