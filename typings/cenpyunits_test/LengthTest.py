import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Length import *

class LengthTest(unittest.TestCase):

    def test_isDefault(self):
        microm = Micrometer()
        mm = Millimeter()
        meter = Meter()
        cm = Centimeter()
        dm = Decimeter()
        km = Kilometer()
        min = Milliinch()
        inch = Inch()
        ft = Feet()
        yard = Yard()
        mile = Mile()

        self.assertFalse(microm.IsDefault(), "Micrometer must not be default")
        self.assertFalse(mm.IsDefault(), "Millimeter must not be default")
        self.assertTrue(meter.IsDefault(), "Meter must be default")
        self.assertFalse(cm.IsDefault(), "Centimeter must not be default")
        self.assertFalse(dm.IsDefault(), "Decimeter must not be default")
        self.assertFalse(km.IsDefault(), "Kilometer must not be default")
        self.assertFalse(min.IsDefault(), "Milliinch must not be default")
        self.assertFalse(inch.IsDefault(), "Inch must not be default")
        self.assertFalse(ft.IsDefault(), "Feet must not be default")
        self.assertFalse(yard.IsDefault(), "Yard must not be default")
        self.assertFalse(mile.IsDefault(), "Mile must not be default")

    def test_UnitGroup(self):
        microm = Micrometer()
        mm = Millimeter()
        meter = Meter()
        cm = Centimeter()
        dm = Decimeter()
        km = Kilometer()
        min = Milliinch()
        inch = Inch()
        ft = Feet()
        yard = Yard()
        mile = Mile()

        self.assertEqual(microm.GetUnitGroup(), UnitGroups.Length)
        self.assertEqual(mm.GetUnitGroup(), UnitGroups.Length)
        self.assertEqual(meter.GetUnitGroup(), UnitGroups.Length)
        self.assertEqual(cm.GetUnitGroup(), UnitGroups.Length)
        self.assertEqual(dm.GetUnitGroup(), UnitGroups.Length)
        self.assertEqual(km.GetUnitGroup(), UnitGroups.Length)
        self.assertEqual(min.GetUnitGroup(), UnitGroups.Length)
        self.assertEqual(inch.GetUnitGroup(), UnitGroups.Length)
        self.assertEqual(ft.GetUnitGroup(), UnitGroups.Length)
        self.assertEqual(yard.GetUnitGroup(), UnitGroups.Length)
        self.assertEqual(mile.GetUnitGroup(), UnitGroups.Length)

        
    def test_convert_microm_to_microm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Micrometer(), Micrometer())
        self.assertEqual(1, unit2)
        
    def test_convert_microm_to_mm(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Micrometer(), Millimeter())
        self.assertEqual(1, unit2)
        
    def test_convert_microm_to_meter(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Micrometer(), Meter())
        self.assertEqual(0.001, unit2)
        
    def test_convert_microm_to_cm(self):
        unit2 = Converter.ConvertUnitToUnit(10000, Micrometer(), Centimeter())
        self.assertEqual(1, unit2)
        
    def test_convert_microm_to_dm(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Micrometer(), Decimeter())
        self.assertEqual(0.01, unit2)
        
    def test_convert_microm_to_km(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Micrometer(), Kilometer())
        self.assertEqual(.001, unit2)
        
    def test_convert_microm_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(100, Micrometer(), Milliinch())
        self.assertEqual(3.9370078740157477, unit2)
        
    def test_convert_microm_to_inch(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Micrometer(), Inch())
        self.assertEqual(39.37007874015748, unit2)
        
    def test_convert_microm_to_ft(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Micrometer(), Feet())
        self.assertEqual(3.2808400000000035, unit2)
        
    def test_convert_microm_to_yard(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Micrometer(), Yard())
        self.assertEqual(1.0936132983377078, unit2)
        
    def test_convert_microm_to_mile(self):
        unit2 = Converter.ConvertUnitToUnit(1000000000, Micrometer(), Mile())
        self.assertEqual(0.621371192237334, unit2)






    def test_convert_mm_to_microm(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millimeter(), Micrometer())
        self.assertEqual(1000000, unit2)
        
    def test_convert_mm_to_mm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Millimeter(), Millimeter())
        self.assertEqual(1, unit2)
        
    def test_convert_mm_to_meter(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millimeter(), Meter())
        self.assertEqual(1, unit2)
        
    def test_convert_mm_to_cm(self):
        unit2 = Converter.ConvertUnitToUnit(10, Millimeter(), Centimeter())
        self.assertEqual(1, unit2)
        
    def test_convert_mm_to_dm(self):
        unit2 = Converter.ConvertUnitToUnit(100, Millimeter(), Decimeter())
        self.assertEqual(1, unit2)
        
    def test_convert_mm_to_km(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Millimeter(), Kilometer())
        self.assertEqual(1, unit2)
        
    def test_convert_mm_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(1, Millimeter(), Milliinch())
        self.assertEqual(39.37007874015748, unit2)
        
    def test_convert_mm_to_inch(self):
        unit2 = Converter.ConvertUnitToUnit(1, Millimeter(), Inch())
        self.assertEqual(0.03937007874015748, unit2)
        
    def test_convert_mm_to_ft(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millimeter(), Feet())
        self.assertEqual(3.2808400000000035, unit2)
        
    def test_convert_mm_to_yard(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millimeter(), Yard())
        self.assertEqual(1.0936132983377078, unit2)
        
    def test_convert_mm_to_mile(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Millimeter(), Mile())
        self.assertEqual(0.621371192237334, unit2)






    def test_convert_meter_to_microm(self):
        unit2 = Converter.ConvertUnitToUnit(0.000001, Meter(), Micrometer())
        self.assertEqual(1, unit2)
        
    def test_convert_meter_to_mm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Meter(), Millimeter())
        self.assertEqual(1000, unit2)
        
    def test_convert_meter_to_meter(self):
        unit2 = Converter.ConvertUnitToUnit(1, Meter(), Meter())
        self.assertEqual(1, unit2)
        
    def test_convert_meter_to_cm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Meter(), Centimeter())
        self.assertEqual(100, unit2)
        
    def test_convert_meter_to_dm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Meter(), Decimeter())
        self.assertEqual(10, unit2)
        
    def test_convert_meter_to_km(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Meter(), Kilometer())
        self.assertEqual(1, unit2)
        
    def test_convert_meter_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Meter(), Milliinch())
        self.assertEqual(39.37007874015748, unit2)
        
    def test_convert_meter_to_inch(self):
        unit2 = Converter.ConvertUnitToUnit(1, Meter(), Inch())
        self.assertEqual(39.37007874015748, unit2)
        
    def test_convert_meter_to_ft(self):
        unit2 = Converter.ConvertUnitToUnit(1, Meter(), Feet())
        self.assertEqual(3.2808400000000035, unit2)
        
    def test_convert_meter_to_yard(self):
        unit2 = Converter.ConvertUnitToUnit(1, Meter(), Yard())
        self.assertEqual(1.0936132983377078, unit2)
        
    def test_convert_meter_to_mile(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Meter(), Mile())
        self.assertEqual(0.621371192237334, unit2)







    def test_convert_cm_to_microm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Centimeter(), Micrometer())
        self.assertEqual(10000, unit2)
        
    def test_convert_cm_to_mm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Centimeter(), Millimeter())
        self.assertEqual(10, unit2)
        
    def test_convert_cm_to_meter(self):
        unit2 = Converter.ConvertUnitToUnit(100, Centimeter(), Meter())
        self.assertEqual(1, unit2)
        
    def test_convert_cm_to_cm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Centimeter(), Centimeter())
        self.assertEqual(1, unit2)
        
    def test_convert_cm_to_dm(self):
        unit2 = Converter.ConvertUnitToUnit(10, Centimeter(), Decimeter())
        self.assertEqual(1, unit2)
        
    def test_convert_cm_to_km(self):
        unit2 = Converter.ConvertUnitToUnit(100, Centimeter(), Kilometer())
        self.assertEqual(0.001, unit2)
        
    def test_convert_cm_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(1, Centimeter(), Milliinch())
        self.assertEqual(393.7007874015748, unit2)
        
    def test_convert_cm_to_inch(self):
        unit2 = Converter.ConvertUnitToUnit(1, Centimeter(), Inch())
        self.assertEqual(0.3937007874015748, unit2)
        
    def test_convert_cm_to_ft(self):
        unit2 = Converter.ConvertUnitToUnit(1, Centimeter(), Feet())
        self.assertEqual(0.032808400000000036, unit2)
        
    def test_convert_cm_to_yard(self):
        unit2 = Converter.ConvertUnitToUnit(100, Centimeter(), Yard())
        self.assertEqual(1.0936132983377078, unit2)
        
    def test_convert_cm_to_mile(self):
        unit2 = Converter.ConvertUnitToUnit(100000, Centimeter(), Mile())
        self.assertEqual(0.621371192237334, unit2)







    def test_convert_dm_to_microm(self):
        unit2 = Converter.ConvertUnitToUnit(10, Decimeter(), Micrometer())
        self.assertEqual(1000000, unit2)
        
    def test_convert_dm_to_mm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Decimeter(), Millimeter())
        self.assertEqual(100, unit2)
        
    def test_convert_dm_to_meter(self):
        unit2 = Converter.ConvertUnitToUnit(1, Decimeter(), Meter())
        self.assertEqual(0.1, unit2)
        
    def test_convert_dm_to_cm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Decimeter(), Centimeter())
        self.assertEqual(10, unit2)
        
    def test_convert_dm_to_dm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Decimeter(), Decimeter())
        self.assertEqual(1, unit2)
        
    def test_convert_dm_to_km(self):
        unit2 = Converter.ConvertUnitToUnit(10000, Decimeter(), Kilometer())
        self.assertEqual(1, unit2)
        
    def test_convert_dm_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Decimeter(), Milliinch())
        self.assertEqual(3.937007874015748, unit2)
        
    def test_convert_dm_to_inch(self):
        unit2 = Converter.ConvertUnitToUnit(1, Decimeter(), Inch())
        self.assertEqual(3.9370078740157486, unit2)
        
    def test_convert_dm_to_ft(self):
        unit2 = Converter.ConvertUnitToUnit(1, Decimeter(), Feet())
        self.assertEqual(0.3280840000000004, unit2)
        
    def test_convert_dm_to_yard(self):
        unit2 = Converter.ConvertUnitToUnit(10, Decimeter(), Yard())
        self.assertEqual(1.0936132983377078, unit2)
        
    def test_convert_dm_to_mile(self):
        unit2 = Converter.ConvertUnitToUnit(10000, Decimeter(), Mile())
        self.assertEqual(0.621371192237334, unit2)






    def test_convert_km_to_microm(self):
        unit2 = Converter.ConvertUnitToUnit(.001, Kilometer(), Micrometer())
        self.assertEqual(1000000, unit2)
        
    def test_convert_km_to_mm(self):
        unit2 = Converter.ConvertUnitToUnit(.000001, Kilometer(), Millimeter())
        self.assertEqual(1, unit2)
        
    def test_convert_km_to_meter(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilometer(), Meter())
        self.assertEqual(1000, unit2)
        
    def test_convert_km_to_cm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilometer(), Centimeter())
        self.assertEqual(100000, unit2)
        
    def test_convert_km_to_dm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilometer(), Decimeter())
        self.assertEqual(10000, unit2)
        
    def test_convert_km_to_km(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilometer(), Kilometer())
        self.assertEqual(1, unit2)
        
    def test_convert_km_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(0.000001, Kilometer(), Milliinch())
        self.assertEqual(39.37007874015748, unit2)
        
    def test_convert_km_to_inch(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Kilometer(), Inch())
        self.assertEqual(39.37007874015748, unit2)
        
    def test_convert_km_to_ft(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilometer(), Feet())
        self.assertEqual(3280.840000000004, unit2)
        
    def test_convert_km_to_yard(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilometer(), Yard())
        self.assertEqual(1093.6132983377079, unit2)
        
    def test_convert_km_to_mile(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilometer(), Mile())
        self.assertEqual(0.621371192237334, unit2)







    def test_convert_min_to_microm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Milliinch(), Micrometer())
        self.assertEqual(25.400000000000002, unit2)
        
    def test_convert_min_to_mm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Milliinch(), Millimeter())
        self.assertEqual(0.0254, unit2)
        
    def test_convert_min_to_meter(self):
        unit2 = Converter.ConvertUnitToUnit(10000, Milliinch(), Meter())
        self.assertEqual(0.254, unit2)
        
    def test_convert_min_to_cm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Milliinch(), Centimeter())
        self.assertEqual(0.00254, unit2)
        
    def test_convert_min_to_dm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Milliinch(), Decimeter())
        self.assertEqual(0.000254, unit2)
        
    def test_convert_min_to_km(self):
        unit2 = Converter.ConvertUnitToUnit(10000000, Milliinch(), Kilometer())
        self.assertEqual(0.254, unit2)
        
    def test_convert_min_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(1, Milliinch(), Milliinch())
        self.assertEqual(1, unit2)
        
    def test_convert_min_to_inch(self):
        unit2 = Converter.ConvertUnitToUnit(1, Milliinch(), Inch())
        self.assertEqual(0.001, unit2)
        
    def test_convert_min_to_ft(self):
        unit2 = Converter.ConvertUnitToUnit(100000, Milliinch(), Feet())
        self.assertEqual(8.333333600000008, unit2)
        
    def test_convert_min_to_yard(self):
        unit2 = Converter.ConvertUnitToUnit(100000, Milliinch(), Yard())
        self.assertEqual(2.7777777777777777, unit2)
        
    def test_convert_min_to_mile(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Milliinch(), Mile())
        self.assertEqual(0.015782828282828284, unit2)






    def test_convert_inch_to_microm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Inch(), Micrometer())
        self.assertEqual(25400.0, unit2)
        
    def test_convert_inch_to_mm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Inch(), Millimeter())
        self.assertEqual(25.4, unit2)
        
    def test_convert_inch_to_meter(self):
        unit2 = Converter.ConvertUnitToUnit(1, Inch(), Meter())
        self.assertEqual(0.0254, unit2)
        
    def test_convert_inch_to_cm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Inch(), Centimeter())
        self.assertEqual(2.54, unit2)
        
    def test_convert_inch_to_dm(self):
        unit2 = Converter.ConvertUnitToUnit(10, Inch(), Decimeter())
        self.assertEqual(2.54, unit2)
        
    def test_convert_inch_to_km(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Inch(), Kilometer())
        self.assertEqual(25.4, unit2)
        
    def test_convert_inch_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Inch(), Milliinch())
        self.assertEqual(1, unit2)
        
    def test_convert_inch_to_inch(self):
        unit2 = Converter.ConvertUnitToUnit(1, Inch(), Inch())
        self.assertEqual(1, unit2)
        
    def test_convert_inch_to_ft(self):
        unit2 = Converter.ConvertUnitToUnit(1, Inch(), Feet())
        self.assertEqual(0.08333333600000009, unit2)
        
    def test_convert_inch_to_yard(self):
        unit2 = Converter.ConvertUnitToUnit(36, Inch(), Yard())
        self.assertEqual(1, unit2)
        
    def test_convert_inch_to_mile(self):
        unit2 = Converter.ConvertUnitToUnit(63360, Inch(), Mile())
        self.assertEqual(0.9999999999999999, unit2)






    def test_convert_ft_to_microm(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Feet(), Micrometer())
        self.assertEqual(304.7999902464, unit2)
        
    def test_convert_ft_to_mm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Feet(), Millimeter())
        self.assertEqual(304.79999024639994, unit2)
        
    def test_convert_ft_to_meter(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Feet(), Meter())
        self.assertEqual(304.7999902464, unit2)
        
    def test_convert_ft_to_cm(self):
        unit2 = Converter.ConvertUnitToUnit(10, Feet(), Centimeter())
        self.assertEqual(304.7999902464, unit2)
        
    def test_convert_ft_to_dm(self):
        unit2 = Converter.ConvertUnitToUnit(100, Feet(), Decimeter())
        self.assertEqual(304.79999024639994, unit2)
        
    def test_convert_ft_to_km(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Feet(), Kilometer())
        self.assertEqual(304.7999902464, unit2)
        
    def test_convert_ft_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Feet(), Milliinch())
        self.assertEqual(11.999999615999998, unit2)
        
    def test_convert_ft_to_inch(self):
        unit2 = Converter.ConvertUnitToUnit(1, Feet(), Inch())
        self.assertEqual(11.999999616, unit2)
        
    def test_convert_ft_to_ft(self):
        unit2 = Converter.ConvertUnitToUnit(1, Feet(), Feet())
        self.assertEqual(1, unit2)
        
    def test_convert_ft_to_yard(self):
        unit2 = Converter.ConvertUnitToUnit(3, Feet(), Yard())
        self.assertEqual(0.9999999679999999, unit2)
        
    def test_convert_ft_to_mile(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Feet(), Mile())
        self.assertEqual(0.18939393333333332, unit2)







    def test_convert_yard_to_microm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Yard(), Micrometer())
        self.assertEqual(914400, unit2)
        
    def test_convert_yard_to_mm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Yard(), Millimeter())
        self.assertEqual(914.4, unit2)
        
    def test_convert_yard_to_meter(self):
        unit2 = Converter.ConvertUnitToUnit(1, Yard(), Meter())
        self.assertEqual(0.9144, unit2)
        
    def test_convert_yard_to_cm(self):
        unit2 = Converter.ConvertUnitToUnit(0.1, Yard(), Centimeter())
        self.assertEqual(9.144, unit2)
        
    def test_convert_yard_to_dm(self):
        unit2 = Converter.ConvertUnitToUnit(0.1, Yard(), Decimeter())
        self.assertEqual(0.9144, unit2)
        
    def test_convert_yard_to_km(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Yard(), Kilometer())
        self.assertEqual(0.9144, unit2)
        
    def test_convert_yard_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(1, Yard(), Milliinch())
        self.assertEqual(36000.0, unit2)
        
    def test_convert_yard_to_inch(self):
        unit2 = Converter.ConvertUnitToUnit(1, Yard(), Inch())
        self.assertEqual(36, unit2)
        
    def test_convert_yard_to_ft(self):
        unit2 = Converter.ConvertUnitToUnit(1, Yard(), Feet())
        self.assertEqual(3.000000096000003, unit2)
        
    def test_convert_yard_to_yard(self):
        unit2 = Converter.ConvertUnitToUnit(1, Yard(), Yard())
        self.assertEqual(1, unit2)
        
    def test_convert_yard_to_mile(self):
        unit2 = Converter.ConvertUnitToUnit(1760, Yard(), Mile())
        self.assertEqual(1, unit2)







    def test_convert_mile_to_microm(self):
        unit2 = Converter.ConvertUnitToUnit(0.000001, Mile(), Micrometer())
        self.assertEqual(1609.344, unit2)
        
    def test_convert_mile_to_mm(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Mile(), Millimeter())
        self.assertEqual(1609.344, unit2)
        
    def test_convert_mile_to_meter(self):
        unit2 = Converter.ConvertUnitToUnit(1, Mile(), Meter())
        self.assertEqual(1609.344, unit2)
        
    def test_convert_mile_to_cm(self):
        unit2 = Converter.ConvertUnitToUnit(0.01, Mile(), Centimeter())
        self.assertEqual(1609.344, unit2)
        
    def test_convert_mile_to_dm(self):
        unit2 = Converter.ConvertUnitToUnit(0.1, Mile(), Decimeter())
        self.assertEqual(1609.344, unit2)
        
    def test_convert_mile_to_km(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Mile(), Kilometer())
        self.assertEqual(1609.344, unit2)
        
    def test_convert_mile_to_min(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Mile(), Milliinch())
        self.assertEqual(63360.0, unit2)
        
    def test_convert_mile_to_inch(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Mile(), Inch())
        self.assertEqual(63.36000000000001, unit2)
        
    def test_convert_mile_to_ft(self):
        unit2 = Converter.ConvertUnitToUnit(1, Mile(), Feet())
        self.assertEqual(5280.000168960006, unit2)
        
    def test_convert_mile_to_yard(self):
        unit2 = Converter.ConvertUnitToUnit(1, Mile(), Yard())
        self.assertEqual(1760, unit2)
        
    def test_convert_mile_to_mile(self):
        unit2 = Converter.ConvertUnitToUnit(1, Mile(), Mile())
        self.assertEqual(1, unit2)

        
if __name__ == "__main__":
    unittest.main()