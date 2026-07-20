from cenpylib import *
from centypes import *


def GetCommandName():
    return "ProgramPG"


def GetCommandUuId():
    return "e359f59a-f78d-4f9f-97a1-1e2905a512f5"


def GetIconName():
    return "COM_ScriptsRun"


def ModifyActiveProgram(Operator: CENPyOlpProgramModifyOperator):
    event_handler = Operator.GetEventHandler()
    program = Operator.GetActiveProgram()

    for operation_group in program.GetOperationGroups():
        for operation in operation_group.GetOperations():
            getter = operation.GetAttribGetter()
            has_speed = getter.GetBool("Has_Speed")
            has_wait = getter.GetBool("Has_Wait")

            for tp_element in operation.GetTpElements():
                if has_speed:
                    speed = event_handler.AddBuiltInEventByType(
                        tp_element, EVENT_SPEED, TPINSERTPOS_INSERTBEFORE
                    )
                    speed.SetSpeed(getter.GetDouble("Speed"))
                if has_wait:
                    dwell = event_handler.AddBuiltInEventByType(
                        tp_element, EVENT_DWELL, TPINSERTPOS_INSERTBEFORE
                    )
                    dwell.SetDwellTime(getter.GetDouble("Wait"))
    return False
