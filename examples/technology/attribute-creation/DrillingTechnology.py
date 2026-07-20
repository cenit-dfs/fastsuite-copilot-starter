from cenpylib import *
from centypes import *


FILE_NAME = "DrillingTechnology.py: "


def PostTechInitAttributes(Operator: CENPyOlpTech_AttribInitOperator):
    creator = Operator.GetAttribCreator()
    creator.AddInteger(
        "MyIntAttribute", 0, -100, 100,
        USER_ATTRIBUTE | PROCESS_ATTRIBUTE | GLOBAL_ATTRIBUTE,
        "MyIntAttribute"
    )
