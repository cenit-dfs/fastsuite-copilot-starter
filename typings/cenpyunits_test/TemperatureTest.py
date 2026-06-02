import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Temperature import *

class TemperatureTest(unittest.TestCase):

    def test_isDefault(self):
        celsius = Celsius()
        kelvin= Kelvin()
        fahrenheit = Fahrenheit()


        self.assertTrue(celsius.IsDefault(), "Celsius must be default")
        self.assertFalse(kelvin.IsDefault(), "Kelvin must not be default")
        self.assertFalse(fahrenheit.IsDefault(), "Fahrenheit must not be default")

    def test_UnitGroup(self):
        celsius = Celsius()
        kelvin= Kelvin()
        fahrenheit = Fahrenheit()

        self.assertEqual(celsius.GetUnitGroup(), UnitGroups.Temperature)
        self.assertEqual(kelvin.GetUnitGroup(), UnitGroups.Temperature)
        self.assertEqual(fahrenheit.GetUnitGroup(), UnitGroups.Temperature)

    def test_convert_fahrenheit_to_celsius(self):
        unit2 = Converter.ConvertUnitToUnit(32, Fahrenheit(), Celsius())
        self.assertEqual(0, unit2)

    def test_convert_fahrenheit_to_kelvin(self):
        unit2 = Converter.ConvertUnitToUnit(32, Fahrenheit(), Kelvin())
        self.assertEqual(273.15, unit2)

    def test_converr_celsius_to_fahrenheit(self):
        unit2 = Converter.ConvertUnitToUnit(0, Celsius(), Fahrenheit())
        self.assertEqual(32, unit2)

    def test_convert_kelvin_to_fahrenheit(self):
        unit2 = Converter.ConvertUnitToUnit(273.15, Kelvin(), Fahrenheit())
        self.assertEqual(32, unit2)

    def test_convert_celsius_to_kelvin(self):
        unit2 = Converter.ConvertUnitToUnit(0, Celsius(), Kelvin())
        self.assertEqual(273.15, unit2)

    def test_convert_kelvin_to_celsius(self):
        unit2 = Converter.ConvertUnitToUnit(273.15, Kelvin(), Celsius())
        self.assertEqual(0, unit2)
      
    def test_convert_celsius_to_celsius(self):
        unit2 = Converter.ConvertUnitToUnit(1, Celsius(), Celsius())
        self.assertEqual(1, unit2)

    def test_convert_kelvin_to_kelvin(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kelvin(), Kelvin())
        self.assertEqual(1, unit2)

    def test_convert_fahrenheit_to_fahrenheit(self):
        unit2 = Converter.ConvertUnitToUnit(100, Fahrenheit(), Fahrenheit())
        self.assertEqual(100, unit2)

if __name__ == "__main__":
    unittest.main()


