"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from cenpydownload import DULPythonPosition   
from .ULPythonMotion import *

class ULPythonPosition(DULPythonPosition):

      def SetMotion(self   , motion: ULPythonMotion):
         """Set the motion for current position
         
         Args:
            motion: motion to be set
         """
         ...
      
      def SetXYZ(self   , position: list):
         """Set the position's coordinates
         
         Args:
            position: A tuple of three doubles representing (x, y, z) coordinates in meters.
         """
         ...
      
      def SetOrientation(self   , orientation: list):
         """Set the position's orientation
         
         Args:
            orientation: A tuple of three doubles representing (Rx, Ry, Rz) rotation angles in degrees.
         """
         ...
      
      def SetConfig(self   , config: str):
         """Set the position config
         
         Args:
            config: config to be set
         """
         ...
      
      def SetTurn(self   , turn: str):
         """Set the turn for the position
         
         Args:
            turn: turn to be set
         """
         ...
      
      def SetProcessType(self   , processType: int):
         """Set the process type of the position
         
         Args:
            processType: process type to be set
         """
         ...
      
      def SetTargetType(self   , targetType: int):
         """Set the target type of the position
         
         Args:
            targetType: target type to be set
         """
         ...
      
      def SetExplicitMainJointValues(self   , mainJointValues: list):
         """Set explicit the main joint values on each joint for the position
         
         Args:
            mainJointValues: main values to be set, input argument is a vector of pairs : the joint object and its value list[tuple[DULPythonJoint, float]]
         """
         ...
      
      def SetExplicitExternalJointValues(self   , externalJointValues: list):
         """Set explicit the external joint values for the position on each external joint
         
         Args:
            externalJointValues: external joint values to be set, input argument is a vector of pairs : the joint object and its double value
         """
         ...
      
      def SetAttributes(self   , attributes: list):
         """Set the attributes of the position
         
         Args:
            attributes: attributes to be set
         """
         ...
         
      def SetName(self   , name: str):
         """Set the name of the position
         
         Args:
            name: name to be set
         """
         ...
      
