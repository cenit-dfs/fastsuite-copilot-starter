"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpVector import *

class CENPyOlpWM_GeometryOperator:
   def CreateVector(self, x: float, y: float, z: float) -> CENPyOlpVector:
      """Create a vector by specifying direction values.
      
      Args:
         x: X-direction.
         y: Y-direction.
         z: Z-direction.
      
      Returns:
         Newly created vector.
      """
      ...
   
   def GetIncludedAngle(self, v0: CENPyOlpVector, v1: CENPyOlpVector, normal: CENPyOlpVector, dir: int) -> float:
      """Get the absolute included angle between the two input vectors in the specified direction about the given normal.
      
      Args:
         v0: The first vector to calculate angle.
         v1: The second vector to calculate angle.
         normal: The normal to the rotational plane
         dir: The direction for angle measurement (dir=1:anticlockwise  dir=-1:clockwise).
      
      Returns:
         Angle between the two vectors in radians from 0 to 2*Pi.
      """
      ...
   
   def ToRadian(self, degrees: float) -> float:
      """Convert the given value from degrees to radians.
      
      Args:
         degrees: Value in degrees.
      
      Returns:
         Value in radians.
      """
      ...
   
   def ToDegrees(self, radians: float) -> float:
      """Convert the given value from radians to degrees.
      
      Args:
         radians: Value in radians.
      
      Returns:
         Value in degrees.
      """
      ...
   
