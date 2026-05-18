"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from .DULPythonBaseProfile import *
from .DULPythonToolProfile import *
from cenpyolpcore import OlpCorePythonOperation

class DULPythonOperation(OlpCorePythonOperation):
      def GetMotions(self) -> list:
         """Gets the vector of the motions for this operation
         
         Returns:
            returns the vector of the motions
         """
         ...
      
      def GetUsedBaseProfile(self) -> DULPythonBaseProfile:
         """Gets used base profile(if not set in program or group)
         
         Returns:
            returns the vector of the attributes
         """
         ...
      
      def GetUsedToolProfile(self) -> DULPythonToolProfile:
         """Gets used tool profile(if not set in program or group)
         
         Returns:
            returns the vector of the attributes
         """
         ...
      
