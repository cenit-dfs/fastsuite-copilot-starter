"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""


class CENPyOlpWM_RuleUpdateOperator:
   def AddEvent(self, eventName: str):
      """Add an event to the rule update operator.
      
      Args:
         eventName: Kernel or Python-defined event name.
      """
      ...
   
   def GetRuleName(self) -> str:
      """Get the name of the rule.
      
      Returns:
         Rule name.
      """
      ...
   
   def GetActiveEventName(self) -> str:
      """Get the name of the currently active event.
      
      Returns:
         Active event name.
      """
      ...
   
   def SetActiveEvent(self, eventName: str):
      """Compare all existing event names with the given name and set the first matched event as active.
      
      Args:
         eventName: Kernel or Python-defined name of the event to activate.
      """
      ...
   
   def OverrideEventRuleInsertPosition(self, insertPosition: int):
      """Set the new insert position for the event rule.
      
      Args:
         insertPosition: New insert position.
      """
      ...
   
