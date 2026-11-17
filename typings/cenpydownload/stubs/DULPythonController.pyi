"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .DULPythonProgram import *
from cenpyolpcore import OlpCorePythonController

class DULPythonController(OlpCorePythonController):
      def GetActiveProgram(self) -> DULPythonProgram:
         """Gets the active program on this controller
         
         Returns:
            returns the active program as IDULProgram
         """
         ...
      
      def GetOutputDirectory(self) -> str:
         """Gets the controller's output directory for downloaded program files
         
         Returns:
            returns the path to the controller's output directory
         """
         ...
      
      def GetTemporaryOutputDirectory(self) -> str:
         """Gets the controller's temporary output directory for downloaded program files
         
         Returns:
            returns the path to the controller's temporary output directory
         """
         ...
      
      def GetTechTabFolder(self   , relativePath: str) -> str:
         """Gets the technology table folder
      If the relative path contains a file name with extension then it will return the path to that file
         
         Args:
            relativePath: Relative path or only filename to search for in plug-in folders
         
         Returns:
            technology table folder or TechTab file location
         """
         ...
      
      def GetConnectedJoints(self) -> list:
         """Gets all connected joints. Mains and externals are not separated
         
         Returns:
            returns a list of all connected joints
         """
         ...
      
      def GetToolProfiles(self) -> list:
         """Gets all tool profiles
         
         Returns:
            returns a list containing all tool profiles
         """
         ...
      
      def GetBaseProfiles(self) -> list:
         """Gets all base profiles
         
         Returns:
            returns a list containing all base profiles
         """
         ...
      
      def GetAccuracyProfiles(self) -> list:
         """Gets all accuracy profiles
         
         Returns:
            returns a list containing all accuracy profiles
         """
         ...
      
      def GetMotionProfiles(self) -> list:
         """Gets all motion profiles
         
         Returns:
            returns a list containing all motion profiles
         """
         ...
      
