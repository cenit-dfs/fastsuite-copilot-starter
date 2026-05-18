"""
Manually created module. COPYRIGHT CENIT AG 2023.
"""

from .CENPyOlpBuiltInEvent import *

class CENPyOlpWaitForIntSignalEvent(CENPyOlpBuiltInEvent):
   def SetValue(self, value: int):
      """Set the value.
      
      Args:
         value: New value to be set.
      """
      ...
      
   def GetValue(self) -> int:
      """Get the value.
      
      Returns:
         Value stored in the event.
      """
      ...
