import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Standard import *

class StandardTest(unittest.TestCase):

    def test_isDefault(self):
        standard = Standard()
        self.assertTrue(standard.IsDefault(), "Candelapersquaremeter must be default")

    def test_UnitGroup(self):
        standard = Standard()
        self.assertEqual(standard.GetUnitGroup(), UnitGroups.Standard)

    def test_convert_standard_to_standard(self):
        unit2 = Converter.ConvertUnitToUnit(1, Standard(), Standard())
        self.assertEqual(1, unit2)
        
if __name__ == "__main__":
    unittest.main()
