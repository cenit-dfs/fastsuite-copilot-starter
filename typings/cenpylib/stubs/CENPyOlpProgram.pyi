"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from typing import overload
from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpFrame import *
from .CENPyOlpOperation import *
from .CENPyOlpOperationGroup import *
from .CENPyOlpTpElement import *
from .CENPyOlpTrack import *

class CENPyOlpProgram:
   def GetName(self) -> str:
      """Get the name of the program.
      
      Returns:
         Program name.
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
   
   def GetOperationGroups(self) -> list[CENPyOlpOperationGroup]:
      """Get all operation groups of the program, including groups from subprogram calls.
      
      Returns:
         List of CENPyOlpOperationGroup objects, found operation groups.
      """
      ...
   
   def GetOperations(self) -> list[CENPyOlpOperation]:
      """Get all operations of the program, including operations from subprogram calls.
      
      Returns:
         List of CENPyOlpOperation objects, found operations.
      """
      ...
   
   def GetLastCreatedOperations(self) -> list[CENPyOlpOperation]:
      """Get the last created and not deleted operations in the program.
      
      Returns:
         List of CENPyOlpOperation objects, the last created operations.
      """
      ...
   
   def GetTpElements(self, includeSuppressed: bool=False) -> list[CENPyOlpTpElement]:
      """Get all toolpath elements of the program, including elements from subprogram calls.
      
      Args:
         includeSuppressed: If True, includes suppressed toolpath elements in the result.
      
      Returns:
         List of CENPyOlpTpElement objects, found toolpath elements.
      """
      ...
   
   def GetTpElementsWithEvent(self, eventName: str) -> list[CENPyOlpTpElement]:
      """Get all toolpath elements of the program with given event name, including elements from subprogram calls.
      
      Args:
         eventName: Event name to search for.
      
      Returns:
         List of CENPyOlpTpElement objects, found toolpath elements with specified event.
      """
      ...
   
   @overload
   def ProgramProcessGeometries(self, processGeometries: list) -> bool:
      """Program the given process geometries in the active controller program with default tool and base frames.
      
      Args:
         processGeometries: Process geometries as CENPyOlpProcessGeometryOperator to program.
      
      Returns:
         True if the operation was completed without errors, otherwise False.
      """
      ...
   
   @overload
   def ProgramProcessGeometries(self, processGeometries: list, baseFrameIndex: int, toolFrameIndex: int) -> bool:
      """Program the given process geometries in the active controller program with specified tool and base frame indexes.
      
      Args:
         processGeometries: Process geometries CENPyOlpProcessGeometryOperator to program.
         baseFrameIndex: Base frame index to use.
         toolFrameIndex: Tool frame index to use.
      
      Returns:
         True if the operation was completed without errors, otherwise False.
      """
      ...
   
   def IsMain(self) -> bool:
      """Get if the program has the "main" flag or is a subprogram.
      
      Returns:
         True if the program is "main", and False if it is a subprogram.
      """
      ...
   
   def GetTracks(self) -> list[CENPyOlpTrack]:
      """Get all toolpath tracks of the program.
      
      Returns:
         List of CENPyOlpTrack objects, found toolpath tracks.
      """
      ...
   
   def SetToolFrame(self, frame: CENPyOlpFrame):
      """Sets the tool frame for the program.
      This method updates the tool frame for the entire program, including all its components.
      
      Args:
         frame: A new tool frame as CENPyOlpFrame object to be set.
      """
      ...
   
   def SetBaseFrame(self, frame: CENPyOlpFrame):
      """Sets the tool frame for the program.
      This method updates the tool frame for the entire program, including all its components.
      
      Args:
         frame: A new base frame as CENPyOlpFrame object to be set.
      """
      ...
   
