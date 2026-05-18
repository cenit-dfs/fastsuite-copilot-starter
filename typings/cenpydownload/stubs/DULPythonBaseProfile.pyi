"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from .DULPythonCommonProfile import *

class DULPythonBaseProfile(DULPythonCommonProfile):
      def GetReferenceProfile(self) -> DULPythonBaseProfile:
         """reference frame
         
         Returns:
            world or other base frame
         """
         ...
      
      def GetXYZ(self) -> tuple:
         """Gets offset position to reference profile
         
         Returns:
            returns offset position to reference profile
         """
         ...
      
      def GetOrientation(self) -> tuple:
         """Gets offset rotation to reference profile
         
         Returns:
            returns offset rotation to reference profile
         """
         ...
      
