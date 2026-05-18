"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from cenpydownload import DULPythonBaseProfile   
from .ULPythonBaseProfile import *

class ULPythonBaseProfile(DULPythonBaseProfile):

      def SetReferenceProfile(self   , pyRefProfile: ULPythonBaseProfile):
         """Set the reference profile for this profile
         
         Args:
            pyRefProfile: ref profile to be set
         """
         ...
      
      def SetXYZ(self   , offsetPosTuple: list):
         """Set the offset position for the base profile
         
         Args:
            offsetPosTuple: offset position to be set; a tuple of three doubles representing (x, y, z) coordinates in meters.
         """
         ...
      
      def SetOrientation(self   , offsetOrientation: list):
         """Set the offset rotation for the base profile
         
         Args:
            offsetOrientation: offset rotation to be set
         """
         ...
      
      def SetIndex(self   , index: int):
         """Set the profile index
         
         Args:
            index: index to be set
         """
         ...
      
      def SetName(self   , name: str):
         """Set the name of the profile
         
         Args:
            name: name to be set
         """
         ...
      
