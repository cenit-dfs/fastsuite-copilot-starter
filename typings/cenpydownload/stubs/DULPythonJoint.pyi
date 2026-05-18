"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from .JointConstellationRole import JointConstellationRole
from .JointKinematicType import JointKinematicType

class DULPythonJoint:
      def GetName(self) -> str:
         """Gets the joint name.
         
         Returns:
            returns the joint name as string
         """
         ...
      
      def GetDofNumber(self) -> int:
         """Gets the DOF index.
         
         Returns:
            returns the dof number
         """
         ...
      
      def GetJointIndex(self) -> int:
         """Gets the joint index starting from base 1.
         
         Returns:
            returns the joint index as int
         """
         ...
      
      def GetJointGroupIndex(self) -> int:
         """Gets joint group index.
         
         Returns:
            returns the joint group index as int
         """
         ...
      
      def GetJointType(self) -> JointKinematicType:
         """Gets the joint type.
         
         Returns:
            returns the joint type
         """
         ...
      
      def GetUnit(self) -> str:
         """Gets the joint unit.
         
         Returns:
            returns the joint unit as string
         """
         ...
      
      def GetPortName(self) -> str:
         """Gets joint port name.
         
         Returns:
            returns the joint part name as string
         """
         ...
      
      def IsExternal(self) -> bool:
         """Gets the information whether or not the joint is an external one.
         
         Returns:
            returns True if joint is external, False otherwise.
         """
         ...
      
      def GetJointRole(self) -> JointConstellationRole:
         """Gets the role of this joint
         
         Returns:
            returns what role the joint has. See JointConstellationRole for details.
         """
         ...
      
