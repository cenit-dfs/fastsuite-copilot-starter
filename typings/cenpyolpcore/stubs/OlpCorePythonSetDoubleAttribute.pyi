"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""


from .OlpCorePythonDoubleAttribute import *

class OlpCorePythonSetDoubleAttribute(OlpCorePythonDoubleAttribute):
    def SetOlpProperty(self, olpProperty: int):
         """Sets the AttributeProperties of this attribute
         
         Args:
            olpProperty: AttributeProperties to be set
         """
         ...

    def SetReadOnly(self, isReadOnly: bool):
         """Sets whether or not this attribute is globally read-only
         
         Args:
            isReadOnly: True if the must be attribute is read-only, False otherwise
         """
         ...
         
    def SetName(self, name: str): 
         """Sets the name of the attribute
         
         Args:
            name: the name of the attribute
         """
         ...
         
    def SetGroupName(self, name: str):
         """Sets the group name
         
         Args:
            name: the name of the attribute group
         """
         ...
         
    def SetValue(self, value: float):
         """Sets the current value
         
         Args:
            value: the new value to set
         """
         ...
         
    def SetValueUnitType(self, valueUnitType: int):
         """Sets the type of unit the value is given in.
            See AttributeValueUnitType for details and default units
         
         Args:
            valueUnitType: new value unit type to be used
         """
         ...

    def SetMinimum(self, minValue: float):
         """Sets the defined valid minimum value
       
         Args:
            minValue: the minimum value the attribute can represent
         """
         ...

    def SetMaximum(self, maxValue: float):
         """Sets the defined valid maximum value
         
         Args:
            maxValue: the maximum value the attribute can represent
         """
         ...

    def SetStepSize(self, stepSize: float):
         """Sets the defined step size used for changing the value of the attribute in spinners.
            The step size does not define the smallest applicable change.
         
         Args:
            stepSize: the defined step size
         """
         ...