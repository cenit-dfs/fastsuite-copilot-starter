"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpFrame import *
from .CENPyOlpOperation import *
from .CENPyOlpProcessGeometryOperator import *
from .CENPyOlpTpElement import *
from .CENPyOlpTrack import *

class CENPyOlpOperationGroup:
   def GetName(self) -> str:
      """Get the name of the operation group.
      
      Returns:
         Operation group name.
      """
      ...
   
   def SetName(self, name: str):
      """Set the operation group name.
      
      Args:
         name: New name.
      """
      ...
   
   def GetParentProgramName(self) -> str:
      """Get the parent program name of the operation group.
      
      Returns:
         Parent program name.
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
   
   def CreateOperation(self, workMethodName: str, olpPgOperator: CENPyOlpProcessGeometryOperator) -> CENPyOlpOperation:
      """Create a new operation in the operation group.
      
      Args:
         workMethodName: Work method name which computes this operation.
         olpPgOperator: Process geometry operator.
      
      Returns:
         Newly created operation.
      """
      ...
   
   def GetOperations(self) -> list[CENPyOlpOperation]:
      """Get all operations of the operation group.
      
      Returns:
         List of CENPyOlpOperation objects, found operations.
      """
      ...
   
   def GetTpElements(self, includeSuppressed: bool=False) -> list[CENPyOlpTpElement]:
      """Get all toolpath elements of the operation group.
      
      Args:
         includeSuppressed: If True, includes suppressed toolpath elements in the result.
      
      Returns:
         List of CENPyOlpTpElement objects, found toolpath elements.
      """
      ...
   
   def GetTpElementsWithEvent(self, eventName: str) -> list[CENPyOlpTpElement]:
      """Get all toolpath elements of the operation group with given event name.
      
      Args:
         eventName: Event name to search for.
      
      Returns:
         List of CENPyOlpTpElement objects, found toolpath elements with specified event.
      """
      ...
   
   def GetTracks(self) -> list[CENPyOlpTrack]:
      """Get all toolpath tracks of the operation group.
      
      Returns:
         List of CENPyOlpTrack objects, found toolpath tracks.
      """
      ...
   
   def SetToolFrame(self, frame: CENPyOlpFrame):
      """Sets the base frame for the operation group.
      This method updates the base frame for all child operations within the group.
      
      Args:
         frame: A new tool frame as CENPyOlpFrame object to be set.
      """
      ...
   
   def SetBaseFrame(self, frame: CENPyOlpFrame):
      """Sets the tool frame for the operation group.
      This method updates the base frame for all child operations within the group.
      
      Args:
         frame: A new base frame as CENPyOlpFrame object to be set.
      """
      ...
   
