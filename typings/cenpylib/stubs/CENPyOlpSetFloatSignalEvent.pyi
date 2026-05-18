"""
Manually created module. COPYRIGHT CENIT AG 2023.
"""

from .CENPyOlpBuiltInEvent import *

class CENPyOlpSetFloatSignalEvent(CENPyOlpBuiltInEvent):
   def SetValue(self, value: float):
      """Set the value.
      
      Args:
         value: New value to be set.
      """
      ...
      
   def GetValue(self) -> float:
      """Get the value.
      
      Returns:
         Value stored in the event.
      """
      ...
