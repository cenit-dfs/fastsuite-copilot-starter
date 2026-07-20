from cenpylib import *
from centypes import *


FILE_NAME = "UltrasonicNdtTechnology.py: "


def PostTechInitEvents(Operator: CENPyOlpTech_EventInitOperator):
    Operator.RegisterPyTechnologyEvent("FourPointApproach.py")
    Operator.RegisterPyTechnologyEvent("SkipEvent.py")


def PostTechInitRules(Operator: CENPyOlpTech_RuleInitOperator):
    Operator.AddPyEvent("ApproachRule", "FourPointApproach")
    Operator.SetActivePyEvent("ApproachRule", "FourPointApproach")
