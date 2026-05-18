"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from .OlpCorePythonDoubleArrayAttribute import *

class OlpCorePythonSetDoubleArrayAttribute(OlpCorePythonDoubleArrayAttribute):
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
         
    def SetValues(self, values: float):
         """Sets the current values
         
         Args:
            value: the new values to set
         """
         ...
         
    def SetValueUnitType(self, valueUnitType: int):
         """Sets the type of unit the value is given in.
            See AttributeValueUnitType for details and default units
         
         Args:
            valueUnitType: new value unit type to be used
         """
         ...

