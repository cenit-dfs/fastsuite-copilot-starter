"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpMatrix import *
from .CENPyOlpPoint import *

class CENPyOlpPoint:
   def SetXYZ(self, x: float, y: float, z: float):
      """Set coordinates of OlpPoint
      
      Args:
         x: X in meters.
         y: Y in meters.
         z: Z in meters.
      """
      ...
   
   def GetXYZ(self) -> tuple[float, float, float]:
      """Get XYZ coordinates as a tuple.
      
      Returns:
         tuple[float, float, float] that represent X, Y and Z coordinates in meters.
      """
      ...
   
   def GetX(self) -> float:
      """Get X coordinate.
      
      Returns:
         X value in meters.
      """
      ...
   
   def GetY(self) -> float:
      """Get Y coordinate.
      
      Returns:
         Y value in meters.
      """
      ...
   
   def GetZ(self) -> float:
      """Get Z coordinate.
      
      Returns:
         Z value in meters.
      """
      ...
   
   def SetX(self, val: float):
      """Set X coordinate.
      
      Args:
         val: X value in meters.
      """
      ...
   
   def SetY(self, val: float):
      """Set Y coordinate.
      
      Args:
         val: Y value in meters.
      """
      ...
   
   def SetZ(self, val: float):
      """Set Z coordinate.
      
      Args:
         val: Z value in meters.
      """
      ...
   
   def Transform(self, pyTransformationMatrix: CENPyOlpMatrix):
      """Transform the point.
      
      Args:
         pyTransformationMatrix: Transformation matrix.
      """
      ...
   
   def Dist(self, pySecondPt: CENPyOlpPoint) -> float:
      """Get the distance between the current and the given point.
      
      Args:
         pySecondPt: Another point.
      
      Returns:
         Distance in meters.
      """
      ...
   
