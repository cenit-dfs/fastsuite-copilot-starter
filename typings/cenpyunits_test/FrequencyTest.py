import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Frequency import *

class FrequencyTest(unittest.TestCase):

    def test_isDefault(self):
        hertz = Hertz()
        mHz= Millihertz()
        kHz = Kilohertz()


        self.assertTrue(hertz.IsDefault(), "Hertz must be default")
        self.assertFalse(mHz.IsDefault(), "Millihertz must not be default")
        self.assertFalse(kHz.IsDefault(), "Kilohertz must not be default")

    def test_UnitGroup(self):
        hertz = Hertz()
        mHz= Millihertz()
        kHz = Kilohertz()

        self.assertEqual(hertz.GetUnitGroup(), UnitGroups.Frequency)
        self.assertEqual(mHz.GetUnitGroup(), UnitGroups.Frequency)
        self.assertEqual(kHz.GetUnitGroup(), UnitGroups.Frequency)

    def test_convert_kHz_to_hertz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilohertz(), Hertz())
        self.assertEqual(1000, unit2)

    def test_convert_kHz_to_mHz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilohertz(), Millihertz())
        self.assertEqual(1000000, unit2)

    def test_converr_hertz_to_kHz(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Hertz(), Kilohertz())
        self.assertEqual(1, unit2)

    def test_convert_mHz_to_kHz(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Millihertz(), Kilohertz())
        self.assertEqual(1, unit2)

    def test_convert_hertz_to_mHz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Hertz(), Millihertz())
        self.assertEqual(1000, unit2)

    def test_convert_mHz_to_hertz(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millihertz(), Hertz())
        self.assertEqual(1, unit2)
      
    def test_convert_hertz_to_hertz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Hertz(), Hertz())
        self.assertEqual(1, unit2)

    def test_convert_mHz_to_mHz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Millihertz(), Millihertz())
        self.assertEqual(1, unit2)

    def test_convert_kHz_to_kHz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilohertz(), Kilohertz())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()
