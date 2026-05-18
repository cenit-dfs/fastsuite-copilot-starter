"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpMatrix import *
from .CENPyOlpVector import *

class CENPyOlpVector:
   def SetXYZ(self, x: float, y: float, z: float):
      """Set new coordinates.
      
      Args:
         x: X coordinate in meters.
         y: Y coordinate in meters.
         z: Z coordinate in meters.
      """
      ...
   
   def GetXYZ(self) -> tuple[float, float, float]:
      """Get the coordinates as tuple.
      
      Returns:
         tuple[float, float, float] that represent X, Y and Z coordinates in meters.
      """
      ...
   
   def GetX(self) -> float:
      """Get the X value.
      
      Returns:
         X coordinate in meters.
      """
      ...
   
   def GetY(self) -> float:
      """Get the Y value.
      
      Returns:
         Y coordinate in meters.
      """
      ...
   
   def GetZ(self) -> float:
      """Get the Z value.
      
      Returns:
         Z coordinate in meters.
      """
      ...
   
   def SetX(self, val: float):
      """Set the X value.
      
      Args:
         val: X coordinate in meters.
      """
      ...
   
   def SetY(self, val: float):
      """Set the Y value.
      
      Args:
         val: Y coordinate in meters.
      """
      ...
   
   def SetZ(self, val: float):
      """Set the Z value.
      
      Args:
         val: Z coordinate in meters.
      """
      ...
   
   def Normalize(self):
      """Normalize the vector.
      """
      ...
   
   def Transform(self, pyTransformationMatrix: CENPyOlpMatrix):
      """Transform the vector.
      
      Args:
         pyTransformationMatrix: Transformation matrix.
      """
      ...
   
   def Angle(self, pySecondVec: CENPyOlpVector) -> float:
      """Compute the angle between current and another vector.
      
      Args:
         pySecondVec: Another vector.
      
      Returns:
         Angle.
      """
      ...
   
   def Invert(self):
      """Invert the vector.
      """
      ...
   
