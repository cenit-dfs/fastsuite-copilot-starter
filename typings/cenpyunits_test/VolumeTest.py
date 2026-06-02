import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Volume import *

class VolumeTest(unittest.TestCase):
 
    def test_isDefault(self):
        qft = Cubicfoot()
        qin= Cubicinch()
        qmm = Cubicmillimeter()
        qm = Cubicmeter()

        self.assertFalse(qft.IsDefault(), "Cubicfoot must not be default")
        self.assertFalse(qin.IsDefault(), "Cubicinch must not be default")
        self.assertFalse(qmm.IsDefault(), "Cubicmillimeter must not be default")
        self.assertTrue(qm.IsDefault(), "Cubicmeter must be default")

    def test_UnitGroup(self):
        qft = Cubicfoot()
        qin= Cubicinch()
        qmm = Cubicmillimeter()
        qm = Cubicmeter()

        self.assertEqual(qft.GetUnitGroup(), UnitGroups.Volume)
        self.assertEqual(qin.GetUnitGroup(), UnitGroups.Volume)
        self.assertEqual(qmm.GetUnitGroup(), UnitGroups.Volume)
        self.assertEqual(qm.GetUnitGroup(), UnitGroups.Volume)

    def test_convert_qmm_to_qft(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Cubicmillimeter(), Cubicfoot())
        self.assertEqual(0.03531466995403866, unit2)

    def test_convert_qmm_to_qin(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Cubicmillimeter(), Cubicinch())
        self.assertEqual(61.02398242509306, unit2)

    def test_convert_qmm_to_qm(self):
        unit2 = Converter.ConvertUnitToUnit(1000000, Cubicmillimeter(), Cubicmeter())
        self.assertEqual(0.001, unit2)

    def test_converr_qft_to_qmm(self):
        unit2 = Converter.ConvertUnitToUnit(0.000001, Cubicfoot(), Cubicmillimeter())
        self.assertEqual(28.316843999999996, unit2)

    def test_convert_qin_to_qmm(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Cubicinch(), Cubicmillimeter())
        self.assertEqual(16.387, unit2)

    def test_convert_qm_to_qmm(self):
        unit2 = Converter.ConvertUnitToUnit(0.00001, Cubicmeter(), Cubicmillimeter())
        self.assertEqual(10000, unit2)

    def test_convert_qft_to_qin(self):
        unit2 = Converter.ConvertUnitToUnit(1, Cubicfoot(), Cubicinch())
        self.assertEqual(1728.006590590102, unit2)

    def test_convert_qft_to_qm(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Cubicfoot(), Cubicmeter())
        self.assertEqual(28.316844, unit2)

    def test_convert_qin_to_qm(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Cubicinch(), Cubicmeter())
        self.assertEqual(0.016387000000000002, unit2)

    def test_convert_qin_to_qft(self):
        unit2 = Converter.ConvertUnitToUnit(1000, Cubicinch(), Cubicfoot())
        self.assertEqual(0.5787014965368317, unit2)
      
    def test_convert_qm_to_qin(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, Cubicmeter(), Cubicinch())
        self.assertEqual(61.02398242509306, unit2)

    def test_convert_qm_to_qft(self):
        unit2 = Converter.ConvertUnitToUnit(1, Cubicmeter(), Cubicfoot())
        self.assertEqual(35.31466995403866, unit2)
      
    def test_convert_qft_to_qft(self):
        unit2 = Converter.ConvertUnitToUnit(1, Cubicfoot(), Cubicfoot())
        self.assertEqual(1, unit2)

    def test_convert_qin_to_qin(self):
        unit2 = Converter.ConvertUnitToUnit(1, Cubicinch(), Cubicinch())
        self.assertEqual(1, unit2)
              
    def test_convert_qm_to_qm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Cubicmeter(), Cubicmeter())
        self.assertEqual(1, unit2)

    def test_convert_qmm_to_qmm(self):
        unit2 = Converter.ConvertUnitToUnit(1, Cubicmillimeter(), Cubicmillimeter())
        self.assertEqual(1, unit2)

if __name__ == "__main__":
    unittest.main()