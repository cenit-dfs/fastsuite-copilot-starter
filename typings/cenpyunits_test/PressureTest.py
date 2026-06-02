import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Pressure import *

class PressureTest(unittest.TestCase):

    def test_isDefault(self):
        pascal = Pascal()
        millip = Millipascal()
        megap = Megapascal()
        bar = Bar()
        oz= Ouncepersquareinch()
        lb = Poundpersquareinch()
        kpa = Kilopascal()

        self.assertTrue(pascal.IsDefault(), "Pascal must be default")
        self.assertFalse(millip.IsDefault(), "Millipascal must not be default")
        self.assertFalse(megap.IsDefault(), "Megapascal must not be default")
        self.assertFalse(bar.IsDefault(), "Bar must not be default")
        self.assertFalse(oz.IsDefault(), "Ouncepersquareinch must not be default")
        self.assertFalse(lb.IsDefault(), "Poundpersquareinch must not be default")
        self.assertFalse(kpa.IsDefault(), "Kilopascal must not be default")

    def test_UnitGroup(self):
        pascal = Pascal()
        millip= Millipascal()
        megap = Megapascal()
        bar = Bar()
        oz= Ouncepersquareinch()
        lb = Poundpersquareinch()
        kpa = Kilopascal()

        self.assertEqual(pascal.GetUnitGroup(), UnitGroups.Pressure)
        self.assertEqual(millip.GetUnitGroup(), UnitGroups.Pressure)
        self.assertEqual(megap.GetUnitGroup(), UnitGroups.Pressure)
        self.assertEqual(bar.GetUnitGroup(), UnitGroups.Pressure)
        self.assertEqual(oz.GetUnitGroup(), UnitGroups.Pressure)
        self.assertEqual(lb.GetUnitGroup(), UnitGroups.Pressure)
        self.assertEqual(kpa.GetUnitGroup(), UnitGroups.Pressure)

    def test_convert_pascal_to_pascal(self):
        unit2 = Converter.ConvertUnitToUnit(1, Pascal(), Pascal())
        self.assertEqual(1, unit2)

    def test_convert_pascal_to_millip(self):
        unit2 = Converter.ConvertUnitToUnit(1, Pascal(), Millipascal())
        self.assertEqual(1000, unit2)
        
    def test_convert_pascal_to_megap(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Pascal(), Megapascal())
        self.assertEqual(0.001, unit2)
        
    def test_convert_pascal_to_bar(self):
        unit2 = Converter.ConvertUnitToUnit(100000, Pascal(), Bar())
        self.assertEqual(1, unit2)
        
    def test_convert_pascal_to_oz(self):
        unit2 = Converter.ConvertUnitToUnit(100, Pascal(), Ouncepersquareinch())
        self.assertEqual(0.23209998495992099, unit2)

    def test_convert_pascal_to_lb(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Pascal(), Poundpersquareinch())
        self.assertEqual(0.1450000005075, unit2)
                        
    def test_convert_pascal_to_kpa(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Pascal(), Kilopascal())
        self.assertEqual(1, unit2)
        
    def test_convert_millip_to_pascal(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millipascal(), Pascal())
        self.assertEqual(1, unit2)
        
    def test_convert_millip_to_millip(self):
        unit2 = Converter.ConvertUnitToUnit(1, Millipascal(), Millipascal())
        self.assertEqual(1, unit2)
        
    def test_convert_millip_to_megap(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Millipascal(), Megapascal())
        self.assertEqual(0.001, unit2)

    def test_convert_millip_to_bar(self):
        unit2 = Converter.ConvertUnitToUnit(100000000, Millipascal(), Bar())
        self.assertEqual(1, unit2)
        
    def test_convert_millip_to_oz(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millipascal(), Ouncepersquareinch())
        self.assertEqual(0.00232099984959921, unit2)
        
    def test_convert_millip_to_lb(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Millipascal(), Poundpersquareinch())
        self.assertEqual(0.1450000005075, unit2)
        
    def test_convert_millip_to_kpa(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Millipascal(), Kilopascal())
        self.assertEqual(0.001, unit2)

    def test_convert_megap_to_pascal(self):
        unit2 = Converter.ConvertUnitToUnit(1, Megapascal(), Pascal())
        self.assertEqual(1000000, unit2)
        
    def test_convert_megap_to_millip(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Megapascal(), Millipascal())
        self.assertEqual(1000000, unit2)
        
    def test_convert_megap_to_megap(self):
        unit2 = Converter.ConvertUnitToUnit(1, Megapascal(), Megapascal())
        self.assertEqual(1, unit2)

    def test_convert_megap_to_bar(self):
        unit2 = Converter.ConvertUnitToUnit(0.1, Megapascal(), Bar())
        self.assertEqual(1, unit2)

    def test_convert_megap_to_oz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Megapascal(), Ouncepersquareinch())
        self.assertEqual(2320.99984959921, unit2)
        
    def test_convert_megap_to_lb(self):
        unit2 = Converter.ConvertUnitToUnit(1, Megapascal(), Poundpersquareinch())
        self.assertEqual(145.0000005075, unit2)
        
    def test_convert_megap_to_kpa(self):
        unit2 = Converter.ConvertUnitToUnit(1, Megapascal(), Kilopascal())
        self.assertEqual(1000, unit2)
        
    def test_convert_bar_to_pascal(self):
        unit2 = Converter.ConvertUnitToUnit(1, Bar(), Pascal())
        self.assertEqual(100000, unit2)

    def test_convert_bar_to_millip(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Bar(), Millipascal())
        self.assertEqual(100000.0, unit2)
        
    def test_convert_bar_to_megap(self):
        unit2 = Converter.ConvertUnitToUnit(1, Bar(), Megapascal())
        self.assertEqual(0.1, unit2)
        
    def test_convert_bar_to_bar(self):
        unit2 = Converter.ConvertUnitToUnit(1, Bar(), Bar())
        self.assertEqual(1, unit2)
        
    def test_convert_bar_to_oz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Bar(), Ouncepersquareinch())
        self.assertEqual(232.099984959921, unit2)

    def test_convert_bar_to_lb(self):
        unit2 = Converter.ConvertUnitToUnit(1, Bar(), Poundpersquareinch())
        self.assertEqual(14.50000005075, unit2)
        
    def test_convert_bar_to_kpa(self):
        unit2 = Converter.ConvertUnitToUnit(1, Bar(), Kilopascal())
        self.assertEqual(100, unit2)
        
    def test_convert_oz_to_pascal(self):
        unit2 = Converter.ConvertUnitToUnit(1, Ouncepersquareinch(), Pascal())
        self.assertEqual(430.8488, unit2)
        
    def test_convert_oz_to_millip(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Ouncepersquareinch(), Millipascal())
        self.assertEqual(430.8488, unit2)

    def test_convert_oz_to_megap(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Ouncepersquareinch(), Megapascal())
        self.assertEqual(0.4308488, unit2)
        
    def test_convert_oz_to_bar(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Ouncepersquareinch(), Bar())
        self.assertEqual(4.308488, unit2)
        
    def test_convert_oz_to_oz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Ouncepersquareinch(), Ouncepersquareinch())
        self.assertEqual(1, unit2)

    def test_convert_oz_to_lb(self):
        unit2 = Converter.ConvertUnitToUnit(1, Ouncepersquareinch(), Poundpersquareinch())
        self.assertEqual(0.06247307621865576, unit2)

    def test_convert_oz_to_kpa(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Ouncepersquareinch(), Kilopascal())
        self.assertEqual(430.8488, unit2)
        
    def test_convert_lb_to_pascal(self):
        unit2 = Converter.ConvertUnitToUnit(1, Poundpersquareinch(), Pascal())
        self.assertEqual(6896.5517, unit2)
        
    def test_convert_lb_to_millip(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Poundpersquareinch(), Millipascal())
        self.assertEqual(6896.5517, unit2)
        
    def test_convert_lb_to_megap(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Poundpersquareinch(), Megapascal())
        self.assertEqual(6.8965517, unit2)

    def test_convert_lb_to_bar(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Poundpersquareinch(), Bar())
        self.assertEqual(68.965517, unit2)
        
    def test_convert_lb_to_oz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Poundpersquareinch(), Ouncepersquareinch())
        self.assertEqual(16.006895458453176, unit2)
        
    def test_convert_lb_to_lb(self):
        unit2 = Converter.ConvertUnitToUnit(1, Poundpersquareinch(), Poundpersquareinch())
        self.assertEqual(1, unit2)
        
    def test_convert_lb_to_kpa(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Poundpersquareinch(), Kilopascal())
        self.assertEqual(6896.5517, unit2)

    def test_convert_kpa_to_pascal(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilopascal(), Pascal())
        self.assertEqual(1000, unit2)
        
    def test_convert_kpa_to_millip(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilopascal(), Millipascal())
        self.assertEqual(1000000, unit2)
        
    def test_convert_kpa_to_megap(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilopascal(), Megapascal())
        self.assertEqual(0.001, unit2)
        
    def test_convert_kpa_to_bar(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilopascal(), Bar())
        self.assertEqual(0.01, unit2)

    def test_convert_kpa_to_oz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilopascal(), Ouncepersquareinch())
        self.assertEqual(2.3209998495992097, unit2)
        
    def test_convert_kpa_to_lb(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilopascal(), Poundpersquareinch())
        self.assertEqual(0.1450000005075, unit2)
        
    def test_convert_kpa_to_kpa(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilopascal(), Kilopascal())
        self.assertEqual(1, unit2)




if __name__ == "__main__":
    unittest.main()
