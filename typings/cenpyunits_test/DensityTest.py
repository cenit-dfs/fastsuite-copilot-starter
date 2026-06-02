import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Density import *

class DensityTest(unittest.TestCase):
    
    def test_isDefault(self):
        kg3m = Kilogramcubicmeter()
        gm3= Gramcubicmeter()
        kgmm3 = Kilogramcubicmillimeter()
        mgm3 = Milligramcubicmeter()
        ozin3= Ouncecubicinch()
        pin3 = Poundcubicinch()
        tm3 = Tonnecubicmeter()

        self.assertTrue(kg3m.IsDefault(), "Kilogramcubicmeter must be default")
        self.assertFalse(gm3.IsDefault(), "Gramcubicmeter must not be default")
        self.assertFalse(kgmm3.IsDefault(), "Kilogramcubicmillimeter must not be default")
        self.assertFalse(mgm3.IsDefault(), "Milligramcubicmeter must not be default")
        self.assertFalse(ozin3.IsDefault(), "Ouncecubicinch must not be default")
        self.assertFalse(pin3.IsDefault(), "Poundcubicinch must not be default")
        self.assertFalse(tm3.IsDefault(), "Tonnecubicmeter must not be default")

    def test_UnitGroup(self):
        kg3m = Kilogramcubicmeter()
        gm3= Gramcubicmeter()
        kgmm3 = Kilogramcubicmillimeter()
        mgm3 = Milligramcubicmeter()
        ozin3= Ouncecubicinch()
        pin3 = Poundcubicinch()
        tm3 = Tonnecubicmeter()

        self.assertEqual(kg3m.GetUnitGroup(), UnitGroups.Density)
        self.assertEqual(gm3.GetUnitGroup(), UnitGroups.Density)
        self.assertEqual(kgmm3.GetUnitGroup(), UnitGroups.Density)
        self.assertEqual(mgm3.GetUnitGroup(), UnitGroups.Density)
        self.assertEqual(ozin3.GetUnitGroup(), UnitGroups.Density)
        self.assertEqual(pin3.GetUnitGroup(), UnitGroups.Density)
        self.assertEqual(tm3.GetUnitGroup(), UnitGroups.Density)

    def test_convert_kg3m_to_kg3m(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilogramcubicmeter(), Kilogramcubicmeter())
        self.assertEqual(1, unit2)

    def test_convert_kg3m_to_gm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilogramcubicmeter(), Gramcubicmeter())
        self.assertEqual(1000, unit2)
        
    def test_convert_kg3m_to_kgmm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilogramcubicmeter(), Kilogramcubicmillimeter())
        self.assertEqual(.000000001, unit2)
        
    def test_convert_kg3m_to_mgm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilogramcubicmeter(), Milligramcubicmeter())
        self.assertEqual(1000000, unit2)
        
    def test_convert_kg3m_to_ozin3(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Kilogramcubicmeter(), Ouncecubicinch())
        self.assertEqual(0.5779999352640073, unit2)

    def test_convert_kg3m_to_pin3(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Kilogramcubicmeter(), Poundcubicinch())
        self.assertEqual(0.036130000075873, unit2)
                        
    def test_convert_kg3m_to_tm3(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Kilogramcubicmeter(), Tonnecubicmeter())
        self.assertEqual(1, unit2)
        
    def test_convert_gm3_to_kg3m(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Gramcubicmeter(), Kilogramcubicmeter())
        self.assertEqual(1, unit2)
        
    def test_convert_gm3_to_gm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Gramcubicmeter(), Gramcubicmeter())
        self.assertEqual(1, unit2)
        
    def test_convert_gm3_to_kgmm3(self):
        unit2 = Converter.ConvertUnitToUnit(1000000000, Gramcubicmeter(), Kilogramcubicmillimeter())
        self.assertEqual(0.001, unit2)

    def test_convert_gm3_to_mgm3(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Gramcubicmeter(), Milligramcubicmeter())
        self.assertEqual(1, unit2)
        
    def test_convert_gm3_to_ozin3(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Gramcubicmeter(), Ouncecubicinch())
        self.assertEqual(0.5779999352640073, unit2)
        
    def test_convert_gm3_to_pin3(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Gramcubicmeter(), Poundcubicinch())
        self.assertEqual(0.036130000075873, unit2)
        
    def test_convert_gm3_to_tm3(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Gramcubicmeter(), Tonnecubicmeter())
        self.assertEqual(0.001, unit2)

    def test_convert_kgmm3_to_kg3m(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilogramcubicmillimeter(), Kilogramcubicmeter())
        self.assertEqual(1000000000, unit2)
        
    def test_convert_kgmm3_to_gm3(self):
        unit2 = Converter.ConvertUnitToUnit(0.000001, Kilogramcubicmillimeter(), Gramcubicmeter())
        self.assertEqual(1000000.0, unit2)
        
    def test_convert_kgmm3_to_kgmm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilogramcubicmillimeter(), Kilogramcubicmillimeter())
        self.assertEqual(1, unit2)

    def test_convert_kgmm3_to_mgm3(self):
        unit2 = Converter.ConvertUnitToUnit(.000001, Kilogramcubicmillimeter(), Milligramcubicmeter())
        self.assertEqual(1000000000.0, unit2)

    def test_convert_kgmm3_to_ozin3(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Kilogramcubicmillimeter(), Ouncecubicinch())
        self.assertEqual(577.9999352640073, unit2)
        
    def test_convert_kgmm3_to_pin3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilogramcubicmillimeter(), Poundcubicinch())
        self.assertEqual(36130.000075872995, unit2)
        
    def test_convert_kgmm3_to_tm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilogramcubicmillimeter(), Tonnecubicmeter())
        self.assertEqual(1000000.0, unit2)
        
    def test_convert_mgm3_to_kg3m(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Milligramcubicmeter(), Kilogramcubicmeter())
        self.assertEqual(1, unit2)

    def test_convert_mgm3_to_gm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Milligramcubicmeter(), Gramcubicmeter())
        self.assertEqual(0.001, unit2)
        
    def test_convert_mgm3_to_kgmm3(self):
        unit2 = Converter.ConvertUnitToUnit(1000000000, Milligramcubicmeter(), Kilogramcubicmillimeter())
        self.assertEqual(0.000001, unit2)
        
    def test_convert_mgm3_to_mgm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Milligramcubicmeter(), Milligramcubicmeter())
        self.assertEqual(1, unit2)
        
    def test_convert_mgm3_to_ozin3(self):
        unit2 = Converter.ConvertUnitToUnit(1000000000, Milligramcubicmeter(), Ouncecubicinch())
        self.assertEqual(0.5779999352640073, unit2)

    def test_convert_mgm3_to_pin3(self):
        unit2 = Converter.ConvertUnitToUnit(1000000000, Milligramcubicmeter(), Poundcubicinch())
        self.assertEqual(0.036130000075873, unit2)
        
    def test_convert_mgm3_to_tm3(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Milligramcubicmeter(), Tonnecubicmeter())
        self.assertEqual(0.001, unit2)
        
    def test_convert_ozin3_to_kg3m(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Ouncecubicinch(), Kilogramcubicmeter())
        self.assertEqual(1.730104, unit2)
        
    def test_convert_ozin3_to_gm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Ouncecubicinch(), Gramcubicmeter())
        self.assertEqual(1730104, unit2)

    def test_convert_ozin3_to_kgmm3(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Ouncecubicinch(), Kilogramcubicmillimeter())
        self.assertEqual(0.001730104, unit2)
        
    def test_convert_ozin3_to_mgm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Ouncecubicinch(), Milligramcubicmeter())
        self.assertEqual(1730104000.0000002, unit2)
        
    def test_convert_ozin3_to_ozin3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Ouncecubicinch(), Ouncecubicinch())
        self.assertEqual(1, unit2)

    def test_convert_ozin3_to_pin3(self):
        unit2 = Converter.ConvertUnitToUnit(16, Ouncecubicinch(), Poundcubicinch())
        self.assertEqual(1.0001385224202908, unit2)

    def test_convert_ozin3_to_tm3(self):
        unit2 = Converter.ConvertUnitToUnit(0.5779999352640073, Ouncecubicinch(), Tonnecubicmeter())
        self.assertEqual(1.0000000000000002, unit2)
        
    def test_convert_pin3_to_kg3m(self):
        unit2 = Converter.ConvertUnitToUnit(1, Poundcubicinch(), Kilogramcubicmeter())
        self.assertEqual(27677.83, unit2)
        
    def test_convert_pin3_to_gm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Poundcubicinch(), Gramcubicmeter())
        self.assertEqual(27677830.0, unit2)
        
    def test_convert_pin3_to_kgmm3(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Poundcubicinch(), Kilogramcubicmillimeter())
        self.assertEqual(0.02767783, unit2)

    def test_convert_pin3_to_mgm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Poundcubicinch(), Milligramcubicmeter())
        self.assertEqual(27677830000.000004, unit2)
        
    def test_convert_pin3_to_ozin3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Poundcubicinch(), Ouncecubicinch())
        self.assertEqual(15.997783948248198, unit2) # should be 16
        
    def test_convert_pin3_to_pin3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Poundcubicinch(), Poundcubicinch())
        self.assertEqual(1, unit2)
        
    def test_convert_pin3_to_tm3(self):
        unit2 = Converter.ConvertUnitToUnit(0.036130000075873, Poundcubicinch(), Tonnecubicmeter())
        self.assertEqual(1, unit2)

    def test_convert_tm3_to_kg3m(self):
        unit2 = Converter.ConvertUnitToUnit(1, Tonnecubicmeter(), Kilogramcubicmeter())
        self.assertEqual(1000, unit2)
        
    def test_convert_tm3_to_gm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Tonnecubicmeter(), Gramcubicmeter())
        self.assertEqual(1000000, unit2)
        
    def test_convert_tm3_to_kgmm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Tonnecubicmeter(), Kilogramcubicmillimeter())
        self.assertEqual(0.000001, unit2)
        
    def test_convert_tm3_to_mgm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Tonnecubicmeter(), Milligramcubicmeter())
        self.assertEqual(1000000000, unit2)

    def test_convert_tm3_to_ozin3(self):
        unit2 = Converter.ConvertUnitToUnit(1.0, Tonnecubicmeter(), Ouncecubicinch())
        self.assertEqual(0.5779999352640073, unit2)
        
    def test_convert_tm3_to_pin3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Tonnecubicmeter(), Poundcubicinch())
        self.assertEqual(0.036130000075873, unit2)
        
    def test_convert_tm3_to_tm3(self):
        unit2 = Converter.ConvertUnitToUnit(1, Tonnecubicmeter(), Tonnecubicmeter())
        self.assertEqual(1, unit2)




if __name__ == "__main__":
    unittest.main()
