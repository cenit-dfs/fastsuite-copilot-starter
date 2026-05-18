"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from .DULPythonProgram import *
from cenpyolpcore import OlpCorePythonSubprogram

class DULPythonSubprogram(OlpCorePythonSubprogram):
      def GetCallingProgram(self) -> DULPythonProgram:
         """Gets the program initiating the call
         
         Returns:
            returns the calling program
         """
         ...
      
      def GetCalledProgram(self) -> DULPythonProgram:
         """Gets the program that is called by the calling program
         
         Returns:
            returns the called program
         """
         ...
      
