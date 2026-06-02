import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.MagneticFlux import *

class MagneticFluxTest(unittest.TestCase):

    def test_isDefault(self):
        tmm2 = Teslasquaremillimeter()
        tm2= Teslasquaremeter()
        mw = Milliweber()
        weber = Weber()

        self.assertFalse(tmm2.IsDefault(), "Teslasquaremillimeter must not be default")
        self.assertFalse(tm2.IsDefault(), "Teslasquaremeter must not be default")
        self.assertFalse(mw.IsDefault(), "Milliweber must not be default")
        self.assertTrue(weber.IsDefault(), "Weber must be default")

    def test_UnitGroup(self):
        tmm2 = Teslasquaremillimeter()
        tm2= Teslasquaremeter()
        mw = Milliweber()
        weber = Weber()

        self.assertEqual(tmm2.GetUnitGroup(), UnitGroups.MagneticFlux)
        self.assertEqual(tm2.GetUnitGroup(), UnitGroups.MagneticFlux)
        self.assertEqual(mw.GetUnitGroup(), UnitGroups.MagneticFlux)
        self.assertEqual(weber.GetUnitGroup(), UnitGroups.MagneticFlux)

    def test_convert_mw_to_tmm2(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Milliweber(), Teslasquaremillimeter())
        self.assertEqual(1, unit2)

    def test_convert_mw_to_tm2(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Milliweber(), Teslasquaremeter())
        self.assertEqual(1, unit2)

    def test_convert_mw_to_weber(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Milliweber(), Weber())
        self.assertEqual(1, unit2)

    def test_converr_tmm2_to_mw(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Teslasquaremillimeter(), Milliweber())
        self.assertEqual(1, unit2)

    def test_convert_tm2_to_mw(self):
        unit2 = Converter.ConvertUnitToUnit(1, Teslasquaremeter(), Milliweber())
        self.assertEqual(1000, unit2)

    def test_convert_weber_to_mw(self):
        unit2 = Converter.ConvertUnitToUnit(1, Weber(), Milliweber())
        self.assertEqual(1000, unit2)

    def test_convert_tmm2_to_tm2(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Teslasquaremillimeter(), Teslasquaremeter())
        self.assertEqual(0.001, unit2)

    def test_convert_tmm2_to_weber(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Teslasquaremillimeter(), Weber())
        self.assertEqual(1, unit2)

    def test_convert_tm2_to_weber(self):
        unit2 = Converter.ConvertUnitToUnit(1, Teslasquaremeter(), Weber())
        self.assertEqual(1, unit2)

    def test_convert_tm2_to_tmm2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Teslasquaremeter(), Teslasquaremillimeter())
        self.assertEqual(1000000, unit2)
      
    def test_convert_weber_to_tm2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Weber(), Teslasquaremeter())
        self.assertEqual(1, unit2)

    def test_convert_weber_to_tmm2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Weber(), Teslasquaremillimeter())
        self.assertEqual(1000000.0, unit2)
      
    def test_convert_tmm2_to_tmm2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Teslasquaremillimeter(), Teslasquaremillimeter())
        self.assertEqual(1, unit2)

    def test_convert_tm2_to_tm2(self):
        unit2 = Converter.ConvertUnitToUnit(1, Teslasquaremeter(), Teslasquaremeter())
        self.assertEqual(1, unit2)
              
    def test_convert_weber_to_weber(self):
        unit2 = Converter.ConvertUnitToUnit(1, Weber(), Weber())
        self.assertEqual(1, unit2)

    def test_convert_mw_to_mw(self):
        unit2 = Converter.ConvertUnitToUnit(1, Milliweber(), Milliweber())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()
