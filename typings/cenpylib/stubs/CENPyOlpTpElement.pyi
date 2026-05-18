"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpMatrix import *
from .CENPyOlpTrack import *

class CENPyOlpTpElement:
   def GetName(self) -> str:
      """Get the name of the toolpath element.
      
      Returns:
         Toolpath element name.
      """
      ...
   
   def SetName(self, name: str):
      """Set the name of the toolpath element.
      
      Args:
         name: New toolpath element name.
      """
      ...
   
   def GetTrack(self) -> CENPyOlpTrack:
      """Get the track corresponding to this toolpath element.
      
      Returns:
         Toolpath track.
      """
      ...
   
   def GetProcessType(self) -> int:
      """Get the process type of the toolpath element.
      
      Returns:
         Process type.
      """
      ...
   
   def GetMotionType(self) -> int:
      """Get the motion type of the toolpath element.
      
      Returns:
         Motion type.
      """
      ...
   
   def GetTargetType(self) -> int:
      """Gets the target type of the underlying toolpath element.
      
      Returns:
         Target type.
      """
      ...
   
   def GetConfigBehavior(self) -> int:
      """Gets the config behavior of the underlying toolpath element.
      
      Returns:
         Target type.
      """
      ...
   
   def GetConfigUserString(self) -> str:
      """Gets the config user string of the underlying toolpath element.
      
      Returns:
         Config user string.
      """
      ...
   
   def GetTurnBehavior(self) -> int:
      """Gets the turn behavior of the underlying toolpath element.
      
      Returns:
         Target type.
      """
      ...
   
   def GetTurnUserString(self) -> str:
      """Gets the turn user string of the underlying toolpath element.
      
      Returns:
         Turn user string.
      """
      ...
   
   def GetCollisionStatus(self, includeViaPoint: bool=True) -> int:
      """Gets the collision status of the underlying toolpath element.
      Includes both cost evaluation and simulation results.
      
      Args:
         includeViaPoint: If True Via Point result is also included.
      
      Returns:
         Collision status.
      """
      ...
   
   def GetSimulationCollisionStatus(self) -> int:
      """Gets the collision status of the underlying toolpath element from the simulation.
      
      Returns:
         Collision status.
      """
      ...
   
   def GetReachabilityStatus(self) -> int:
      """Gets the reachability status of the underlying toolpath element.
      
      Returns:
         Reachability status
      """
      ...
   
   def GetSingularityStatus(self) -> int:
      """Gets the singularity status of the underlying toolpath element.
      
      Returns:
         Singularity status
      """
      ...
   
   def GetTeachFlags(self) -> int:
      """Gets the teach flags indicating the modifications made to the underlying toolpath element.
      
      Returns:
         Teach flags.
      """
      ...
   
   def GetMatrix(self) -> CENPyOlpMatrix:
      """Gets the current matrix of the toolpath element.
      
      Returns:
         Current matrix.
      """
      ...
   
   def GetInitialPathMatrix(self) -> CENPyOlpMatrix:
      """Get the initial path matrix which has been saved after PathCompute but before AlignmentCompute.
      
      Returns:
         Initial path matrix.
      """
      ...
   
   def GetInitialPathMatrixTranslatedInBaseFrame(self, x: float, y: float, z: float, index: int) -> CENPyOlpMatrix:
      """Get the initial path matrix moved with the given coordinates relative to the specified base frame.
      
      Args:
         x: The translation in X direction.
         y: The translation in Y direction.
         z: The translation in Z direction.
         index: Base frame index.
      
      Returns:
         Translated initial path matrix.
      """
      ...
   
   def GetGlobalTransformedMatrix(self) -> CENPyOlpMatrix:
      """Get the path matrix which has been saved after global transformation compute in aligned state.
      
      Returns:
         Global transformed path matrix in aligned state.
      """
      ...
   
   def GetBaseFrameTransformedMatrixUnaligned(self) -> CENPyOlpMatrix:
      """Gets the matrix of the toolpath element on a GlobalTransformed compute state without alignment information with respect to base frame.
      
      Returns:
         GlobalTransformed compute state specific matrix - free of alignment
      """
      ...
   
   def GetGlobalTransformedMatrixUnaligned(self) -> CENPyOlpMatrix:
      """Get the path matrix which has been saved after global transformation compute in unaligned state.
      
      Returns:
         Global transformed path matrix in unaligned state.
      """
      ...
   
   def GetInitialNeighbourMatrix(self, next: bool=True) -> CENPyOlpMatrix:
      """Get the next or previous toolpath element, relative to the current one, within the current operation. Default is next.
      
      Args:
         next: True for the next and False for the previous toolpath element.
      
      Returns:
         Matrix of the next or previous toolpath element. None if the start or the end is reached.
      """
      ...
   
   def GetMatrixToActiveBaseFrame(self) -> CENPyOlpMatrix:
      """Get the toolpath element matrix with respect to active (output) base frame.
      
      Returns:
         Matrix relative to active (output) base frame.
      """
      ...
   
   def GetMatrixToBaseFrame(self, index: int) -> CENPyOlpMatrix:
      """Get the toolpath element matrix with respect to the given base frame index.
      
      Args:
         index: Index of the base frame to which this toolpath matrix should be relative.
      
      Returns:
         Matrix relative to the given base frame index.
      """
      ...
   
