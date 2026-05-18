"""
Manually created module. COPYRIGHT CENIT AG 2023.
"""

from .CENPyOlpBuiltInEvent import *

class CENPyOlpWaitForBoolSignalEvent(CENPyOlpBuiltInEvent):
   def SetValue(self, value: bool):
      """Set the value.
      
      Args:
         value: New value to be set.
      """
      ...
      
   def GetValue(self) -> bool:
      """Get the value.
      
      Returns:
         Value stored in the event.
      """
      ...
