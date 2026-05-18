"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""


from .OlpCorePythonStringAttribute import *

class OlpCorePythonSetStringAttribute(OlpCorePythonStringAttribute):
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
         
    def SetValue(self, value: str):
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
