"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpMatrix import *

class CENPyOlpSeamFindingOperator:
   def GetSeamFindingPoint(self, atEnd: bool, optDir: bool, distance: float) -> CENPyOlpMatrix:
      """Get SeamFinding Start Point
      
      Args:
         atEnd: Finding Operation at End is True
         optDir: Optional Direction, approach from the other Side
         distance: Distance in Length from Start/End
      
      Returns:
         return the point matrix
      """
      ...
   
   def GetSeamTrackingPoint(self, distance: float) -> CENPyOlpMatrix:
      """Get SeamTracking Start Point
      
      Args:
         distance: Distance from Start/End
      
      Returns:
         return the point matrix
      """
      ...
   
   def SeamFindingApproachRetractPoint(self, initialMatrix: CENPyOlpMatrix, dx: float, dy: float, dz: float) -> CENPyOlpMatrix:
      """Returns an Approach or Retract Point which takes :<br/>
      the WORK Angle as CycleRotation::ROT_PATH_TOOL<br/>
      the TRAVEL Angle as CycleRotation::ROT_TOOL (alternative: ROT_PATH_TOOL use SeamFindingApproachRetractPointAlt)<br/>
      the TOOL Angle as CycleRotation::ROT_TOOL<br/>
      Note : Event has to be set to CycleRotation::ROT_TOOL
      
      Args:
         initialMatrix: the Matrix of the Base Point
         dx: Approach/Retract Distance in X
         dy: Approach/Retract Distance in Y
         dz: Approach/Retract Distance in Z
      
      Returns:
         return the point matrix
      """
      ...
   
   def SeamFindingApproachRetractPointAlt(self, initialMatrix: CENPyOlpMatrix, dx: float, dy: float, dz: float) -> CENPyOlpMatrix:
      """Returns an Approach or Retract Point which takes :<br/>
      the WORK Angle as CycleRotation::ROT_PATH_TOOL<br/>
      the TRAVEL Angle as CycleRotation::ROT_PATH_TOOL (alternative: ROT_TOOL use SeamFindingApproachRetractPoint)<br/>
      the TOOL Angle as CycleRotation::ROT_TOOL<br/>
      Note : Event has to be set to CycleRotation::ROT_TOOL
      
      Args:
         initialMatrix: the Matrix of the Base Point
         dx: Approach/Retract Distance in X
         dy: Approach/Retract Distance in Y
         dz: Approach/Retract Distance in Z
      
      Returns:
         return the point matrix
      """
      ...
   
