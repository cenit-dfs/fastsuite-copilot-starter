import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.FlowRate import *

class FlowRateTest(unittest.TestCase):

    def test_isDefault(self):
        mm3s = CubicMillimeterSecond()
        cm3min= CubicCentimeterMinute()
        in3min = CubicInchMinute()


        self.assertTrue(mm3s.IsDefault(), "CubicMillimeterSecond must be default")
        self.assertFalse(cm3min.IsDefault(), "CubicCentimeterMinute must not be default")
        self.assertFalse(in3min.IsDefault(), "CubicInchMinute must not be default")

    def test_UnitGroup(self):
        mm3s = CubicMillimeterSecond()
        cm3min= CubicCentimeterMinute()
        in3min = CubicInchMinute()

        self.assertEqual(mm3s.GetUnitGroup(), UnitGroups.FlowRate)
        self.assertEqual(cm3min.GetUnitGroup(), UnitGroups.FlowRate)
        self.assertEqual(in3min.GetUnitGroup(), UnitGroups.FlowRate)

    def test_convert_in3min_to_mm3s(self):
        unit2 = Converter.ConvertUnitToUnit(1, CubicInchMinute(), CubicMillimeterSecond())
        self.assertEqual(273.117733333, unit2)

    def test_convert_in3min_to_cm3min(self):
        unit2 = Converter.ConvertUnitToUnit(1, CubicInchMinute(), CubicCentimeterMinute())
        self.assertEqual(16.387063999652256, unit2)

    def test_converr_mm3s_to_in3min(self):
        unit2 = Converter.ConvertUnitToUnit(1000, CubicMillimeterSecond(), CubicInchMinute())
        self.assertEqual(3.6614246456884056, unit2)

    def test_convert_cm3min_to_in3min(self):
        unit2 = Converter.ConvertUnitToUnit(1000, CubicCentimeterMinute(), CubicInchMinute())
        self.assertEqual(61.023744096027244, unit2)

    def test_convert_mm3s_to_cm3min(self):
        unit2 = Converter.ConvertUnitToUnit(1000, CubicMillimeterSecond(), CubicCentimeterMinute())
        self.assertEqual(59.99999999879999, unit2) # should be 60

    def test_convert_cm3min_to_mm3s(self):
        unit2 = Converter.ConvertUnitToUnit(1, CubicCentimeterMinute(), CubicMillimeterSecond())
        self.assertEqual(16.666666667, unit2)
      
    def test_convert_mm3s_to_mm3s(self):
        unit2 = Converter.ConvertUnitToUnit(1, CubicMillimeterSecond(), CubicMillimeterSecond())
        self.assertEqual(1, unit2)

    def test_convert_cm3min_to_cm3min(self):
        unit2 = Converter.ConvertUnitToUnit(1, CubicCentimeterMinute(), CubicCentimeterMinute())
        self.assertEqual(1, unit2)

    def test_convert_in3min_to_in3min(self):
        unit2 = Converter.ConvertUnitToUnit(1, CubicInchMinute(), CubicInchMinute())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()
