import unittest
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from cenpyunits import Converter
from cenpyunits.Speed import *

class SpeedTest(unittest.TestCase):


    def test_isDefault(self):
        kilomh = KilometerHour()
        mms = MillimeterSecond()
        ms = MeterSecond()
        millimetm = MillimeterMinute()
        meterm = MeterMinute()
        ins = InchSecond()
        ftps = FeetSecond()
        mph = MileHour()
        ipm = InchMinute()
        tpm = FeetMinute()

        self.assertFalse(kilomh.IsDefault(), "KilometerHour must not be default")
        self.assertFalse(mms.IsDefault(), "MillimeterSecond must not be default")
        self.assertTrue(ms.IsDefault(), "MeterSecond must be default")
        self.assertFalse(millimetm.IsDefault(), "MillimeterMinute must not be default")
        self.assertFalse(meterm.IsDefault(), "MeterMinute must not be default")
        self.assertFalse(ins.IsDefault(), "InchSecond must not be default")
        self.assertFalse(ftps.IsDefault(), "FeetSecond must not be default")
        self.assertFalse(mph.IsDefault(), "MileHour must not be default")
        self.assertFalse(ipm.IsDefault(), "InchMinute must not be default")
        self.assertFalse(tpm.IsDefault(), "FeetMinute must not be default")

    def test_UnitGroup(self):
        kilomh = KilometerHour()
        mms = MillimeterSecond()
        ms = MeterSecond()
        millimetm = MillimeterMinute()
        meterm = MeterMinute()
        ins = InchSecond()
        ftps = FeetSecond()
        mph = MileHour()
        ipm = InchMinute()
        tpm = FeetMinute()

        self.assertEqual(kilomh.GetUnitGroup(), UnitGroups.Speed)
        self.assertEqual(mms.GetUnitGroup(), UnitGroups.Speed)
        self.assertEqual(ms.GetUnitGroup(), UnitGroups.Speed)
        self.assertEqual(millimetm.GetUnitGroup(), UnitGroups.Speed)
        self.assertEqual(meterm.GetUnitGroup(), UnitGroups.Speed)
        self.assertEqual(ins.GetUnitGroup(), UnitGroups.Speed)
        self.assertEqual(ftps.GetUnitGroup(), UnitGroups.Speed)
        self.assertEqual(mph.GetUnitGroup(), UnitGroups.Speed)
        self.assertEqual(ipm.GetUnitGroup(), UnitGroups.Speed)
        self.assertEqual(tpm.GetUnitGroup(), UnitGroups.Speed)

        
    def test_convert_kilomh_to_kilomh(self):
        unit2 = Converter.ConvertUnitToUnit(1, KilometerHour(), KilometerHour())
        self.assertEqual(1, unit2)
        
    def test_convert_kilomh_to_mms(self):
        unit2 = Converter.ConvertUnitToUnit(1, KilometerHour(), MillimeterSecond())
        self.assertEqual(277.77777777778, unit2)
        
    def test_convert_kilomh_to_ms(self):
        unit2 = Converter.ConvertUnitToUnit(1, KilometerHour(), MeterSecond())
        self.assertEqual(0.27777777777778, unit2)
        
    def test_convert_kilomh_to_millimetm(self):
        unit2 = Converter.ConvertUnitToUnit(0.0001, KilometerHour(), MillimeterMinute())
        self.assertEqual(1.666666666333347, unit2)
        
    def test_convert_kilomh_to_meterm(self):
        unit2 = Converter.ConvertUnitToUnit(1, KilometerHour(), MeterMinute())
        self.assertEqual(16.666666666663467, unit2)
        
    def test_convert_kilomh_to_ins(self):
        unit2 = Converter.ConvertUnitToUnit(1, KilometerHour(), InchSecond())
        self.assertEqual(10.936132983377167, unit2)
        
    def test_convert_kilomh_to_ftps(self):
        unit2 = Converter.ConvertUnitToUnit(1, KilometerHour(), FeetSecond())
        self.assertEqual(0.9113444444444527, unit2)
        
    def test_convert_kilomh_to_mph(self):
        unit2 = Converter.ConvertUnitToUnit(1, KilometerHour(), MileHour())
        self.assertEqual(0.6213711922373389, unit2)
        
    def test_convert_kilomh_to_ipm(self):
        unit2 = Converter.ConvertUnitToUnit(1, KilometerHour(), InchMinute())
        self.assertEqual(656.1679790542968, unit2)
        
    def test_convert_kilomh_to_tpm(self):
        unit2 = Converter.ConvertUnitToUnit(1, KilometerHour(), FeetMinute())
        self.assertEqual(54.680664916885824, unit2)
        

    def test_convert_mms_to_kilomh(self):
        unit2 = Converter.ConvertUnitToUnit(1000, MillimeterSecond(), KilometerHour())
        self.assertEqual(3.5999999999999712, unit2)
        
    def test_convert_mms_to_mms(self):
        unit2 = Converter.ConvertUnitToUnit(1, MillimeterSecond(), MillimeterSecond())
        self.assertEqual(1, unit2)
        
    def test_convert_mms_to_ms(self):
        unit2 = Converter.ConvertUnitToUnit(1000, MillimeterSecond(), MeterSecond())
        self.assertEqual(1, unit2)
        
    def test_convert_mms_to_millimetm(self):
        unit2 = Converter.ConvertUnitToUnit(10, MillimeterSecond(), MillimeterMinute())
        self.assertEqual(599.99999988, unit2)
        
    def test_convert_mms_to_meterm(self):
        unit2 = Converter.ConvertUnitToUnit(1, MillimeterSecond(), MeterMinute())
        self.assertEqual(0.059999999999988, unit2)
        
    def test_convert_mms_to_ins(self):
        unit2 = Converter.ConvertUnitToUnit(1000, MillimeterSecond(), InchSecond())
        self.assertEqual(39.37007874015748, unit2)
        
    def test_convert_mms_to_ftps(self):
        unit2 = Converter.ConvertUnitToUnit(1000, MillimeterSecond(), FeetSecond())
        self.assertEqual(3.2808400000000035, unit2)
        
    def test_convert_mms_to_mph(self):
        unit2 = Converter.ConvertUnitToUnit(1000, MillimeterSecond(), MileHour())
        self.assertEqual(2.2369362920544025, unit2)
        
    def test_convert_mms_to_ipm(self):
        unit2 = Converter.ConvertUnitToUnit(1000, MillimeterSecond(), InchMinute())
        self.assertEqual( 2362.204724595449, unit2)
        
    def test_convert_mms_to_tpm(self):
        unit2 = Converter.ConvertUnitToUnit(1000, MillimeterSecond(), FeetMinute())
        self.assertEqual(196.85039370078738, unit2)
        

    def test_convert_ms_to_kilomh(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterSecond(), KilometerHour())
        self.assertEqual(3.5999999999999712, unit2)
        
    def test_convert_ms_to_mms(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterSecond(), MillimeterSecond())
        self.assertEqual(1000, unit2)
        
    def test_convert_ms_to_ms(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterSecond(), MeterSecond())
        self.assertEqual(1, unit2)
        
    def test_convert_ms_to_millimetm(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, MeterSecond(), MillimeterMinute())
        self.assertEqual(59.999999988000006, unit2)
        
    def test_convert_ms_to_meterm(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterSecond(), MeterMinute())
        self.assertEqual(59.999999999988, unit2)
        
    def test_convert_ms_to_ins(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterSecond(), InchSecond())
        self.assertEqual(39.37007874015748, unit2)
        
    def test_convert_ms_to_ftps(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterSecond(), FeetSecond())
        self.assertEqual(3.2808400000000035, unit2)
        
    def test_convert_ms_to_mph(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterSecond(), MileHour())
        self.assertEqual(2.2369362920544025, unit2)
        
    def test_convert_ms_to_ipm(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterSecond(), InchMinute())
        self.assertEqual(2362.204724595449, unit2)
        
    def test_convert_ms_to_tpm(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterSecond(), FeetMinute())
        self.assertEqual(196.85039370078738, unit2)
        


    def test_convert_millimetm_to_kilomh(self):
        unit2 = Converter.ConvertUnitToUnit(1000, MillimeterMinute(), KilometerHour())
        self.assertEqual(0.06000000001199952, unit2)
        
    def test_convert_millimetm_to_mms(self):
        unit2 = Converter.ConvertUnitToUnit(1, MillimeterMinute(), MillimeterSecond())
        self.assertEqual(0.01666666667, unit2)
        
    def test_convert_millimetm_to_ms(self):
        unit2 = Converter.ConvertUnitToUnit(100, MillimeterMinute(), MeterSecond())
        self.assertEqual(0.001666666667, unit2)
        
    def test_convert_millimetm_to_millimetm(self):
        unit2 = Converter.ConvertUnitToUnit(1, MillimeterMinute(), MillimeterMinute())
        self.assertEqual(1, unit2)
        
    def test_convert_millimetm_to_meterm(self):
        unit2 = Converter.ConvertUnitToUnit(1000, MillimeterMinute(), MeterMinute())
        self.assertEqual(1.0000000001998, unit2)
        
    def test_convert_millimetm_to_ins(self):
        unit2 = Converter.ConvertUnitToUnit(100, MillimeterMinute(), InchSecond())
        self.assertEqual(0.06561679791338583, unit2)
        
    def test_convert_millimetm_to_ftps(self):
        unit2 = Converter.ConvertUnitToUnit(1000, MillimeterMinute(), FeetSecond())
        self.assertEqual(0.05468066667760286, unit2)
        
    def test_convert_millimetm_to_mph(self):
        unit2 = Converter.ConvertUnitToUnit(1000, MillimeterMinute(), MileHour())
        self.assertEqual(0.03728227154169649, unit2)
        
    def test_convert_millimetm_to_ipm(self):
        unit2 = Converter.ConvertUnitToUnit(1, MillimeterMinute(), InchMinute())
        self.assertEqual(0.0393700787511315, unit2)
        
    def test_convert_millimetm_to_tpm(self):
        unit2 = Converter.ConvertUnitToUnit(100, MillimeterMinute(), FeetMinute())
        self.assertEqual(0.3280839895669291, unit2)




    def test_convert_meterm_to_kilomh(self):
        unit2 = Converter.ConvertUnitToUnit(100, MeterMinute(), KilometerHour())
        self.assertEqual(6.000000000001152, unit2)
        
    def test_convert_meterm_to_mms(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterMinute(), MillimeterSecond())
        self.assertEqual(16.66666666667, unit2)
        
    def test_convert_meterm_to_ms(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterMinute(), MeterSecond())
        self.assertEqual(0.01666666666667, unit2)
        
    def test_convert_meterm_to_millimetm(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterMinute(), MillimeterMinute())
        self.assertEqual(999.9999998002, unit2)
        
    def test_convert_meterm_to_meterm(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterMinute(), MeterMinute())
        self.assertEqual(1, unit2)
        
    def test_convert_meterm_to_ins(self):
        unit2 = Converter.ConvertUnitToUnit(100, MeterMinute(), InchSecond())
        self.assertEqual(65.6167979002756, unit2)
        
    def test_convert_meterm_to_ftps(self):
        unit2 = Converter.ConvertUnitToUnit(100, MeterMinute(), FeetSecond())
        self.assertEqual(5.468066666667767, unit2)
        
    def test_convert_meterm_to_mph(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterMinute(), MileHour())
        self.assertEqual(0.0372822715342475, unit2)
        
    def test_convert_meterm_to_ipm(self):
        unit2 = Converter.ConvertUnitToUnit(1, MeterMinute(), InchMinute())
        self.assertEqual(39.37007874326537, unit2)
        
    def test_convert_meterm_to_tpm(self):
        unit2 = Converter.ConvertUnitToUnit(10, MeterMinute(), FeetMinute())
        self.assertEqual(32.80839895013779, unit2)



    def test_convert_ins_to_kilomh(self):
        unit2 = Converter.ConvertUnitToUnit(1000, InchSecond(), KilometerHour())
        self.assertEqual(91.43999999999926, unit2)
        
    def test_convert_ins_to_mms(self):
        unit2 = Converter.ConvertUnitToUnit(100, InchSecond(), MillimeterSecond())
        self.assertEqual(2540.0, unit2)
        
    def test_convert_ins_to_ms(self):
        unit2 = Converter.ConvertUnitToUnit(1, InchSecond(), MeterSecond())
        self.assertEqual(0.0254, unit2)
        
    def test_convert_ins_to_millimetm(self):
        unit2 = Converter.ConvertUnitToUnit(1, InchSecond(), MillimeterMinute())
        self.assertEqual(1523.9999996952, unit2)
        
    def test_convert_ins_to_meterm(self):
        unit2 = Converter.ConvertUnitToUnit(1, InchSecond(), MeterMinute())
        self.assertEqual(1.5239999999996952, unit2)
        
    def test_convert_ins_to_ins(self):
        unit2 = Converter.ConvertUnitToUnit(1, InchSecond(), InchSecond())
        self.assertEqual(1, unit2)
        
    def test_convert_ins_to_ftps(self):
        unit2 = Converter.ConvertUnitToUnit(100, InchSecond(), FeetSecond())
        self.assertEqual(8.333333600000008, unit2)
        
    def test_convert_ins_to_mph(self):
        unit2 = Converter.ConvertUnitToUnit(1000, InchSecond(), MileHour())
        self.assertEqual(56.81818181818181, unit2)
        
    def test_convert_ins_to_ipm(self):
        unit2 = Converter.ConvertUnitToUnit(1, InchSecond(), InchMinute())
        self.assertEqual(60.00000000472441, unit2)
        
    def test_convert_ins_to_tpm(self):
        unit2 = Converter.ConvertUnitToUnit(1, InchSecond(), FeetMinute())
        self.assertEqual(4.999999999999999, unit2)




    def test_convert_ftps_to_kilomh(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetSecond(), KilometerHour())
        self.assertEqual(1.097279964887031, unit2)
        
    def test_convert_ftps_to_mms(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetSecond(), MillimeterSecond())
        self.assertEqual(304.79999024639994, unit2)
        
    def test_convert_ftps_to_ms(self):
        unit2 = Converter.ConvertUnitToUnit(100, FeetSecond(), MeterSecond())
        self.assertEqual(30.479999024639998, unit2)
        
    def test_convert_ftps_to_millimetm(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetSecond(), MillimeterMinute())
        self.assertEqual(18287.9994111264, unit2)
        
    def test_convert_ftps_to_meterm(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetSecond(), MeterMinute())
        self.assertEqual(18.28799941478034, unit2)
        
    def test_convert_ftps_to_ins(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetSecond(), InchSecond())
        self.assertEqual(11.999999616, unit2)
        
    def test_convert_ftps_to_ftps(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetSecond(), FeetSecond())
        self.assertEqual(1, unit2)
        
    def test_convert_ftps_to_mph(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetSecond(), MileHour())
        self.assertEqual(0.68181816, unit2)
        
    def test_convert_ftps_to_ipm(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetSecond(), InchMinute())
        self.assertEqual(719.9999770166929, unit2)
        
    def test_convert_ftps_to_tpm(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetSecond(), FeetMinute())
        self.assertEqual(59.99999807999999, unit2)


    def test_convert_mph_to_kilomh(self):
        unit2 = Converter.ConvertUnitToUnit(1, MileHour(), KilometerHour())
        self.assertEqual(1.609343999999987, unit2)
        
    def test_convert_mph_to_mms(self):
        unit2 = Converter.ConvertUnitToUnit(1, MileHour(), MillimeterSecond())
        self.assertEqual(447.03999999999996, unit2)
        
    def test_convert_mph_to_ms(self):
        unit2 = Converter.ConvertUnitToUnit(1, MileHour(), MeterSecond())
        self.assertEqual(0.44704, unit2)
        
    def test_convert_mph_to_millimetm(self):
        unit2 = Converter.ConvertUnitToUnit(0.001, MileHour(), MillimeterMinute())
        self.assertEqual(26.82239999463552, unit2)
        
    def test_convert_mph_to_meterm(self):
        unit2 = Converter.ConvertUnitToUnit(10, MileHour(), MeterMinute())
        self.assertEqual(268.22399999994633, unit2)
        
    def test_convert_mph_to_ins(self):
        unit2 = Converter.ConvertUnitToUnit(1, MileHour(), InchSecond())
        self.assertEqual(17.6, unit2)
        
    def test_convert_mph_to_ftps(self):
        unit2 = Converter.ConvertUnitToUnit(1, MileHour(), FeetSecond())
        self.assertEqual(1.4666667136000016, unit2)
        
    def test_convert_mph_to_mph(self):
        unit2 = Converter.ConvertUnitToUnit(1, MileHour(), MileHour())
        self.assertEqual(1, unit2)
        
    def test_convert_mph_to_ipm(self):
        unit2 = Converter.ConvertUnitToUnit(1, MileHour(), InchMinute())
        self.assertEqual(1056.0000000831496, unit2)
        
    def test_convert_mph_to_tpm(self):
        unit2 = Converter.ConvertUnitToUnit(36, MileHour(), FeetMinute())
        self.assertEqual(3168.0, unit2)
 

    def test_convert_ipm_to_kilomh(self):
        unit2 = Converter.ConvertUnitToUnit(100, InchMinute(), KilometerHour())
        self.assertEqual(0.15239999998799877, unit2)
        
    def test_convert_ipm_to_mms(self):
        unit2 = Converter.ConvertUnitToUnit(1, InchMinute(), MillimeterSecond())
        self.assertEqual(0.42333333329999995, unit2)
        
    def test_convert_ipm_to_ms(self):
        unit2 = Converter.ConvertUnitToUnit(1000, InchMinute(), MeterSecond())
        self.assertEqual(0.4233333333, unit2)
        
    def test_convert_ipm_to_millimetm(self):
        unit2 = Converter.ConvertUnitToUnit(10, InchMinute(), MillimeterMinute())
        self.assertEqual(253.9999999292, unit2)
        
    def test_convert_ipm_to_meterm(self):
        unit2 = Converter.ConvertUnitToUnit(100, InchMinute(), MeterMinute())
        self.assertEqual(2.539999999799492, unit2)
        
    def test_convert_ipm_to_ins(self):
        unit2 = Converter.ConvertUnitToUnit(100, InchMinute(), InchSecond())
        self.assertEqual(1.666666666535433, unit2)
        
    def test_convert_ipm_to_ftps(self):
        unit2 = Converter.ConvertUnitToUnit(100, InchMinute(), FeetSecond())
        self.assertEqual(0.13888889332239734, unit2)
        
    def test_convert_ipm_to_mph(self):
        unit2 = Converter.ConvertUnitToUnit(1000, InchMinute(), MileHour())
        self.assertEqual(0.9469696968951324, unit2)
        
    def test_convert_ipm_to_ipm(self):
        unit2 = Converter.ConvertUnitToUnit(1, InchMinute(), InchMinute())
        self.assertEqual(1, unit2)
        
    def test_convert_ipm_to_tpm(self):
        unit2 = Converter.ConvertUnitToUnit(3, InchMinute(), FeetMinute())
        self.assertEqual(0.24999999998031494, unit2)



    def test_convert_tpm_to_kilomh(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetMinute(), KilometerHour())
        self.assertEqual(0.018287999999999853, unit2)
        
    def test_convert_tpm_to_mms(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetMinute(), MillimeterSecond())
        self.assertEqual(5.08, unit2)
        
    def test_convert_tpm_to_ms(self):
        unit2 = Converter.ConvertUnitToUnit(100, FeetMinute(), MeterSecond())
        self.assertEqual(0.508, unit2)
        
    def test_convert_tpm_to_millimetm(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetMinute(), MillimeterMinute())
        self.assertEqual(304.79999993904005, unit2)
        
    def test_convert_tpm_to_meterm(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetMinute(), MeterMinute())
        self.assertEqual(0.30479999999993906, unit2)
        
    def test_convert_tpm_to_ins(self):
        unit2 = Converter.ConvertUnitToUnit(1000, FeetMinute(), InchSecond())
        self.assertEqual(200, unit2)
        
    def test_convert_tpm_to_ftps(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetMinute(), FeetSecond())
        self.assertEqual(0.01666666720000002, unit2)
        
    def test_convert_tpm_to_mph(self):
        unit2 = Converter.ConvertUnitToUnit(100, FeetMinute(), MileHour())
        self.assertEqual(1.1363636363636365, unit2)
        
    def test_convert_tpm_to_ipm(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetMinute(), InchMinute())
        self.assertEqual(12.000000000944883, unit2)
        
    def test_convert_tpm_to_tpm(self):
        unit2 = Converter.ConvertUnitToUnit(1, FeetMinute(), FeetMinute())
        self.assertEqual(1, unit2)

        
if __name__ == "__main__":
    unittest.main()