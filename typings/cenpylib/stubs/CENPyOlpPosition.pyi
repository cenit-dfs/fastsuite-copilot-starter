"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from typing import overload
from .CENPyOlpMatrix import *
from .CENPyOlpTpElement import *

class CENPyOlpPosition:
   def X(self) -> float:
      """Get X coordinate.
      
      Returns:
         X coordinate.
      """
      ...
   
   def Y(self) -> float:
      """Get Y coordinate.
      
      Returns:
         Y coordinate.
      """
      ...
   
   def Z(self) -> float:
      """Get Z coordinate.
      
      Returns:
         Z coordinate.
      """
      ...
   
   def RX(self) -> float:
      """Get Rx orientation.
      
      Returns:
         Rx orientation.
      """
      ...
   
   def RY(self) -> float:
      """Get Ry orientation.
      
      Returns:
         Ry orientation.
      """
      ...
   
   def RZ(self) -> float:
      """Get Rz orientation.
      
      Returns:
         Rz orientation.
      """
      ...
   
   def GetCoordinates(self) -> list[float]:
      """Get all toolpath element coordinates.
      
      Returns:
         List with X, Y and Z coordinates as float values.
      """
      ...
   
   def GetCoordinatesToBaseFrame(self) -> list[float]:
      """Get all toolpath element coordinates relative to BaseFrame.
      
      Returns:
         List with X, Y and Z coordinates as float values.
      """
      ...
   
   @overload
   def SetCoordinates(self, x: float, y: float, z: float):
      """Set all toolpath element coordinates.
      
      Args:
         x: X coordinate.
         y: Y coordinate.
         z: Z coordinate.
      """
      ...
   
   @overload
   def SetCoordinates(self, coordinates: list):
      """Set all toolpath element coordinates using the list.
      
      Args:
         coordinates: List with X, Y and Z float coordinates.
      """
      ...
   
   def GetViaPointCoordinates(self) -> list[float]:
      """Get all via point coordinates.
      
      Returns:
         List with X, Y and Z coordinates as float values.
      """
      ...
   
   @overload
   def SetViaPointCoordinates(self, x: float, y: float, z: float):
      """Set all via point coordinates.
      
      Args:
         x: X coordinate.
         y: Y coordinate.
         z: Z coordinate.
      """
      ...
   
   @overload
   def SetViaPointCoordinates(self, coordinates: list):
      """Set all via point coordinates using the list.
      
      Args:
         coordinates: List with X, Y and Z float coordinates.
      """
      ...
   
   def GetOrientation(self) -> list[float]:
      """Get all orientations.
      
      Returns:
         List with RX, RY and RZ orientations as float values.
      """
      ...
   
   @overload
   def SetOrientation(self, rx: float, ry: float, rz: float):
      """Set all orientations.
      
      Args:
         rx: Rx orientation.
         ry: Ry orientation.
         rz: Rz orientation.
      """
      ...
   
   @overload
   def SetOrientation(self, orientation: list):
      """Set all orientations using the list.
      
      Args:
         orientation: List with float RX, RY and RZ orientations.
      """
      ...
   
   def GetRefTpElement(self) -> CENPyOlpTpElement:
      """Get the reference toolpath element.
      
      Returns:
         >Olp toolpath element.
      """
      ...
   
   def SetRefTpElement(self, olpTpElement: CENPyOlpTpElement):
      """Set the reference toolpath element.
      
      Args:
         olpTpElement: Olp toolpath element.
      """
      ...
   
   def GetPositionRelation(self) -> int:
      """Get the relation of the position.
      
      Returns:
         Relation of the position.
      """
      ...
   
   @overload
   def SetPositionRelation(self, newPosRelation: int):
      """Set the new relation for the position.
      
      Args:
         newPosRelation: Position relation to set.
      """
      ...
   
   @overload
   def SetPositionRelation(self, newPosRelation: int, baseFrameIndex: int):
      """Set the position relation to Base frame and the base frame index.
      
      Args:
         newPosRelation: Position relation to set.
         baseFrameIndex: Base frame index to set.
      """
      ...
   
   def GetMatrix(self) -> CENPyOlpMatrix:
      """Get the represented toolpath element matrix.
      
      Returns:
         Matrix.
      """
      ...
   
   def GetViaPointMatrix(self) -> CENPyOlpMatrix:
      """Get the represented via point matrix.
      
      Returns:
         Matrix.
      """
      ...
   
   def GetWorldMatrix(self) -> CENPyOlpMatrix:
      """Get the world matrix of the position.
      
      Returns:
         World matrix.
      """
      ...
   
   @overload
   def TranslatePosition(self, x: float, y: float, z: float, positionRelation: int):
      """Translates the toolpath element position locally in given direction.
      
      Args:
         x: Direction in local x.
         y: Direction in local y.
         z: Direction in local z.
         positionRelation: Position relation the local translation should be done in.
      """
      ...
   
   @overload
   def TranslatePosition(self, x: float, y: float, z: float, positionRelation: int, baseFrameIndex: int):
      """Translates the toolpath element position locally in given direction relative to the base frame, specified by its index.
      
      Args:
         x: Direction in local x.
         y: Direction in local y.
         z: Direction in local z.
         positionRelation: Position relation the local translation should be done in.
         baseFrameIndex: Base frame index to be used for translation.
      """
      ...
   
   @overload
   def TranslateViaPointPosition(self, x: float, y: float, z: float, positionRelation: int):
      """Translates the via point position locally in given direction.
      
      Args:
         x: Direction in local x.
         y: Direction in local y.
         z: Direction in local z.
         positionRelation: Position relation the local translation should be done in.
      """
      ...
   
   @overload
   def TranslateViaPointPosition(self, x: float, y: float, z: float, positionRelation: int, baseFrameIndex: int):
      """Translates the via point position locally in given direction relative to the base frame, specified by its index.
      
      Args:
         x: Direction in local x.
         y: Direction in local y.
         z: Direction in local z.
         positionRelation: Position relation the local translation should be done in.
         baseFrameIndex: Base frame index to be used for translation.
      """
      ...
   
   @overload
   def RotatePosition(self, rX: float, rY: float, rZ: float, positionRelation: int):
      """Rotates the position locally around given direction.
      
      Args:
         rX: Rotation around local x.
         rY: Rotation around local y.
         rZ: Rotation around local z.
         positionRelation: Position relation the local rotation should be done in.
      """
      ...
   
   @overload
   def RotatePosition(self, rX: float, rY: float, rZ: float, positionRelation: int, baseFrameIndex: int):
      """Rotates the position locally around given direction relative to the base frame, specified by its index.
      
      Args:
         rX: Rotation around local x.
         rY: Rotation around local y.
         rZ: Rotation around local z.
         positionRelation: Position relation the local rotation should be done in.
         baseFrameIndex: Base frame index to be used for rotation.
      """
      ...
   
   def GetViaPointName(self) -> str:
      """Get the name of the Via point if it exists, <c>nullptr</c> otherwise.
      
      Returns:
         Via point name.
      """
      ...
   
   def GetJointValues(self) -> list[float]:
      """Get all toolpath element joint values.
      
      Returns:
         Joint float values list.
      """
      ...
   
   def SetJointValues(self, values: list):
      """Set all toolpath element joint values.
      
      Args:
         values: Joint float values list.
      """
      ...
   
   def GetExternalJointValues(self) -> list[float]:
      """Get all toolpath element external joint values.
      
      Returns:
         Joint float values list.
      """
      ...
   
   def SetExternalJointValues(self, values: list, additional: bool=False):
      """Set all toolpath element external joint values.
      
      Args:
         values: Joint float values list.
         additional: if True, don't clear existing _modifiedTeachFlags trans and rot float values.
      """
      ...
   
