"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from typing import overload
from .CENPyOlpPosition import *
from .CENPyOlpTpElement import *

class CENPyOlpTeachHandler:
   @overload
   def GetTpElementPosition(self, tpElement: CENPyOlpTpElement, posRelation: int) -> CENPyOlpPosition:
      """Get position of the toolpath element.
      
      Args:
         tpElement: Reference toolpath element.
         posRelation: Relation of the position.
      
      Returns:
         Toolpath element position.
      """
      ...
   
   @overload
   def GetTpElementPosition(self, tpElement: CENPyOlpTpElement, posRelation: int, baseFrameIndex: int) -> CENPyOlpPosition:
      """Get position of the toolpath element relative to the given base frame, specified by its index.
      
      Args:
         tpElement: Reference toolpath element.
         posRelation: Relation of the position.
         baseFrameIndex: Base frame index.
      
      Returns:
         Toolpath element position.
      """
      ...
   
   def ModifyTpElement(self, olpPosition: CENPyOlpPosition) -> bool:
      """Apply the current position values to the reference toolpath element. Currently, only an active program is allowed to be modified.
      
      Args:
         olpPosition: Olp position to take current values from and that holds the reference toolpath element.
      
      Returns:
         True if modification was successful, False otherwise.
      """
      ...
   
   def InsertNewTpElement(self, olpPosition: CENPyOlpPosition, motionType: int, insertPosition: int) -> CENPyOlpTpElement:
      """Insert a new toolpath element. Currently, only PTP and LIN motion types can be inserted and only an active program is allowed to be modified.
      
      Args:
         olpPosition: Olp position of the toolpath element to be created. Olp position also contains reference toolpath element.
         motionType: Motion type of the toolpath element to be created.
         insertPosition: Insert position in relation to the reference toolpath element.
      
      Returns:
         Newly created toolpath element. None, if failed to insert the new toolpath element.
      """
      ...
   
   def RemoveTpElement(self, toolpathElement: CENPyOlpTpElement):
      """Remove the given toolpath element. Currently, only an active program is allowed to be modified.
      Toolpath elements with the process type ProcessInsert, Auxiliary and TeachInsert will be deleted, and all other types will be suppressed.
      
      Args:
         toolpathElement: Toolpath element to remove.
      """
      ...
   
   def SetTpElementName(self, tpElement: CENPyOlpTpElement, name: str):
      """Set the name of the toolpath element. The Teach Flag for Name will be set.
      
      Args:
         tpElement: Reference toolpath element.
         name: New toolpath element name.
      """
      ...
   
   def SetTpElementMotionType(self, tpElement: CENPyOlpTpElement, iMotionType: int):
      """Set the new motion type of the toolpath element. The Teach Flag for MotionType will be set.
      If the motion type cannot be set because of restrictions, the element will be skipped.
      
      Args:
         tpElement: Reference toolpath element.
         iMotionType: Motion type to set.
      """
      ...
   
   def SetTpElementTargetType(self, tpElement: CENPyOlpTpElement, iTargetType: int):
      """Sets the new target type of the underlying toolpath element. The Teach Flag for TargetType will be set.
      
      Args:
         tpElement: Reference toolpath element.
         iTargetType: Target type to set.
      """
      ...
   
   def SetTpElementConfigBehavior(self, tpElement: CENPyOlpTpElement, iConfigBehavior: int):
      """Sets the config behavior for the given toolpath elements. The Teach Flag for Config will be set.
      
      Args:
         tpElement: Reference toolpath element.
         iConfigBehavior: Config behavior to set.
      """
      ...
   
   def SetTpElementTurnBehavior(self, tpElement: CENPyOlpTpElement, iTurnBehavior: int):
      """Sets the turn behavior for the given toolpath elements. The Teach Flag for Turn will be set.
      
      Args:
         tpElement: Reference toolpath element.
         iTurnBehavior: Turn behavior to set.
      """
      ...
   
   @overload
   def RemoveTeachFlags(self, tpElement: CENPyOlpTpElement) -> bool:
      """Removes all teach flags and resets the toolpath element properties to their initial values.
      
      Args:
         tpElement: Reference toolpath element.
      
      Returns:
         True if successful, otherwise False.
      """
      ...
   
   @overload
   def RemoveTeachFlags(self, tpElement: CENPyOlpTpElement, teachFlags: int) -> bool:
      """Removes the specified teach flags and resets their properties to the initial values.
      
      Args:
         tpElement: Reference toolpath element.
         teachFlags: Teach flags to reset.
      
      Returns:
         True if successful, otherwise False.
      """
      ...
   
