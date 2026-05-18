"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribCreator import *
from .CENPyOlpEvent_PEOperator import *
from .CENPyOlpMatrix import *
from .CENPyOlpPoint import *
from .CENPyOlpTpElement import *
from .CENPyOlpVector import *

class CENPyOlpEvent_PEOperatorUpload(CENPyOlpEvent_PEOperator):
   def SetComputationStateMatrix(self, tpe: CENPyOlpTpElement, computeStateMatrix: int, newMatrix: CENPyOlpMatrix):
      """Sets one of the matrices of TPE depending on given state
      
      Args:
         tpe: TPE to set matrix
         computeStateMatrix: state to set matrix to
         newMatrix: new Matrix
      """
      ...
   
   def CreateMatrix(self) -> CENPyOlpMatrix:
      """Creates a new unit matrix
      
      Returns:
         Newly created unit matrix
      """
      ...
   
   def CreatePoint(self, x: float, y: float, z: float) -> CENPyOlpPoint:
      """Creates a point with the given coordinates
      
      Args:
         x: x-coordinate
         y: y-coordinate
         z: z-coordinate
      
      Returns:
         Newly created point
      """
      ...
   
   def CreateVector(self, x: float, y: float, z: float) -> CENPyOlpVector:
      """Creates a vector with the given coordinates
      
      Args:
         x: x-coordinate
         y: y-coordinate
         z: z-coordinate
      
      Returns:
         Newly created vector
      """
      ...
   
   def GetOperationAttribCreator(self) -> CENPyOlpAttribCreator:
      """Get attribute creator of event operation
      
      Returns:
         Attribute creator of event operation
      """
      ...
   
