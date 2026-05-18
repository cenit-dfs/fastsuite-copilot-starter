"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from .DULPythonController import *
from cenpyolpcore import OlpCorePythonBaseOperator

class DULPythonDownloadOperator(OlpCorePythonBaseOperator):
      def GetController(self) -> DULPythonController:
         """Gets the controller attached to this instance of the download operator
         
         Returns:
            returns the active controller for download
         """
         ...
      
      def AddOutputFilePath(self   , filePath: str):
         """Adds the given file path to the list of created output files
         
         Args:
            filePath: filepath to the created output file
         """
         ...
      
