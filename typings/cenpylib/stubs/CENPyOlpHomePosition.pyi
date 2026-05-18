"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpJoint import *

class CENPyOlpHomePosition:
   def GetName(self) -> str:
      """Get name of the home position.
      
      Returns:
         home position's name
      """
      ...
   
   def GetCount(self) -> int:
      """Get the number of joints/positions in this Home Position
      
      Returns:
         Returns the number of joints/position in this Home Position
      """
      ...
   
   def GetJointAt(self, index: int) -> CENPyOlpJoint:
      """Get the joint at specified index
      
      Args:
         index: Index of the joint
      
      Returns:
         Returns the joint at the desired position
      """
      ...
   
   def GetPositionAt(self, index: int, isKinematicSpecific: bool) -> float:
      """Gets the position of a joint at a specific index.
      
      Args:
         index: the index of the joint to get the position from
         isKinematicSpecific: If No, the returned position is the mathematical value. If Yes, it is computed according to the resource's kinematic conventions.
      
      Returns:
         Returns the joint at the desired position computed according to the resource's kinematic conventions.
      """
      ...
   
   def GetPositionOf(self, joint: CENPyOlpJoint, isKinematicSpecific: bool) -> float:
      """Gets the position of a given joint.
      
      Args:
         joint: The joint whose position to get
         isKinematicSpecific: If No, the returned position is the mathematical value. If Yes, it is computed according to the resource's kinematic conventions.
      
      Returns:
         The position of a given joint.
      """
      ...
   
