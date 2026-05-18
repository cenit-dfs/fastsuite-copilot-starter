"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpController import *
from .CENPyOlpLogOperator import *

class CENPyOlpTech_EventInitOperator:
   def RegisterPyTechnologyEvent(self, eventName: str):
      """Register a new event in technology.
      
      Args:
         eventName: Event name to be registered.
      """
      ...
   
   def GetController(self) -> CENPyOlpController:
      """Get the parent controller interface.
      
      Returns:
         Controller interface.
      """
      ...
   
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Get the log operator interface.
      
      Returns:
         Log operator interface.
      """
      ...
   
