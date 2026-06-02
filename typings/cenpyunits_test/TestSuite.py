import unittest
import sys, os, inspect
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from cenpyunits_test.AccelerationTest import *
from cenpyunits_test.AngleTest import *
from cenpyunits_test.AngularAccelerationTest import *
from cenpyunits_test.AngularSpeedTest import *
from cenpyunits_test.AreaTest import *
from cenpyunits_test.DensityTest import *
from cenpyunits_test.ElectricCapacityTest import *
from cenpyunits_test.ElectricChargeTest import *
from cenpyunits_test.ElectricCurrentTest import *
from cenpyunits_test.ElectricResistTest import *
from cenpyunits_test.EnergyTest import *
from cenpyunits_test.FlowRateTest import *
from cenpyunits_test.ForceTest import *
from cenpyunits_test.FrequencyTest import *
from cenpyunits_test.InductionTest import *
from cenpyunits_test.LengthTest import *
from cenpyunits_test.LuminanceTest import *
from cenpyunits_test.LuminousIntensityTest import *
from cenpyunits_test.MagneticFieldTest import *
from cenpyunits_test.MagneticFluxTest import *
from cenpyunits_test.MassTest import *
from cenpyunits_test.PercentTest import *
from cenpyunits_test.PowerTest import *
from cenpyunits_test.PressureTest import *
from cenpyunits_test.SpeedTest import *
from cenpyunits_test.StandardTest import *
from cenpyunits_test.TemperatureTest import *
from cenpyunits_test.TimeTest import *
from cenpyunits_test.VoltageTest import *
from cenpyunits_test.VolumeTest import *


def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    test_suite.addTests(test_loader.loadTestsFromTestCase(AccelerationTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(AngleTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(AngularAccelerationTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(AngularSpeedTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(AreaTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(DensityTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(ElectricCapacityTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(ElectricChargeTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(ElectricCurrentTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(ElectricResistTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(EnergyTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(FlowRateTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(ForceTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(FrequencyTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(InductionTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(LengthTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(LuminanceTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(LuminousIntensityTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(MagneticFieldTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(MagneticFluxTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(MassTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(PercentTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(PowerTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(PressureTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(SpeedTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(StandardTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TemperatureTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TimeTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(VoltageTest))
    test_suite.addTests(test_loader.loadTestsFromTestCase(VolumeTest))
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())