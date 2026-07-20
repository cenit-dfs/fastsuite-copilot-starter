from cenpylib import *
from centypes import *


FILE_NAME = "SkipEvent.py: "


def GetEventName():
    return "SkipEvent"


def GetEventUuId():
    return "f2bbdeea-7ef1-4ad7-ad66-56e0a101e6b4"


def GetIconName():
    return "ProcessStop"


def GetExplodeCycle():
    return 0


def GetCycleExplodeBehavior():
    return CYCLE_EXPLODEIMMEDIATELY


def GetMultipleCreationIsPossible():
    return 1


def GetEventType():
    return OLPEVENT_OLP


def GetCycleTranslationFlag():
    return CYCLETRANSLATION_TRANSYES


def GetCycleTranslationManualFlag():
    return CYCLETRANSLATION_TRANSYES


def GetCycleTranslationAutoFlag():
    return CYCLETRANSLATION_TRANSYES


def GetCycleRotationFlag():
    return CYCLEROTATION_ROTPATHTOOL


def GetCycleRotationAutoFlag():
    return CYCLEROTATION_ROTPATHTOOL


def GetCycleRotationManualFlag():
    return CYCLEROTATION_ROTPATHTOOL


def IsMachiningCycle():
    return False


def GetGroupName():
    return "OlpEvent"


def PostInitAttributes(Operator: CENPyOlpEvent_AttribInitOperator):
    creator = Operator.GetAttribCreator()
    skip = creator.AddBool(
        "Skip", True, USER_ATTRIBUTE | PROCESS_ATTRIBUTE, "Skip"
    )
    skip.SetReComputeEnterState(ENTERSTATE_NORECOMPUTE)
