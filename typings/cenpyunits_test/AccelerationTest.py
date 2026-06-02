import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Acceleration import *

class AccelerationTest(unittest.TestCase):

    def test_isDefault(self):
        fss = FootSecondSecond()
        iss = InchSecondSecond()
        mss = MeterSecondSecond()
        mmss = MillimeterSecondSecond()

        self.assertTrue(mss.IsDefault(), "MeterSecondSecond must be default")
        self.assertFalse(fss.IsDefault(), "FootSecondSecond must not be default")
        self.assertFalse(iss.IsDefault(), "InchSecondSecond must not be default")
        self.assertFalse(mmss.IsDefault(), "MillimeterSecondSecond must not be default")

    def test_UnitGroup(self):
        fss = FootSecondSecond()
        iss = InchSecondSecond()
        mss = MeterSecondSecond()
        mmss = MillimeterSecondSecond()

        self.assertEqual(fss.GetUnitGroup(), UnitGroups.Acceleration)
        self.assertEqual(iss.GetUnitGroup(), UnitGroups.Acceleration)
        self.assertEqual(mss.GetUnitGroup(), UnitGroups.Acceleration)
        self.assertEqual(mmss.GetUnitGroup(), UnitGroups.Acceleration)

    def test_convert_mss_to_mmss(self):        
        mmss = Converter.ConvertDefaultToUnit(1.0, MillimeterSecondSecond())
        self.assertEqual(1000.0, mmss)

    def test_convert_mmss_to_mss(self):        
        mss = Converter.ConvertUnitToDefault(1000.0, MillimeterSecondSecond())
        self.assertEqual(1.0, mss)
      
    def test_convert_mss_to_iss(self):        
        iss = Converter.ConvertDefaultToUnit(1.0, InchSecondSecond())
        self.assertEqual(39.37007874015748, iss)

    def test_convert_iss_to_mss(self):        
        mss = Converter.ConvertUnitToDefault(39.37007874015748, InchSecondSecond())
        self.assertEqual(1.0, mss)  
        
    def test_convert_mss_to_fss(self):        
        fss = Converter.ConvertDefaultToUnit(1.0, FootSecondSecond())
        self.assertEqual(3.2808400000000035, fss)

    def test_convert_fss_to_mss(self):        
        mss = Converter.ConvertUnitToDefault(3.2808400000000035, FootSecondSecond())
        self.assertEqual(1.0, mss)
        
    def test_convert_mss_to_mss(self):        
        mss = Converter.ConvertDefaultToUnit(1.0, MeterSecondSecond())
        self.assertEqual(1.0, mss)

    def test_convert_fss_to_fss(self):        
        fss = Converter.ConvertUnitToUnit(1.0, FootSecondSecond(), FootSecondSecond())
        self.assertEqual(1.0, fss)
        
    def test_convert_iss_to_iss(self):        
        iss = Converter.ConvertUnitToUnit(1.0, InchSecondSecond(), InchSecondSecond())
        self.assertEqual(1.0, iss)
        
    def test_convert_mmss_to_mmss(self):        
        mmss = Converter.ConvertUnitToUnit(1.0, MillimeterSecondSecond(), MillimeterSecondSecond())
        self.assertEqual(1.0, mmss)


if __name__ == "__main__":
    unittest.main()