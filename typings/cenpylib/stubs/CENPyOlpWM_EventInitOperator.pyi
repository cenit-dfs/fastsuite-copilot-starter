"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpController import *
from .CENPyOlpLogOperator import *

class CENPyOlpWM_EventInitOperator:
   def RegisterPyTechnologyEvent(self, pyScriptName: str):
      """Register an event to a work method.
      
      Args:
         pyScriptName: Python-defined rule name.
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
   
