import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.LuminousIntensity import *

class LuminousIntensityTest(unittest.TestCase):

    def test_isDefault(self):
        candela = Candela()
        self.assertTrue(candela.IsDefault(), "Candelapersquaremeter must be default")

    def test_UnitGroup(self):
        candela = Candela()
        self.assertEqual(candela.GetUnitGroup(), UnitGroups.LuminousIntensity)

    def test_convert_candela_to_candela(self):
        unit2 = Converter.ConvertUnitToUnit(1, Candela(), Candela())
        self.assertEqual(1, unit2)
        
if __name__ == "__main__":
    unittest.main()
