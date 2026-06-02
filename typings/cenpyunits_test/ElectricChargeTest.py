import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.ElectricCharge import *

class ElectricChargeTest(unittest.TestCase):

    def test_isDefault(self):
        kc = Kilocoulomb()
        mc= Millicoulomb()
        sc = Statcoulomb()
        c= Coulomb()

        self.assertFalse(kc.IsDefault(), "Kilocoulomb must not be default")
        self.assertFalse(mc.IsDefault(), "Millicoulomb must not be default")
        self.assertFalse(sc.IsDefault(), "Statcoulomb must not be default")
        self.assertTrue(c.IsDefault(), "Coulomb must be default")

    def test_UnitGroup(self):
        kc = Kilocoulomb()
        mc= Millicoulomb()
        sc = Statcoulomb()
        c= Coulomb()

        self.assertEqual(kc.GetUnitGroup(), UnitGroups.ElectricCharge)
        self.assertEqual(mc.GetUnitGroup(), UnitGroups.ElectricCharge)
        self.assertEqual(sc.GetUnitGroup(), UnitGroups.ElectricCharge)
        self.assertEqual(c.GetUnitGroup(), UnitGroups.ElectricCharge)

    def test_convert_sc_to_kc(self):
        unit2 = Converter.ConvertUnitToUnit(1000000000, Statcoulomb(), Kilocoulomb())
        self.assertEqual(0.00033299999999999996, unit2)

    def test_convert_sc_to_mc(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Statcoulomb(), Millicoulomb())
        self.assertEqual(0.33299999999999996, unit2)

    def test_convert_sc_to_c(self):
        unit2 = Converter.ConvertUnitToUnit(1000000000, Statcoulomb(), Coulomb())
        self.assertEqual(0.33299999999999996, unit2)

    def test_converr_kc_to_sc(self):
        unit2 = Converter.ConvertUnitToUnit(0.000000000001, Kilocoulomb(), Statcoulomb())
        self.assertEqual(3.0030030030030033, unit2)

    def test_convert_mc_to_sc(self):
        unit2 = Converter.ConvertUnitToUnit(0.000001, Millicoulomb(), Statcoulomb())
        self.assertEqual(3.0030030030030033, unit2)

    def test_convert_c_to_sc(self):
        unit2 = Converter.ConvertUnitToUnit(0.000000001, Coulomb(), Statcoulomb())
        self.assertEqual(3.0030030030030033, unit2)

    def test_convert_kc_to_mc(self):
        unit2 = Converter.ConvertUnitToUnit(.001, Kilocoulomb(), Millicoulomb())
        self.assertEqual(1000, unit2)

    def test_convert_kc_to_c(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilocoulomb(), Coulomb())
        self.assertEqual(1000, unit2)

    def test_convert_mc_to_c(self):
        unit2 = Converter.ConvertUnitToUnit(1, Millicoulomb(), Coulomb())
        self.assertEqual(0.001, unit2)

    def test_convert_mc_to_kc(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millicoulomb(), Kilocoulomb())
        self.assertEqual(0.001, unit2)
      
    def test_convert_c_to_mc(self):
        unit2 = Converter.ConvertUnitToUnit(1, Coulomb(), Millicoulomb())
        self.assertEqual(1000, unit2)

    def test_convert_c_to_kc(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Coulomb(), Kilocoulomb())
        self.assertEqual(1, unit2)
      
    def test_convert_kc_to_kc(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilocoulomb(), Kilocoulomb())
        self.assertEqual(1, unit2)

    def test_convert_mc_to_mc(self):
        unit2 = Converter.ConvertUnitToUnit(1, Millicoulomb(), Millicoulomb())
        self.assertEqual(1, unit2)
              
    def test_convert_c_to_c(self):
        unit2 = Converter.ConvertUnitToUnit(1, Coulomb(), Coulomb())
        self.assertEqual(1, unit2)

    def test_convert_sc_to_sc(self):
        unit2 = Converter.ConvertUnitToUnit(1, Statcoulomb(), Statcoulomb())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()