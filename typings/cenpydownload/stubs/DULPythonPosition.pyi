"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from .DULPythonJoint import *
from cenpyolpcore import OlpCorePythonProgramComponent
from .ProcessType import ProcessType
from .TargetType import TargetType

class DULPythonPosition(OlpCorePythonProgramComponent):
      def GetXYZ(self) -> tuple:
         """Gets position
         
         Returns:
            tuple of double containing position values
         """
         ...
      
      def GetOrientation(self) -> tuple:
         """Gets orientation
         
         Returns:
            tuple of double containing rotation angles values
         """
         ...
      
      def GetConfig(self) -> str:
         """Gets position config
         
         Returns:
            config string
         """
         ...
      
      def GetTurn(self) -> str:
         """Gets turn value
         
         Returns:
            turn value string
         """
         ...
      
      def GetAllJointValues(self) -> list[DULPythonJoint]:
         """Gets the vector of all joints and joint values
         
         Returns:
            returns list[tuple[DULPythonJoint, float]] for all joint values
         """
         ...
      
      def GetMainJointValues(self) -> list[DULPythonJoint]:
         """Gets the vector of main joints and joint values
         
         Returns:
            returns list[tuple[DULPythonJoint, float]] for main joint values
         """
         ...
      
      def GetExternalJointValues(self) -> list[DULPythonJoint]:
         """Gets the vector of external joints and joint values
         
         Returns:
            returns list[tuple[DULPythonJoint, float]] for external joint values
         """
         ...
      
      def GetProcessType(self) -> ProcessType:
         """Gets process type
         
         Returns:
            process type
         """
         ...
      
      def GetTargetType(self) -> TargetType:
         """Gets target type
         
         Returns:
            target type
         """
         ...
      
