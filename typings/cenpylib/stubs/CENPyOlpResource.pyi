"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribute import *
from .CENPyOlpFrame import *
from .CENPyOlpHomePosition import *
from .CENPyOlpJoint import *
from .CENPyOlpPort import *

class CENPyOlpResource:
   def GetName(self) -> str:
      """Get the resource name.
      
      Returns:
         Resource name.
      """
      ...
   
   def GetManufacturer(self) -> str:
      """Get the resource manufacturer.
      
      Returns:
         Resource manufacturer.
      """
      ...
   
   def GetSeries(self) -> str:
      """Get the resource series.
      
      Returns:
         Resource series.
      """
      ...
   
   def GetModel(self) -> str:
      """Get the resource model.
      
      Returns:
         Resource model.
      """
      ...
   
   def GetItemType(self) -> int:
      """Get the item type of the resource as unsigned integer.
      
      Returns:
         Item type of the resource as unsigned integer.
      """
      ...
   
   def GetItemSubType(self) -> int:
      """Get the item sub type of the resource as unsigned integer.
      
      Returns:
         Item sub type of the resource as unsigned integer.
      """
      ...
   
   def GetAllPorts(self) -> list[CENPyOlpPort]:
      """Get all ports that are currently active in this resource.
      
      Returns:
         List of CENPyOlpPort objects, found ports.
      """
      ...
   
   def GetAllJoints(self) -> list[CENPyOlpJoint]:
      """Get all joints that are currently active in this resource.
      
      Returns:
         List of CENPyOlpJoint objects, found joints.
      """
      ...
   
   def GetPorts(self, valueType: int, direction: int) -> list[CENPyOlpPort]:
      """Get all ports of a specific value type and direction that are currently active in this resource.
      
      Args:
         valueType: Desired value type for the ports.
         direction: Desired direction for the ports.
      
      Returns:
         List of CENPyOlpPort objects, found ports with specified value type and direction.
      """
      ...
   
   def GetAttributeByName(self, attributeName: str) -> CENPyOlpAttribute:
      """Get access to the attribute by name.
      
      Args:
         attributeName: Name of attribute to search for.
      
      Returns:
         Attribute object.
      """
      ...
   
   def GetValueOfIntegerAttributeByName(self, name: str) -> int:
      """Get access to the integer attribute by name.
      
      Args:
         name: Name of attribute to search for.
      
      Returns:
         Value of the attribute.
      """
      ...
   
   def GetValueOfFloatAttributeByName(self, name: str) -> float:
      """Get access to the float attribute by name.
      
      Args:
         name: Name of attribute to search for.
      
      Returns:
         Value of the attribute.
      """
      ...
   
   def GetValueOfStringAttributeByName(self, name: str) -> str:
      """Get access to the string attribute by name.
      
      Args:
         name: Name of attribute to search for.
      
      Returns:
         Value of the attribute.
      """
      ...
   
   def GetValueOfBoolAttributeByName(self, name: str) -> bool:
      """Get access to the bool attribute by name.
      
      Args:
         name: Name of attribute to search for.
      
      Returns:
         Value of the attribute.
      """
      ...
   
   def GetHomePositions(self) -> list[CENPyOlpHomePosition]:
      """Get all home positions of this resource
      
      Returns:
         List of CENPyOlpHomePosition objects, representing home positions of this resource.
      """
      ...
   
   def GetBaseFrames(self) -> list[CENPyOlpFrame]:
      """Get all base frames of this resource.
      
      Returns:
         List of CENPyOlpFrame objects representing the base frames of this resource.
      """
      ...
   
   def GetChildFrames(self) -> list[CENPyOlpFrame]:
      """Get all child frames of this resource.
      
      Returns:
         List of CENPyOlpFrame objects representing the child frames of this resource.
      """
      ...
   
