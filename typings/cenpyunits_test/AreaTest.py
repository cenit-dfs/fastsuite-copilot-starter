import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Area import *

class AreaTest(unittest.TestCase):
    
    def test_isDefault(self):
        sm = SquareMeter()
        smm= SquareMillimeter()
        si = SquareInch()
        sf = SquareFoot()

        self.assertTrue(sm.IsDefault(), "SquareMeter must be default")
        self.assertFalse(smm.IsDefault(), "SquareMillimeter must not be default")
        self.assertFalse(si.IsDefault(), "SquareInch must not be default")
        self.assertFalse(sf.IsDefault(), "SquareFoot must not be default")

    def test_UnitGroup(self):
        sm = SquareMeter()
        smm= SquareMillimeter()
        si = SquareInch()
        sf = SquareFoot()

        self.assertEqual(sm.GetUnitGroup(), UnitGroups.Area)
        self.assertEqual(smm.GetUnitGroup(), UnitGroups.Area)
        self.assertEqual(si.GetUnitGroup(), UnitGroups.Area)
        self.assertEqual(sf.GetUnitGroup(), UnitGroups.Area)

    def test_convert_sm_to_sm(self):
        unit2 = Converter.ConvertUnitToUnit(1, SquareMeter(), SquareMeter())
        self.assertEqual(1, unit2)

    def test_convert_sm_to_smm(self):
        unit2 = Converter.ConvertUnitToUnit(1, SquareMeter(), SquareMillimeter())
        self.assertEqual(1000000, unit2)
        
    def test_convert_sm_to_si(self):
        unit2 = Converter.ConvertUnitToUnit(1, SquareMeter(), SquareInch())
        self.assertEqual(1550.0031000062002, unit2)
        
    def test_convert_sm_to_sf(self):
        unit2 = Converter.ConvertUnitToUnit(1, SquareMeter(), SquareFoot())
        self.assertEqual(10.763910416709722, unit2)
        
    def test_convert_smm_to_sm(self):
        unit2 = Converter.ConvertUnitToUnit(1, SquareMillimeter(), SquareMeter())
        self.assertEqual(0.000001, unit2)

    def test_convert_smm_to_smm(self):
        unit2 = Converter.ConvertUnitToUnit(1, SquareMillimeter(), SquareMillimeter())
        self.assertEqual(1, unit2)
        
    def test_convert_smm_to_si(self):
        unit2 = Converter.ConvertUnitToUnit(1, SquareMillimeter(), SquareInch())
        self.assertEqual(0.0015500031000062, unit2)
        
    def test_convert_smm_to_sf(self):
        unit2 = Converter.ConvertUnitToUnit(1000, SquareMillimeter(), SquareFoot())
        self.assertEqual(0.010763910416709722, unit2)
        
    def test_convert_si_to_sm(self):
        unit2 = Converter.ConvertUnitToUnit(1550.0031000062002, SquareInch(), SquareMeter())
        self.assertEqual(1, unit2)

    def test_convert_si_to_smm(self):
        unit2 = Converter.ConvertUnitToUnit(0.0015500031000062, SquareInch(), SquareMillimeter())
        self.assertEqual(1, unit2)
        
    def test_convert_si_to_si(self):
        unit2 = Converter.ConvertUnitToUnit(1, SquareInch(), SquareInch())
        self.assertEqual(1, unit2)
        
    def test_convert_si_to_sf(self):
        unit2 = Converter.ConvertUnitToUnit(1000, SquareInch(), SquareFoot())
        self.assertEqual(6.944444444444444, unit2)
        
    def test_convert_sf_to_sm(self):
        unit2 = Converter.ConvertUnitToUnit(10.763910416709722, SquareFoot(), SquareMeter())
        self.assertEqual(1, unit2)

    def test_convert_sf_to_smm(self):
        unit2 = Converter.ConvertUnitToUnit(0.010763910416709722, SquareFoot(), SquareMillimeter())
        self.assertEqual(1000.0000000000001, unit2)
        
    def test_convert_sf_to_si(self):
        unit2 = Converter.ConvertUnitToUnit(6.944444444444444, SquareFoot(), SquareInch())
        self.assertEqual(1000, unit2)
        
    def test_convert_sf_to_sf(self):
        unit2 = Converter.ConvertUnitToUnit(1, SquareFoot(), SquareFoot())
        self.assertEqual(1, unit2)

        
if __name__ == "__main__":
    unittest.main()