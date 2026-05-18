"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""


class CENPyOlpTech_RuleUpdateOperator:
   def AddEvent(self, eventName: str):
      """Add an event to rule update operator.
      
      Args:
         eventName: Name of the event.
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
         Name of the active event.
      """
      ...
   
   def SetActiveEvent(self, eventName: str):
      """Compare all existing event names with the given name and set the first matched event to active.
      
      Args:
         eventName: Name of the event to activate.
      """
      ...
   
   def OverrideEventRuleInsertPosition(self, insertPosition: int):
      """Set the new insert position for the event rule.
      
      Args:
         insertPosition: New insert position.
      """
      ...
   
