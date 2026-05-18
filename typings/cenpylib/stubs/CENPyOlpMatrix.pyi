"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from typing import overload
from .CENPyOlpMatrix import *
from .CENPyOlpPoint import *
from .CENPyOlpVector import *

class CENPyOlpMatrix:
   def Translate(self, x: float, y: float, z: float, withinLocalSystem: bool=True):
      """Translate the matrix.
      
      Args:
         x: the x value
         y: the y value
         z: the z value
         withinLocalSystem: the referring to local system (default = True), False for global
      """
      ...
   
   def RotateX(self, angle: float):
      """Rotate the matrix around x axis.
      
      Args:
         angle: rotation angle
      """
      ...
   
   def RotateY(self, angle: float):
      """Rotate the matrix around y axis.
      
      Args:
         angle: rotation angle
      """
      ...
   
   def RotateZ(self, angle: float):
      """Rotate the matrix around z axis.
      
      Args:
         angle: rotation angle
      """
      ...
   
   def Rotate(self, angle: float, axis: CENPyOlpVector):
      """Rotate the matrix around given axis.
      
      Args:
         angle: rotation angle
         axis: rotation axis
      """
      ...
   
   def GetPosition(self) -> CENPyOlpPoint:
      """Get position of matrix as a point.
      
      Returns:
         position as point
      """
      ...
   
   def GetXDirection(self) -> CENPyOlpVector:
      """Get the matrix x direction as vector.
      
      Returns:
         direction as vector
      """
      ...
   
   def GetYDirection(self) -> CENPyOlpVector:
      """Get the matrix y direction as vector.
      
      Returns:
         direction as vector
      """
      ...
   
   def GetZDirection(self) -> CENPyOlpVector:
      """Get the matrix z direction as vector.
      
      Returns:
         direction as vector
      """
      ...
   
   def Transform(self, pyPointToTransform: CENPyOlpPoint) -> CENPyOlpPoint:
      """Transform a point within this matrix.
      
      Args:
         pyPointToTransform: point to transform
      
      Returns:
         the transformed point
      """
      ...
   
   def GetRotation(self, inDegrees: bool=False) -> tuple:
      """Get rotation angles of this matrix.
      
      Args:
         inDegrees: flag specifying the unit: True = degree, False = radians
      
      Returns:
         output of x, y, z float angle
      """
      ...
   
   def Inverse(self) -> CENPyOlpMatrix:
      """Invert the matrix.
      
      Returns:
         the inverted matrix
      """
      ...
   
   def Multiply(self, pyLeftMatrix: CENPyOlpMatrix, pyRightMatrix: CENPyOlpMatrix) -> CENPyOlpMatrix:
      """Multiply two matrices.
      
      Args:
         pyLeftMatrix: input of left matrix
         pyRightMatrix: input of right matrix
      
      Returns:
         result matrix
      """
      ...
   
   @overload
   def SetRotation(self, firstAxis: CENPyOlpVector, secondAxis: CENPyOlpVector, axesPair: int):
      """Sets the rotational part of the matrix as determined by the two input vectors.
   ///The input vectors are assumed to be orthogonal and normalized.
      
      Args:
         firstAxis: first axis
         secondAxis: second axis
         axesPair: pair of rotation axis
      """
      ...
   
   @overload
   def SetRotation(self, xAxis: CENPyOlpVector, yAxis: CENPyOlpVector, zAxis: CENPyOlpVector):
      """Sets the rotational part of the matrix as determined by three input vectors.
   The input vectors are assumed to be orthogonal normalized.
      
      Args:
         xAxis: the vector for the X axis.
         yAxis: the vector for the Y axis.
         zAxis: the vector for the Z axis.
      """
      ...
   
   def GetDistance(self, otherMatrix: CENPyOlpMatrix) -> float:
      """Gets the distance between the current matrix and the given matrix.
      
      Args:
         otherMatrix: Another matrix.
      
      Returns:
         The distance.
      """
      ...
   
   def IsValid(self) -> bool:
      """Checks if the matrix is valid.
      
      Returns:
         True if the matrix is not None, otherwise False.
      """
      ...
   
   def GetXRotation(self, inDegrees: bool=False) -> float:
      """Get the X rotation angle of this matrix.
      
      Args:
         inDegrees: flag specifying the unit: True = degree, False = radians
      
      Returns:
         X rotation angle
      """
      ...
   
   def GetYRotation(self, inDegrees: bool=False) -> float:
      """Get the Y rotation angle of this matrix.
      
      Args:
         inDegrees: flag specifying the unit: True = degree, False = radians
      
      Returns:
         Y rotation angle
      """
      ...
   
   def GetZRotation(self, inDegrees: bool=False) -> float:
      """Get the Z rotation angle of this matrix.
      
      Args:
         inDegrees: flag specifying the unit: True = degree, False = radians
      
      Returns:
         Z rotation angle
      """
      ...
   
