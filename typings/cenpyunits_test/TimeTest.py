import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Time import *

class TimeTest(unittest.TestCase):

    def test_isDefault(self):
        day = Day()
        hour = Hour()
        min= Minute()
        msec = Millisecond()
        sec = Second()

        self.assertFalse(day.IsDefault(), "Day must not be default")
        self.assertFalse(hour.IsDefault(), "Hour must not be default")
        self.assertFalse(min.IsDefault(), "Minute must not be default")
        self.assertFalse(msec.IsDefault(), "Millisecond must not be default")
        self.assertTrue(sec.IsDefault(), "Second must be default")

    def test_UnitGroup(self):
        day = Day()
        hour = Hour()
        min= Minute()
        msec = Millisecond()
        sec = Second()

        self.assertEqual(day.GetUnitGroup(), UnitGroups.Time)
        self.assertEqual(hour.GetUnitGroup(), UnitGroups.Time)
        self.assertEqual(min.GetUnitGroup(), UnitGroups.Time)
        self.assertEqual(msec.GetUnitGroup(), UnitGroups.Time)
        self.assertEqual(sec.GetUnitGroup(), UnitGroups.Time)

    def test_convert_msec_to_hour(self):
        unit2 = Converter.ConvertUnitToUnit(3600000, Millisecond(), Hour())
        self.assertEqual(1, unit2)

    def test_convert_msec_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(60000, Millisecond(), Minute())
        self.assertEqual(1, unit2)

    def test_convert_msec_to_sec(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millisecond(), Second())
        self.assertEqual(1, unit2)

    def test_converr_hour_to_msec(self):
        unit2 = Converter.ConvertUnitToUnit(1, Hour(), Millisecond())
        self.assertEqual(3600000, unit2)

    def test_convert_min_to_msec(self):
        unit2 = Converter.ConvertUnitToUnit(1, Minute(), Millisecond())
        self.assertEqual(60000, unit2)

    def test_convert_sec_to_msec(self):
        unit2 = Converter.ConvertUnitToUnit(1, Second(), Millisecond())
        self.assertEqual(1000, unit2)

    def test_convert_hour_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(1, Hour(), Minute())
        self.assertEqual(60, unit2)

    def test_convert_hour_to_sec(self):
        unit2 = Converter.ConvertUnitToUnit(1, Hour(), Second())
        self.assertEqual(3600, unit2)

    def test_convert_min_to_sec(self):
        unit2 = Converter.ConvertUnitToUnit(1, Minute(), Second())
        self.assertEqual(60, unit2)

    def test_convert_min_to_hour(self):
        unit2 = Converter.ConvertUnitToUnit(60, Minute(), Hour())
        self.assertEqual(1, unit2)
      
    def test_convert_sec_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(120, Second(), Minute())
        self.assertEqual(2, unit2)

    def test_convert_sec_to_hour(self):
        unit2 = Converter.ConvertUnitToUnit(3600, Second(), Hour())
        self.assertEqual(1, unit2)
      
    def test_convert_hour_to_hour(self):
        unit2 = Converter.ConvertUnitToUnit(1, Hour(), Hour())
        self.assertEqual(1, unit2)

    def test_convert_min_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(1, Minute(), Minute())
        self.assertEqual(1, unit2)
              
    def test_convert_sec_to_sec(self):
        unit2 = Converter.ConvertUnitToUnit(1, Second(), Second())
        self.assertEqual(1, unit2)

    def test_convert_msec_to_msec(self):
        unit2 = Converter.ConvertUnitToUnit(1, Millisecond(), Millisecond())
        self.assertEqual(1, unit2)
        
    def test_convert_msec_to_day(self):
        unit2 = Converter.ConvertUnitToUnit(86400000, Millisecond(), Day())
        self.assertEqual(1, unit2)
        
    def test_convert_sec_to_day(self):
        unit2 = Converter.ConvertUnitToUnit(86400,Second(), Day())
        self.assertEqual(1, unit2)
        
    def test_convert_min_to_day(self):
        unit2 = Converter.ConvertUnitToUnit(1440, Minute(), Day())
        self.assertEqual(1, unit2)
        
    def test_convert_hour_to_day(self):
        unit2 = Converter.ConvertUnitToUnit(24, Hour(), Day())
        self.assertEqual(1, unit2)
        
    def test_convert_day_to_day(self):
        unit2 = Converter.ConvertUnitToUnit(1, Day(), Day())
        self.assertEqual(1, unit2)
        
    def test_convert_day_to_msec(self):
        unit2 = Converter.ConvertUnitToUnit(1, Day(), Millisecond())
        self.assertEqual(86400000.0, unit2)
        
    def test_convert_day_to_sec(self):
        unit2 = Converter.ConvertUnitToUnit(1, Day(), Second())
        self.assertEqual(86400, unit2)
        
    def test_convert_day_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(1, Day(), Minute())
        self.assertEqual(1440, unit2)
        
    def test_convert_day_to_hour(self):
        unit2 = Converter.ConvertUnitToUnit(1, Day(), Hour())
        self.assertEqual(24, unit2)

if __name__ == "__main__":
    unittest.main()