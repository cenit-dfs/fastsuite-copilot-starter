"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpController import *
from .CENPyOlpEventObject import *
from .CENPyOlpLogOperator import *

class CENPyOlpTech_RuleInitOperator:
   def AddPyEvent(self, ruleName: str, pyEventName: str) -> CENPyOlpEventObject:
      """Add an event to the event rule.
      
      Args:
         ruleName: Kernel or Python-defined rule name.
         pyEventName: Kernel or Python-defined event name.
      
      Returns:
         Added event object.
      """
      ...
   
   def AddPyEventByUUID(self, ruleName: str, eventUUID: str) -> CENPyOlpEventObject:
      """Add an event to the event rule.
      
      Args:
         ruleName: Kernel or Python-defined rule name.
         eventUUID: Kernel or Python-defined event uuid.
      
      Returns:
         Added event object.
      """
      ...
   
   def SetActivePyEvent(self, ruleName: str, eventBaseName: str):
      """Set the given event as active in the specified rule.
      
      Args:
         ruleName: Kernel or Python-defined rule name.
         eventBaseName: Kernel or Python-defined event name.
      """
      ...
   
   def OverrideEventRuleInsertPosition(self, ruleName: str, insertPosition: int):
      """Set the new insert position for the event rules with given name.
      
      Args:
         ruleName: Event rule name to search for.
         insertPosition: New insert position.
      """
      ...
   
   def RemoveEventFromRule(self, ruleName: str, eventName: str):
      """Remove an event from the event rule.
      
      Args:
         ruleName: Kernel or Python-defined rule name.
         eventName: Kernel or Python-defined event name.
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
   
