from cenpylib import *
from centypes import *


FILE_NAME = "PointWorkMethod.py: "


def PostWmInitEvents(Operator: CENPyOlpWM_EventInitOperator):
    Operator.RegisterPyTechnologyEvent("FourPointApproach.py")
    Operator.RegisterPyTechnologyEvent("SkipEvent.py")


def PostWmInitRules(Operator: CENPyOlpWM_RuleInitOperator):
    Operator.AddPyEvent("ApproachRule", "FourPointApproach")
    Operator.SetActivePyEvent("ApproachRule", "FourPointApproach")
