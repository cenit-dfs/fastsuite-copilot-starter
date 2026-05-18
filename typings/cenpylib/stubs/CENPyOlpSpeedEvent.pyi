"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpBuiltInEvent import *

class CENPyOlpSpeedEvent(CENPyOlpBuiltInEvent):
   def GetSpeed(self) -> float:
      """Get the speed value.
      
      Returns:
         Speed value.
      """
      ...
   
   def SetSpeed(self, speed: float):
      """Set the speed value.
      
      Args:
         speed: New speed value.
      """
      ...
   
   def GetPathType(self) -> int:
      """Get the path type that this event is for.
      
      Returns:
         Path type.
      """
      ...
   
   def SetPathType(self, inPathType: int):
      """Set the path type that this event is for.
      
      Args:
         inPathType: New path type.
      """
      ...
   
   def GetUnit(self) -> int:
      """Get the event units.
      
      Returns:
         Event units.
      """
      ...
   
   def SetUnit(self, inUnit: int):
      """Set the event units.
      The units must be in the list of allowed units for the event, otherwise, the method does nothing.
      
      Args:
         inUnit: New event units.
      """
      ...
   
