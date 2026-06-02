import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Power import *

class PowerTest(unittest.TestCase):
 
    def test_isDefault(self):
        ftlbs = Footpoundforcepersecond()
        btus= Britishthermalunitpersecond()
        kw = Kilowatt()
        watt = Watt()

        self.assertFalse(ftlbs.IsDefault(), "Footpoundforcepersecond must not be default")
        self.assertFalse(btus.IsDefault(), "Britishthermalunitpersecond must not be default")
        self.assertFalse(kw.IsDefault(), "Kilowatt must not be default")
        self.assertTrue(watt.IsDefault(), "Watt must be default")

    def test_UnitGroup(self):
        ftlbs = Footpoundforcepersecond()
        btus= Britishthermalunitpersecond()
        kw = Kilowatt()
        watt = Watt()

        self.assertEqual(ftlbs.GetUnitGroup(), UnitGroups.Power)
        self.assertEqual(btus.GetUnitGroup(), UnitGroups.Power)
        self.assertEqual(kw.GetUnitGroup(), UnitGroups.Power)
        self.assertEqual(watt.GetUnitGroup(), UnitGroups.Power)

    def test_convert_kw_to_ftlbs(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilowatt(), Footpoundforcepersecond())
        self.assertEqual(737.5991148810622, unit2)

    def test_convert_kw_to_btus(self):
        unit2 = Converter.ConvertUnitToUnit(10, Kilowatt(), Britishthermalunitpersecond())
        self.assertEqual(9.477999194370067, unit2)

    def test_convert_kw_to_watt(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilowatt(), Watt())
        self.assertEqual(1000, unit2)

    def test_converr_ftlbs_to_kw(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Footpoundforcepersecond(), Kilowatt())
        self.assertEqual(1.35575, unit2)

    def test_convert_btus_to_kw(self):
        unit2 = Converter.ConvertUnitToUnit(1, Britishthermalunitpersecond(), Kilowatt())
        self.assertEqual(1.055075, unit2)

    def test_convert_watt_to_kw(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Watt(), Kilowatt())
        self.assertEqual(1, unit2)

    def test_convert_ftlbs_to_btus(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Footpoundforcepersecond(), Britishthermalunitpersecond())
        self.assertEqual(1.284979740776722, unit2)

    def test_convert_ftlbs_to_watt(self):
        unit2 = Converter.ConvertUnitToUnit(1, Footpoundforcepersecond(), Watt())
        self.assertEqual(1.35575, unit2)

    def test_convert_btus_to_watt(self):
        unit2 = Converter.ConvertUnitToUnit(1, Britishthermalunitpersecond(), Watt())
        self.assertEqual(1055.075, unit2)

    def test_convert_btus_to_ftlbs(self):
        unit2 = Converter.ConvertUnitToUnit(1, Britishthermalunitpersecond(), Footpoundforcepersecond())
        self.assertEqual(778.2223861331366, unit2)
      
    def test_convert_watt_to_btus(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Watt(), Britishthermalunitpersecond())
        self.assertEqual(0.9477999194370068, unit2)

    def test_convert_watt_to_ftlbs(self):
        unit2 = Converter.ConvertUnitToUnit(1, Watt(), Footpoundforcepersecond())
        self.assertEqual(0.7375991148810621, unit2)
      
    def test_convert_ftlbs_to_ftlbs(self):
        unit2 = Converter.ConvertUnitToUnit(1, Footpoundforcepersecond(), Footpoundforcepersecond())
        self.assertEqual(1, unit2)

    def test_convert_btus_to_btus(self):
        unit2 = Converter.ConvertUnitToUnit(1, Britishthermalunitpersecond(), Britishthermalunitpersecond())
        self.assertEqual(1, unit2)
              
    def test_convert_watt_to_watt(self):
        unit2 = Converter.ConvertUnitToUnit(1, Watt(), Watt())
        self.assertEqual(1, unit2)

    def test_convert_kw_to_kw(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilowatt(), Kilowatt())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()

