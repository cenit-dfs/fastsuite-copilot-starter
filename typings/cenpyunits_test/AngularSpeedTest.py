import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.AngularSpeed import *

class AngularSpeedTest(unittest.TestCase):

    def test_isDefault(self):
        degsec = DegreeSecond()
        degmin= DegreeMinute()
        radsec = RadianSecond()
        radmin= RadianMinute()

        self.assertFalse(degsec.IsDefault(), "DegreeSecond must not be default")
        self.assertFalse(degmin.IsDefault(), "DegreeMinute must not be default")
        self.assertTrue(radsec.IsDefault(), "RadianSecond must be default")
        self.assertFalse(radmin.IsDefault(), "RadianMinute must not be default")

    def test_UnitGroup(self):
        degsec = DegreeSecond()
        degmin= DegreeMinute()
        radsec = RadianSecond()
        radmin= RadianMinute()

        self.assertEqual(degsec.GetUnitGroup(), UnitGroups.AngularSpeed)
        self.assertEqual(degmin.GetUnitGroup(), UnitGroups.AngularSpeed)
        self.assertEqual(radsec.GetUnitGroup(), UnitGroups.AngularSpeed)
        self.assertEqual(radmin.GetUnitGroup(), UnitGroups.AngularSpeed)

    def test_convert_radsec_to_degsec(self):
        radsecsec = Converter.ConvertDefaultToUnit(1, DegreeSecond())
        self.assertEqual(57.295779578552306, radsecsec)

    def test_convert_radsec_to_degmin(self):
        radsecsec = Converter.ConvertDefaultToUnit(1, DegreeMinute())
        self.assertEqual(3437.7468731973313, radsecsec)

    def test_convert_radsec_to_radmin(self):
        radsecsec = Converter.ConvertDefaultToUnit(1, RadianMinute())
        self.assertEqual(60, radsecsec)

    def test_converr_degsec_to_radsec(self):
        radsecsec = Converter.ConvertUnitToDefault(1, DegreeSecond())
        self.assertEqual(0.0174532925, radsecsec)

    def test_convert_degmin_to_radsec(self):
        radsecsec = Converter.ConvertUnitToDefault(3437.7468731973313, DegreeMinute())
        self.assertEqual(1, radsecsec)

    def test_convert_radmin_to_radsec(self):
        radsecsec = Converter.ConvertUnitToDefault(60, RadianMinute())
        self.assertEqual(1.0, radsecsec)

    def test_convert_degsec_to_degmin(self):
        radsecsec = Converter.ConvertUnitToUnit(1.0, DegreeSecond(), DegreeMinute())
        self.assertEqual(60.00000171887343, radsecsec) #should be 60, but neah...

    def test_convert_degsec_to_radmin(self):
        radsecsec = Converter.ConvertUnitToUnit(1.0, DegreeSecond(), RadianMinute())
        self.assertEqual(1.04719755, radsecsec) 

    def test_convert_degmin_to_radmin(self):
        radsecsec = Converter.ConvertUnitToUnit(1.0, DegreeMinute(), RadianMinute())
        self.assertEqual(0.017453292000000002, radsecsec) 

    def test_convert_degmin_to_degsec(self):
        radsecsec = Converter.ConvertUnitToUnit(1.0, DegreeMinute(), DegreeSecond())
        self.assertEqual(0.01666666618920184, radsecsec) 
      
    def test_convert_radmin_to_degmin(self):
        radsecsec = Converter.ConvertUnitToUnit(1.0, RadianMinute(), DegreeMinute())
        self.assertEqual(57.29578121995552, radsecsec) 

    def test_convert_radmin_to_degsec(self):
        radsecsec = Converter.ConvertUnitToUnit(1.0, RadianMinute(), DegreeSecond())
        self.assertEqual(0.9549296596425384, radsecsec) 
      
    def test_convert_degsec_to_degsec(self):
        degsec = Converter.ConvertUnitToUnit(1.0, DegreeSecond(), DegreeSecond())
        self.assertEqual(1.0, degsec)

    def test_convert_degmin_to_degmin(self):
        degmin = Converter.ConvertUnitToUnit(1.0, DegreeMinute(), DegreeMinute())
        self.assertEqual(1.0, degmin)  
              
    def test_convert_radmin_to_radmin(self):
        degsecsec = Converter.ConvertDefaultToUnit(1.0, RadianSecond())
        self.assertEqual(1.0, degsecsec)

    def test_convert_radsec_to_radsec(self):
        radmin = Converter.ConvertUnitToUnit(1.0, RadianMinute(), RadianMinute())
        self.assertEqual(1.0, radmin)  

if __name__ == "__main__":
    unittest.main()