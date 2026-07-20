from cenpylib import *
from centypes import *


WEAVE_PATTERN = "WeavePattern"
WEAVE_TYPE = "WeaveType"
WEAVE_LENGTH = "WeaveLength"
WEAVE_FREQUENCY = "WeaveFrequency"
WEAVE_DEFLECTION = "WeaveDeflection"
WEAVE_ANGLE = "WeaveAngle"
ADVANCED_OPTIONS = "AdvancedOptions"
ADVANCED_DELAY = "AdvancedDelay"


def PostTechInitAttributes(Operator: CENPyOlpTech_AttribInitOperator):
    creator = Operator.GetAttribCreator()
    use_level = USER_ATTRIBUTE | PROCESS_ATTRIBUTE | OPERATION_ATTRIBUTE

    creator.AddEnum(WEAVE_PATTERN, ["None", "Triangle"], "None",
                    use_level, WEAVE_PATTERN)
    creator.AddEnum(WEAVE_TYPE, ["Weave length", "Frequency"],
                    "Weave length", use_level, WEAVE_TYPE)
    creator.AddBool(ADVANCED_OPTIONS, False, use_level, ADVANCED_OPTIONS)

    for name in (WEAVE_LENGTH, WEAVE_FREQUENCY, WEAVE_DEFLECTION,
                 WEAVE_ANGLE, ADVANCED_DELAY):
        attribute = creator.AddDouble(name, 0.0, 0.0, 100.0, 0.01,
                                      use_level, ATTRIB_STANDARD, name)
        attribute.SetVisibility(False)


def PostTechOnAttribChanged(Operator: CENPyOlpTech_AttribChangedOperator):
    getter = Operator.GetAttribGetter()
    pattern = getter.GetAttributeEnumByName(WEAVE_PATTERN).GetValue()
    weave_type = getter.GetAttributeEnumByName(WEAVE_TYPE).GetValue()
    weaving = pattern != "None"

    getter.GetAttributeByName(WEAVE_LENGTH).SetVisibility(
        weaving and weave_type == "Weave length"
    )
    getter.GetAttributeByName(WEAVE_FREQUENCY).SetVisibility(
        weaving and weave_type != "Weave length"
    )
    getter.GetAttributeByName(WEAVE_DEFLECTION).SetVisibility(weaving)
    getter.GetAttributeByName(WEAVE_ANGLE).SetVisibility(weaving)
    getter.GetAttributeByName(ADVANCED_DELAY).SetVisibility(
        getter.GetBool(ADVANCED_OPTIONS)
    )
