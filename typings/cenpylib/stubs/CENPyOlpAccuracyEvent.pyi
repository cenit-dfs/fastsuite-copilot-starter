"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpBuiltInEvent import *

class CENPyOlpAccuracyEvent(CENPyOlpBuiltInEvent):
   def GetAccuracy(self) -> float:
      """Gets the value stored on this accuracy event instance
      
      Returns:
         returns the accuracy event value
      """
      ...
   
   def SetAccuracy(self, accuracy: float):
      """Sets the accuracy value for this event instance
      
      Args:
         accuracy: new accuracy value
      """
      ...
   
   def GetPathType(self) -> int:
      """Retrieve the path type that this event is associated with.
      
      Returns:
         path type
      """
      ...
   
   def SetPathType(self, inPathType: int):
      """Set the path type that this event will be associated with.
      
      Args:
         inPathType: path type
      """
      ...
   
   def GetCriteria(self) -> int:
      """Retrieve the accuracy criteria.
      
      Returns:
         accuracy criteria
      """
      ...
   
   def SetCriteria(self, inCriteria: int):
      """Set the accuracy criteria.
      
      Args:
         inCriteria: new accuracy criteria
      """
      ...
   
