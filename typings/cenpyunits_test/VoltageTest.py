import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Voltage import *

class VoltageTest(unittest.TestCase):

    def test_isDefault(self):
        volt = Volt()
        mv= Millivolt()
        kv = Kilovolt()


        self.assertTrue(volt.IsDefault(), "Volt must be default")
        self.assertFalse(mv.IsDefault(), "Millivolt must not be default")
        self.assertFalse(kv.IsDefault(), "Kilovolt must not be default")

    def test_UnitGroup(self):
        volt = Volt()
        mv= Millivolt()
        kv = Kilovolt()

        self.assertEqual(volt.GetUnitGroup(), UnitGroups.Voltage)
        self.assertEqual(mv.GetUnitGroup(), UnitGroups.Voltage)
        self.assertEqual(kv.GetUnitGroup(), UnitGroups.Voltage)

    def test_convert_kv_to_volt(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilovolt(), Volt())
        self.assertEqual(1000, unit2)

    def test_convert_kv_to_mv(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Kilovolt(), Millivolt())
        self.assertEqual(1000, unit2)

    def test_converr_volt_to_kv(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Volt(), Kilovolt())
        self.assertEqual(1, unit2)

    def test_convert_mv_to_kv(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millivolt(), Kilovolt())
        self.assertEqual(0.001, unit2)

    def test_convert_volt_to_mv(self):
        unit2 = Converter.ConvertUnitToUnit(1, Volt(), Millivolt())
        self.assertEqual(1000, unit2)

    def test_convert_mv_to_volt(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millivolt(), Volt())
        self.assertEqual(1, unit2)
      
    def test_convert_volt_to_volt(self):
        unit2 = Converter.ConvertUnitToUnit(1, Volt(), Volt())
        self.assertEqual(1, unit2)

    def test_convert_mv_to_mv(self):
        unit2 = Converter.ConvertUnitToUnit(1, Millivolt(), Millivolt())
        self.assertEqual(1, unit2)

    def test_convert_kv_to_kv(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilovolt(), Kilovolt())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()

