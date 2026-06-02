import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Mass import *

class MassTest(unittest.TestCase):
    
    def test_isDefault(self):
        kg = Kilogram()
        gram = Gram()
        slug = Slug()
        mgram = Milligram()
        oz= Ounce()
        lb = Pound()
        tonne = Tonne()

        self.assertTrue(kg.IsDefault(), "Kilogram must be default")
        self.assertFalse(gram.IsDefault(), "Gram must not be default")
        self.assertFalse(slug.IsDefault(), "Slug must not be default")
        self.assertFalse(mgram.IsDefault(), "Milligram must not be default")
        self.assertFalse(oz.IsDefault(), "Ounce must not be default")
        self.assertFalse(lb.IsDefault(), "Pound must not be default")
        self.assertFalse(tonne.IsDefault(), "Tonne must not be default")

    def test_UnitGroup(self):
        kg = Kilogram()
        gram= Gram()
        slug = Slug()
        mgram = Milligram()
        oz= Ounce()
        lb = Pound()
        tonne = Tonne()

        self.assertEqual(kg.GetUnitGroup(), UnitGroups.Mass)
        self.assertEqual(gram.GetUnitGroup(), UnitGroups.Mass)
        self.assertEqual(slug.GetUnitGroup(), UnitGroups.Mass)
        self.assertEqual(mgram.GetUnitGroup(), UnitGroups.Mass)
        self.assertEqual(oz.GetUnitGroup(), UnitGroups.Mass)
        self.assertEqual(lb.GetUnitGroup(), UnitGroups.Mass)
        self.assertEqual(tonne.GetUnitGroup(), UnitGroups.Mass)

    def test_convert_kg_to_kg(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilogram(), Kilogram())
        self.assertEqual(1, unit2)

    def test_convert_kg_to_gram(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilogram(), Gram())
        self.assertEqual(1000, unit2)
        
    def test_convert_kg_to_slug(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilogram(), Slug())
        self.assertEqual(0.06852176603148429, unit2)
        
    def test_convert_kg_to_mgram(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilogram(), Milligram())
        self.assertEqual(1000000, unit2)
        
    def test_convert_kg_to_oz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilogram(), Ounce())
        self.assertEqual(35.27396198068672, unit2)

    def test_convert_kg_to_lb(self):
        unit2 = Converter.ConvertUnitToUnit(1, Kilogram(), Pound())
        self.assertEqual(2.2046226218487757, unit2)
                        
    def test_convert_kg_to_tonne(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Kilogram(), Tonne())
        self.assertEqual(1, unit2)
        
    def test_convert_gram_to_kg(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Gram(), Kilogram())
        self.assertEqual(1, unit2)
        
    def test_convert_gram_to_gram(self):
        unit2 = Converter.ConvertUnitToUnit(1, Gram(), Gram())
        self.assertEqual(1, unit2)
        
    def test_convert_gram_to_slug(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Gram(), Slug())
        self.assertEqual(0.06852176603148429, unit2)

    def test_convert_gram_to_mgram(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Gram(), Milligram())
        self.assertEqual(1, unit2)
        
    def test_convert_gram_to_oz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Gram(), Ounce())
        self.assertEqual(0.035273961980686726, unit2)
        
    def test_convert_gram_to_lb(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Gram(), Pound())
        self.assertEqual(2.2046226218487757, unit2)
        
    def test_convert_gram_to_tonne(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Gram(), Tonne())
        self.assertEqual(0.001, unit2)

    def test_convert_slug_to_kg(self):
        unit2 = Converter.ConvertUnitToUnit(1, Slug(), Kilogram())
        self.assertEqual(14.5939029, unit2)
        
    def test_convert_slug_to_gram(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Slug(), Gram())
        self.assertEqual(14.5939029, unit2)
        
    def test_convert_slug_to_slug(self):
        unit2 = Converter.ConvertUnitToUnit(1, Slug(), Slug())
        self.assertEqual(1, unit2)

    def test_convert_slug_to_mgram(self):
        unit2 = Converter.ConvertUnitToUnit(.000001, Slug(), Milligram())
        self.assertEqual(14.5939029, unit2)

    def test_convert_slug_to_oz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Slug(), Ounce())
        self.assertEqual(514.7847760444337, unit2)
        
    def test_convert_slug_to_lb(self):
        unit2 = Converter.ConvertUnitToUnit(1, Slug(), Pound())
        self.assertEqual(32.17404847440445, unit2)
        
    def test_convert_slug_to_tonne(self):
        unit2 = Converter.ConvertUnitToUnit(1, Slug(), Tonne())
        self.assertEqual(0.0145939029, unit2)
        
    def test_convert_mgram_to_kg(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Milligram(), Kilogram())
        self.assertEqual(1, unit2)

    def test_convert_mgram_to_gram(self):
        unit2 = Converter.ConvertUnitToUnit(1, Milligram(), Gram())
        self.assertEqual(0.001, unit2)
        
    def test_convert_mgram_to_slug(self):
        unit2 = Converter.ConvertUnitToUnit(1000000000, Milligram(), Slug())
        self.assertEqual(68.52176603148429, unit2)
        
    def test_convert_mgram_to_mgram(self):
        unit2 = Converter.ConvertUnitToUnit(1, Milligram(), Milligram())
        self.assertEqual(1, unit2)
        
    def test_convert_mgram_to_oz(self):
        unit2 = Converter.ConvertUnitToUnit(100000, Milligram(), Ounce())
        self.assertEqual(3.527396198068672, unit2)

    def test_convert_mgram_to_lb(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Milligram(), Pound())
        self.assertEqual(2.2046226218487757, unit2)
        
    def test_convert_mgram_to_tonne(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Milligram(), Tonne())
        self.assertEqual(0.001, unit2)
        
    def test_convert_oz_to_kg(self):
        unit2 = Converter.ConvertUnitToUnit(1, Ounce(), Kilogram())
        self.assertEqual(0.0283495231, unit2)
        
    def test_convert_oz_to_gram(self):
        unit2 = Converter.ConvertUnitToUnit(1, Ounce(), Gram())
        self.assertEqual(28.3495231, unit2)

    def test_convert_oz_to_slug(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Ounce(), Slug())
        self.assertEqual(1.9425593889623591, unit2)
        
    def test_convert_oz_to_mgram(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Ounce(), Milligram())
        self.assertEqual(28.349523100000003, unit2)
        
    def test_convert_oz_to_oz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Ounce(), Ounce())
        self.assertEqual(1, unit2)

    def test_convert_oz_to_lb(self):
        unit2 = Converter.ConvertUnitToUnit(1, Ounce(), Pound())
        self.assertEqual(0.06249999994488443, unit2)

    def test_convert_oz_to_tonne(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Ounce(), Tonne())
        self.assertEqual(0.0283495231, unit2)
        
    def test_convert_lb_to_kg(self):
        unit2 = Converter.ConvertUnitToUnit(1, Pound(), Kilogram())
        self.assertEqual(0.45359237, unit2)
        
    def test_convert_lb_to_gram(self):
        unit2 = Converter.ConvertUnitToUnit(1, Pound(), Gram())
        self.assertEqual(453.59237, unit2)
        
    def test_convert_lb_to_slug(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Pound(), Slug())
        self.assertEqual(31.080950250806453, unit2)

    def test_convert_lb_to_mgram(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Pound(), Milligram())
        self.assertEqual(453.5923700000001, unit2)
        
    def test_convert_lb_to_oz(self):
        unit2 = Converter.ConvertUnitToUnit(1, Pound(), Ounce())
        self.assertEqual(16.000000014109585, unit2)
        
    def test_convert_lb_to_lb(self):
        unit2 = Converter.ConvertUnitToUnit(1, Pound(), Pound())
        self.assertEqual(1, unit2)
        
    def test_convert_lb_to_tonne(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Pound(), Tonne())
        self.assertEqual(0.45359237, unit2)

    def test_convert_tonne_to_kg(self):
        unit2 = Converter.ConvertUnitToUnit(1, Tonne(), Kilogram())
        self.assertEqual(1000, unit2)
        
    def test_convert_tonne_to_gram(self):
        unit2 = Converter.ConvertUnitToUnit(1, Tonne(), Gram())
        self.assertEqual(1000000, unit2)
        
    def test_convert_tonne_to_slug(self):
        unit2 = Converter.ConvertUnitToUnit(1, Tonne(), Slug())
        self.assertEqual(68.52176603148429, unit2)
        
    def test_convert_tonne_to_mgram(self):
        unit2 = Converter.ConvertUnitToUnit(1, Tonne(), Milligram())
        self.assertEqual(1000000000, unit2)

    def test_convert_tonne_to_oz(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Tonne(), Ounce())
        self.assertEqual(35.27396198068672, unit2)
        
    def test_convert_tonne_to_lb(self):
        unit2 = Converter.ConvertUnitToUnit(1, Tonne(), Pound())
        self.assertEqual(2204.622621848776, unit2)
        
    def test_convert_tonne_to_tonne(self):
        unit2 = Converter.ConvertUnitToUnit(1, Tonne(), Tonne())
        self.assertEqual(1, unit2)




if __name__ == "__main__":
    unittest.main()
