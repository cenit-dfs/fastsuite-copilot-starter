import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Luminance import *

class LuminanceTest(unittest.TestCase):

    def test_isDefault(self):
        caf2 = Candelapersquarefoot()
        cain2= Candelapersquareinch()
        capmm2 = Candelapersquaremillimeter()
        capm2 = Candelapersquaremeter()

        self.assertFalse(caf2.IsDefault(), "Candelapersquarefoot must not be default")
        self.assertFalse(cain2.IsDefault(), "Candelapersquareinch must not be default")
        self.assertFalse(capmm2.IsDefault(), "Candelapersquaremillimeter must not be default")
        self.assertTrue(capm2.IsDefault(), "Candelapersquaremeter must be default")

    def test_UnitGroup(self):
        caf2 = Candelapersquarefoot()
        cain2= Candelapersquareinch()
        capmm2 = Candelapersquaremillimeter()
        capm2 = Candelapersquaremeter()

        self.assertEqual(caf2.GetUnitGroup(), UnitGroups.Luminance)
        self.assertEqual(cain2.GetUnitGroup(), UnitGroups.Luminance)
        self.assertEqual(capmm2.GetUnitGroup(), UnitGroups.Luminance)
        self.assertEqual(capm2.GetUnitGroup(), UnitGroups.Luminance)

    def test_convert_capmm2_to_caf2(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Candelapersquaremillimeter(), Candelapersquarefoot())
        self.assertEqual(92.90304359661127, unit2)

    def test_convert_capmm2_to_cain2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Candelapersquaremillimeter(), Candelapersquareinch())
        self.assertEqual(645.160041625726, unit2)

    def test_convert_capmm2_to_capm2(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Candelapersquaremillimeter(), Candelapersquaremeter())
        self.assertEqual(1000, unit2)

    def test_converr_caf2_to_capmm2(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Candelapersquarefoot(), Candelapersquaremillimeter())
        self.assertEqual(0.01076391, unit2)

    def test_convert_cain2_to_capmm2(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Candelapersquareinch(), Candelapersquaremillimeter())
        self.assertEqual(1.550003, unit2)

    def test_convert_capm2_to_capmm2(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Candelapersquaremeter(), Candelapersquaremillimeter())
        self.assertEqual(1, unit2)

    def test_convert_caf2_to_cain2(self):
        unit2 = Converter.ConvertUnitToUnit(143.99999628387826, Candelapersquarefoot(), Candelapersquareinch())
        self.assertEqual(1, unit2)

    def test_convert_caf2_to_capm2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Candelapersquarefoot(), Candelapersquaremeter())
        self.assertEqual(10.76391, unit2)

    def test_convert_cain2_to_capm2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Candelapersquareinch(), Candelapersquaremeter())
        self.assertEqual(1550.003, unit2)

    def test_convert_cain2_to_caf2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Candelapersquareinch(), Candelapersquarefoot())
        self.assertEqual(143.99999628387826, unit2)
      
    def test_convert_capm2_to_cain2(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Candelapersquaremeter(), Candelapersquareinch())
        self.assertEqual(0.6451600416257259, unit2)

    def test_convert_capm2_to_caf2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Candelapersquaremeter(), Candelapersquarefoot())
        self.assertEqual(0.09290304359661128, unit2)
      
    def test_convert_caf2_to_caf2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Candelapersquarefoot(), Candelapersquarefoot())
        self.assertEqual(1, unit2)

    def test_convert_cain2_to_cain2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Candelapersquareinch(), Candelapersquareinch())
        self.assertEqual(1, unit2)
              
    def test_convert_capm2_to_capm2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Candelapersquaremeter(), Candelapersquaremeter())
        self.assertEqual(1, unit2)

    def test_convert_capmm2_to_capmm2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Candelapersquaremillimeter(), Candelapersquaremillimeter())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()