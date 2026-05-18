"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from centypes import *
from .CENPyOlpSystemAttribSetter import *

class CENPyOlpAttribSetter:
   def SetInteger(self, name: str, val: int, overrideMode: int=ATTRIBOVERRIDEMODE_DEFAULT):
      """Set the Integer Value for the given Integer attribute.
      
      Args:
         name: Name of the attribute.
         val: New Value of the attribute.
         overrideMode: Level at which to set the attribute Value (Default = 0, OpGroup, Operation, CheckLevel).
      """
      ...
   
   def SetDouble(self, name: str, val: float, overrideMode: int=ATTRIBOVERRIDEMODE_DEFAULT):
      """Set the Double Value for the given Double attribute.
      
      Args:
         name: Name of the attribute.
         val: New Value of the attribute.
         overrideMode: Level at which to set the attribute Value (Default = 0, OpGroup, Operation, CheckLevel).
      """
      ...
   
   def SetString(self, name: str, val: str, overrideMode: int=ATTRIBOVERRIDEMODE_DEFAULT):
      """Set the String Value for the given String attribute.
      
      Args:
         name: Name of the attribute.
         val: New Value of the attribute.
         overrideMode: Level at which to set the attribute Value (Default = 0, OpGroup, Operation, CheckLevel).
      """
      ...
   
   def SetBool(self, name: str, val: bool, overrideMode: int=ATTRIBOVERRIDEMODE_DEFAULT):
      """Set the Bool Value for the given Bool attribute.
      
      Args:
         name: Name of the attribute.
         val: New Value of the attribute.
         overrideMode: Level at which to set the attribute Value (Default = 0, OpGroup, Operation, CheckLevel).
      """
      ...
   
   def SetEnumIndex(self, name: str, index: int, overrideMode: int=ATTRIBOVERRIDEMODE_DEFAULT):
      """Set the EnumIndex Value for the given Enum attribute.
      
      Args:
         name: Name of the attribute.
         index: New Value of the attribute.
         overrideMode: Level at which to set the attribute Value (Default = 0, OpGroup, Operation, CheckLevel).
      """
      ...
   
   def GetSystemAttribSetter(self) -> CENPyOlpSystemAttribSetter:
      """Get the system attribute setter.
      
      Returns:
         System attribute setter object.
      """
      ...
   
