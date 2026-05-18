"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpEventObject import *
from .CENPyOlpLogicPortEvent import *
from .CENPyOlpSyncRobotsEvent import *
from .CENPyOlpTpElement import *

class CENPyOlpEventHandler:
   def GetEventsByName(self, tpElement: CENPyOlpTpElement, eventName: str) -> list[CENPyOlpEventObject]:
      """Get all existing Olp events with the specified name on the given toolpath element.
      
      Args:
         tpElement: Toolpath element to check for events.
         eventName: Event name to search for.
      
      Returns:
         List of CENPyOlpEventObject objects, found events.
      """
      ...
   
   def GetRuleBasedEventsByName(self, tpElement: CENPyOlpTpElement, eventName: str) -> list[CENPyOlpEventObject]:
      """Get all existing rule-based Olp events with the specified name on the given toolpath element.
      
      Args:
         tpElement: Toolpath element to check for events.
         eventName: Event name to search for.
      
      Returns:
         List of CENPyOlpEventObject objects, found events.
      """
      ...
   
   def GetBuiltInEventsByType(self, tpElement: CENPyOlpTpElement, iEventType: int) -> list:
      """Get all existing Built-in events with the specified type on the given toolpath element.
      
      Args:
         tpElement: Toolpath element to check for events
         iEventType: Event type to search for.
      
      Returns:
         List of objects, found events.
      """
      ...
   
   def GetAllRuleBasedEvents(self, tpElement: CENPyOlpTpElement) -> list:
      """Get all existing rule-based Olp events on the given toolpath element.
      
      Args:
         tpElement: Toolpath element to check for events.
      
      Returns:
         Number of found events.
      """
      ...
   
   def GetAllNonRuleBasedEvents(self, tpElement: CENPyOlpTpElement) -> list:
      """Get all existing Olp events, not added by a Rule, on the given toolpath element.
      
      Args:
         tpElement: Toolpath element to check for events.
      
      Returns:
         Number of found events.
      """
      ...
   
   def AddEventByName(self, tpElement: CENPyOlpTpElement, eventName: str, iInsertPosition: int) -> CENPyOlpEventObject:
      """Add a new Olp event on the given toolpath element.
      
      Args:
         tpElement: Toolpath element on which to add a new event.
         eventName: Name of the event to add.
         iInsertPosition: Insert position. "Inherit" is not supported because there is no parent event.
      
      Returns:
         Newly added event.
      """
      ...
   
   def AddBuiltInEventByType(self, tpElement: CENPyOlpTpElement, iEventType: int, iInsertPosition: int) -> object:
      """Add a new Built-in event on the given toolpath element.
      
      Args:
         tpElement: Toolpath element on which to add a new event.
         iEventType: Type of the event to add.
         iInsertPosition: Insert position. "Inherit" is not supported because there is no parent event.
      
      Returns:
         Newly added event.
      """
      ...
   
   def RemoveEvent(self, tpElement: CENPyOlpTpElement, event: CENPyOlpEventObject):
      """Remove the given Olp event from the specified toolpath element.
      
      Args:
         tpElement: Toolpath element to remove event from.
         event: Event to remove.
      """
      ...
   
   def RemoveBuiltInEvent(self, tpElement: CENPyOlpTpElement, event: object):
      """Remove Built-in event from the given toolpath element.
      
      Args:
         tpElement: Toolpath element to remove event from.
         event: Built-in event to remove.
      """
      ...
   
   def AddLogicPortEvent(self, target: CENPyOlpTpElement, logicPortUserNumber: int, direction: PortDirection, iInsertPosition: int) -> CENPyOlpLogicPortEvent:
      """Add a logic port event to the toolpath element. The event is created for the first logic port which has the given direction
      and user number. If no such logic port is found, no event is added and null is returned.
      
      Args:
         target: The toolpath element on which to add the event
         logicPortUserNumber: The user number identifying for which logic port to create the event.
         direction: The direction of the logic port.
         iInsertPosition: Where to add the event with respect to the target
      
      Returns:
         The added event
      """
      ...
   
   def AddSyncRobotsEvent(self, target: CENPyOlpTpElement, iInsertPosition: int) -> CENPyOlpSyncRobotsEvent:
      """Adds a Synchronize Robots event to target toolpath element.
      
      Args:
         target: toolpath element where synchronize robots event to be added.
         iInsertPosition: Insert position - before or after the target toolpath element
      
      Returns:
         The Synchronize Robots Event added
      """
      ...
   
