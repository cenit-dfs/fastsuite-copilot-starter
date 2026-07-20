from cenpylib import *
from centypes import *


PROC_GEO_NAME = "ProcGeoName"
HAS_SPEED = "Has_Speed"
SPEED = "Speed"
HAS_WAIT = "Has_Wait"
WAIT = "Wait"


def PostWmInitAttributes(Operator: CENPyOlpWM_AttribInitOperator):
    creator = Operator.GetAttribCreator()
    use_level = USER_ATTRIBUTE | PROCESS_ATTRIBUTE | OPERATION_ATTRIBUTE

    proc_geo_name = creator.AddString(PROC_GEO_NAME, "", use_level, PROC_GEO_NAME)
    proc_geo_name.SetReadOnly(True)

    has_speed = creator.AddBool(HAS_SPEED, False, use_level, HAS_SPEED)
    has_speed.SetReadOnly(True)
    speed = creator.AddDouble(SPEED, 0.0, 0.0, 10.0, 0.01,
                              use_level, ATTRIB_SPEED, SPEED)
    speed.SetReadOnly(True)

    has_wait = creator.AddBool(HAS_WAIT, False, use_level, HAS_WAIT)
    has_wait.SetReadOnly(True)
    wait = creator.AddDouble(WAIT, 0.0, 0.0, 999.0, 0.01,
                             use_level, ATTRIB_TIME, WAIT)
    wait.SetReadOnly(True)


def PostWmSyncPgAttributes(Operator: CENPyOlpWM_SyncPgAttribOperator):
    setter = Operator.GetAttribSetter()
    geometry = Operator.GetCurrentProcessGeometryOperator()

    has_speed = geometry.GetBool(HAS_SPEED)
    has_wait = geometry.GetBool(HAS_WAIT)

    setter.SetString(PROC_GEO_NAME, geometry.GetProcessGeometryName(), False)
    setter.SetBool(HAS_SPEED, has_speed, False)
    setter.SetDouble(SPEED, geometry.GetDouble(SPEED) if has_speed else 0.0, False)
    setter.SetBool(HAS_WAIT, has_wait, False)
    setter.SetDouble(WAIT, geometry.GetDouble(WAIT) if has_wait else 0.0, False)
