from cenpylib import *
from centypes import *


FILE_NAME = "FourPointApproach.py: "
APP_SPEED = "ApproachSpeed"
APP_ACCURACY = "ApproachAccuracy"
APPROACH_Z = "ApproachLengthZ"
SKIP_EVENT_UUID = "f2bbdeea-7ef1-4ad7-ad66-56e0a101e6b4"


def GetEventName():
    return "FourPointApproach"


def GetEventUuId():
    return "1E02EA6A-BD3C-475F-BC79-0CD098C00EFC"


def GetIconName():
    return "StartPoint"


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
    use_level = USER_ATTRIBUTE | PROCESS_ATTRIBUTE

    speed = creator.AddDouble(APP_SPEED, 0.3, 0.0, 10.0, 0.01,
                              use_level, ATTRIB_SPEED, APP_SPEED)
    speed.SetReComputeEnterState(ENTERSTATE_NORECOMPUTE)

    accuracy = creator.AddDouble(APP_ACCURACY, 15.0, 0.0, 100.0, 0.01,
                                 use_level, ATTRIB_STANDARD, APP_ACCURACY)
    accuracy.SetReComputeEnterState(ENTERSTATE_NORECOMPUTE)

    approach_z = creator.AddDouble(APPROACH_Z, 0.05, 0.0, 1.0, 0.01,
                                   use_level, ATTRIB_LENGTH, APPROACH_Z)
    approach_z.SetReComputeEnterState(ENTERSTATE_COMPLETE)


def PostProcessAttributes(Operator: CENPyOlpEvent_PEOperator):
    pass


def PostCompute(Operator: CENPyOlpEvent_EventComputeOperator):
    logger = Operator.GetLoggerOperator()
    getter = Operator.GetAttribGetter()
    event_operator = Operator.GetEventOperator()

    offsets = None
    resources = Operator.GetController().GetResources(
        FSITEMTYPE_PERIPHERAL, ITEM_TOOL
    )
    for resource in resources:
        offsets = (
            resource.GetValueOfFloatAttributeByName("CAMERA_X"),
            resource.GetValueOfFloatAttributeByName("CAMERA_Y"),
            resource.GetValueOfFloatAttributeByName("SPRAY_X"),
            resource.GetValueOfFloatAttributeByName("SPRAY_Y")
        )
        break

    if offsets is None:
        logger.LogError(FILE_NAME + "No peripheral tool resource was found.")
        return

    camera_x, camera_y, spray_x, spray_y = offsets
    z_offset = getter.GetDouble(APPROACH_Z)

    matrices = [
        Operator.GetRefTpElement().GetInitialPathMatrix()
        for _ in range(5)
    ]
    matrices[0].Translate(0.0, 0.0, z_offset, True)
    matrices[1].Translate(camera_x, camera_y, z_offset, True)
    matrices[2].Translate(0.0, 0.0, z_offset, True)
    matrices[3].Translate(spray_x, spray_y, z_offset, True)
    matrices[4].Translate(0.0, 0.0, z_offset, True)

    first = Operator.MovePTP(matrices[0])
    speed = event_operator.AddSpeed(first, TPINSERTPOS_INSERTBEFORE)
    speed.SetSpeed(getter.GetDouble(APP_SPEED))
    accuracy = event_operator.AddAccuracyEvent(
        first, TPINSERTPOS_INSERTBEFORE
    )
    accuracy.SetAccuracy(getter.GetDouble(APP_ACCURACY) / 1000.0)

    second = Operator.MoveLin(matrices[1])
    skip_on = event_operator.AddEvent(
        SKIP_EVENT_UUID, second, TPINSERTPOS_INSERTBEFORE
    )
    skip_on.SetBool("Skip", True)

    Operator.MoveLin(matrices[2])
    Operator.MoveLin(matrices[3])
    fifth = Operator.MoveLin(matrices[4])
    skip_off = event_operator.AddEvent(
        SKIP_EVENT_UUID, fifth, TPINSERTPOS_INSERTAFTER
    )
    skip_off.SetBool("Skip", False)
