"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from .DULPythonBaseProfile import *
from .DULPythonToolProfile import *
from cenpyolpcore import OlpCorePythonOperationGroup

class DULPythonOperationGroup(OlpCorePythonOperationGroup):
      def GetOperations(self) -> list:
         """Gets all operations
         
         Returns:
            returns a list containing all operations of this group
         """
         ...
      
      def GetUsedBaseProfile(self) -> DULPythonBaseProfile:
         """Gets used base profile (if not set in program)
         
         Returns:
            returns the uses base profile
         """
         ...
      
      def GetUsedToolProfile(self) -> DULPythonToolProfile:
         """Gets used tool profile (if not set in program)
         
         Returns:
            returns the used tool profile
         """
         ...
      
