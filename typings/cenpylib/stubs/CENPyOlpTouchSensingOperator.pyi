"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpMatrix import *

class CENPyOlpTouchSensingOperator:
   def GetCollisionPoint(self, frame: int) -> CENPyOlpMatrix:
      """Get collision point matrix.
      
      Args:
         frame: Touch direction along Normal (0) or BaseFrame (1).
      
      Returns:
         Collision point matrix.
      """
      ...
   
   def GetStartPoint(self, frame: int) -> CENPyOlpMatrix:
      """Get start point matrix.
      
      Args:
         frame: Touch direction along Normal (0) or BaseFrame (1).
      
      Returns:
         Start point matrix.
      """
      ...
   
   def GetEndPoint(self, frame: int) -> CENPyOlpMatrix:
      """Get end point matrix.
      
      Args:
         frame: Touch direction along Normal (0) or BaseFrame (1).
      
      Returns:
         End point matrix.
      """
      ...
   
   def GetReferencePoint(self) -> CENPyOlpMatrix:
      """Get reference point matrix.
      
      Returns:
         Reference point matrix.
      """
      ...
   
   def SetTouchStartDistance(self, startDist: float):
      """Set touch start distance.
      
      Args:
         startDist: Offset reference point in direction of the surface normal.
      """
      ...
   
   def SetTouchEndDistance(self, endDist: float):
      """Set touch end distance
      
      Args:
         endDist: Offset reference point in minus direction of the surface normal
      """
      ...
   
   def TouchPointCompute(self):
      """Compute touch point.
      """
      ...
   
   def GetTouchLocationType(self) -> int:
      """Calculate touch point near PG start or end.
      
      Returns:
         Touch location type: AtStart (1) or AtEnd (2).
      """
      ...
   
   def GetLastTouchDir(self) -> int:
      """Get last touch direction.
      
      Returns:
         BaseFrame touch axis: Undefined (0), XMinus (1), XPlus (2), YMinus (3), YPlus (4), ZMinus (5), ZPlus (6).
      """
      ...
   
