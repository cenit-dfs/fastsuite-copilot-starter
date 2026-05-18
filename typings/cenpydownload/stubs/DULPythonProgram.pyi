"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from .DULPythonBaseProfile import *
from .DULPythonOperationGroup import *
from .DULPythonSubprogram import *
from .DULPythonToolProfile import *
from cenpyolpcore import OlpCorePythonProgram

class DULPythonProgram(OlpCorePythonProgram):
      def GetUsedBaseProfile(self) -> DULPythonBaseProfile:
         """Gets the program wide base profile, if set.
         
         Returns:
            returns the used BaseProfile if set for the entire program, None otherwise
         """
         ...
      
      def GetUsedToolProfile(self) -> DULPythonToolProfile:
         """Gets the program wide tool profile, if set.
         
         Returns:
            returns the used ToolProfile if set for the entire program, None otherwise
         """
         ...
      
      def GetOperationGroups(self) -> list[DULPythonOperationGroup]:
         """Gets all operation groups
         
         Returns:
            returns a list of DULPythonOperationGroup containing all operation groups
         """
         ...
      
      def GetSubprograms(self) -> list[DULPythonSubprogram]:
         """Gets all subprograms
         
         Returns:
            returns a list of DULPythonSubprogram containing all subprograms
         """
         ...
      
      def GetGroupsAndSubprograms(self) -> list:
         """Gets all operation groups and subprograms
         
         Returns:
            returns a list of all operation groups and subprograms
         """
         ...
      
