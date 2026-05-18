"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""


class CENPyOlpJoint:
   def GetName(self) -> str:
      """Get the joint name.
      
      Returns:
         Joint name.
      """
      ...
   
   def GetKinType(self) -> int:
      """Returns the kinematic type of a joint
      
      Returns:
         kinematic type
      """
      ...
   
   def GetJointType(self) -> int:
      """Returns the joint type
      
      Returns:
         joint type
      """
      ...
   
   def GetJointIndex(self) -> int:
      """The joint index results out of the sum of the RSIM-index for main joints and external joints,
      whereby main joints start at 1 and the externals continue after the last main joint.
      
      Returns:
         Joint index
      """
      ...
   
   def GetMinPos(self) -> float:
      """Returns joint minimum position
      
      Returns:
         Minimum
      """
      ...
   
   def GetMaxPos(self) -> float:
      """Returns joint maximum position
      
      Returns:
         Maximum
      """
      ...
   
   def GetCurrentPos(self) -> float:
      """Returns joint actual position
      
      Returns:
         Actual
      """
      ...
   
