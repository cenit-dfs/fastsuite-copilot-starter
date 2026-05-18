"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpEventObject import *
from .CENPyOlpFrame import *
from .CENPyOlpTpElement import *
from .CENPyOlpTrack import *

class CENPyOlpOperation:
   def GetName(self) -> str:
      """Get the name of the operation.
      
      Returns:
         Operation group name.
      """
      ...
   
   def SetName(self, name: str):
      """Set the operation name.
      
      Args:
         name: New name.
      """
      ...
   
   def GetAttribGetter(self) -> CENPyOlpAttribGetter:
      """Get attribute getter interface which handles the Olp attribute container.
      
      Returns:
         Attribute getter interface.
      """
      ...
   
   def GetAttribSetter(self) -> CENPyOlpAttribSetter:
      """Get attribute setter interface which handles the Olp attribute container.
      
      Returns:
         Attribute setter interface.
      """
      ...
   
   def OverrideAttribute(self, name: str):
      """Override an attribute with the given name.
      
      Args:
         name: Name of the attribute to override.
      """
      ...
   
   def GetProcessGeometryIdentifier(self) -> str:
      """Get the UUID of the process geometry of the current operation.
      
      Returns:
         Process geometry UUID.
      """
      ...
   
   def GetTpElements(self, includeSuppressed: bool=False) -> list[CENPyOlpTpElement]:
      """Get all toolpath elements of the operation.
      
      Args:
         includeSuppressed: If True, includes suppressed toolpath elements in the result.
      
      Returns:
         List of CENPyOlpTpElement objects, found toolpath elements.
      """
      ...
   
   def GetTpElementsWithEvent(self, eventName: str) -> list[CENPyOlpTpElement]:
      """Get all toolpath elements of the operation with given event name.
      
      Args:
         eventName: Event name to search for.
      
      Returns:
         List of CENPyOlpTpElement objects, found toolpath elements with specified event.
      """
      ...
   
   def GetTracks(self) -> list[CENPyOlpTrack]:
      """Get all toolpath tracks of the operation.
      
      Returns:
         List of CENPyOlpTrack objects, found toolpath tracks.
      """
      ...
   
   def GetActiveEventRules(self) -> list[CENPyOlpEventObject]:
      """Get all active event rules found on the operation.
      
      Returns:
         List of CENPyOlpEventObject objects
      """
      ...
   
   def UpdateNameFromRule(self):
      """Updates the Operation Name for AP dashboard. Might be not updated from Script call
      """
      ...
   
   def SetToolFrame(self, frame: CENPyOlpFrame):
      """Sets the tool frame for the operation.
      
      Args:
         frame: A new tool frame as CENPyOlpFrame object to be set.
      """
      ...
   
   def GetToolFrame(self) -> CENPyOlpFrame:
      """Gets the tool frame of the operation.
      
      Returns:
         Object CENPyOlpFrame representing the current tool frame.
      """
      ...
   
   def SetBaseFrame(self, frame: CENPyOlpFrame):
      """Sets the base frame for the operation.
      
      Args:
         frame: A new base frame as CENPyOlpFrame object to be set.
      """
      ...
   
   def GetBaseFrame(self) -> CENPyOlpFrame:
      """Gets the base frame of the operation.
      
      Returns:
         Object CENPyOlpFrame representing the current base frame.
      """
      ...
   
