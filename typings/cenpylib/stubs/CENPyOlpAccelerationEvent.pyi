"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpBuiltInEvent import *

class CENPyOlpAccelerationEvent(CENPyOlpBuiltInEvent):
   def GetAcceleration(self) -> float:
      """Get the acceleration value.
      
      Returns:
         acceleration value.
      """
      ...
   
   def SetAcceleration(self, acceleration: float):
      """Sets the acceleration value.
      
      Args:
         acceleration: the acceleration value
      """
      ...
   
   def SetUnit(self, inUnit: int):
      """Set the event's unit. The unit must be in the list of allowed units for the event.
      Otherwise, the method does nothing.
      
      Args:
         inUnit: event's unit
      """
      ...
   
   def GetPathType(self) -> int:
      """Retrieve the path type that this event is associated with.
      
      Returns:
         event path type
      """
      ...
   
   def SetPathType(self, inPathType: int):
      """Set the path type that this event will be associated with.
      
      Args:
         inPathType: path type
      """
      ...
   
