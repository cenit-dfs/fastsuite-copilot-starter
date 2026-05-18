"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from .DULPythonCommonProfile import *
from .ToolType import ToolType

class DULPythonToolProfile(DULPythonCommonProfile):
      def GetXYZ(self) -> tuple:
         """Gets tcp offset position
         
         Returns:
            tcp offset position
         """
         ...
      
      def GetOrientation(self) -> tuple:
         """Gets tcp offset rotation
         
         Returns:
            offset rotation
         """
         ...
      
      def GetToolType(self) -> ToolType:
         """Gets tool type
         
         Returns:
            tool type
         """
         ...

      def IsVisionFrame(self) -> bool:
         """Gets the flag indicating whether or not this profile represents a vision frame
         
         Returns:
            returns True if the profile represents a vision frame
         """
         ...
      
