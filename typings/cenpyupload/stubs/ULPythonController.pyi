"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from cenpydownload import DULPythonController   
from .ULPythonBaseProfile import *
from .ULPythonProgram import *
from .ULPythonToolProfile import *

class ULPythonController(DULPythonController):

      def SetActiveProgram(self   , pyProgram: ULPythonProgram):
         """Set the program for the controller
         
         Args:
            pyProgram: program to be set
         """
         ...
      
      def SetToolProfiles(self   , toolProfiles: list):
         """Set the tool profiles for the controller
         
         Args:
            toolProfiles: tool profiles to be set
         """
         ...
      
      def SetBaseProfiles(self   , baseProfiles: list):
         """Set the base profiles for the controller
         
         Args:
            baseProfiles: base profiles to be set
         """
         ...
      
      def AddBaseProfile(self   , profileToAdd: ULPythonBaseProfile):
         """add a base profile at the end of base profiles list
         
         Args:
            profileToAdd: base profile to be added
         """
         ...
      
      def AddToolProfile(self   , profileToAdd: ULPythonToolProfile):
         """add a tool profile at the end of tool profiles list
         
         Args:
            profileToAdd: tool profile to be added
         """
         ...
      
