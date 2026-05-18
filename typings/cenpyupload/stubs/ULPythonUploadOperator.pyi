"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from cenpyolpcore import OlpCorePythonBaseOperator 
from .ULPythonBaseProfile import *
from .ULPythonController import *
from .ULPythonEvent import *
from .ULPythonMotion import *
from .ULPythonOperation import *
from .ULPythonOperationGroup import *
from .ULPythonPosition import *
from .ULPythonProgram import *
from .ULPythonSubprogram import *
from .ULPythonToolProfile import *

class ULPythonUploadOperator(OlpCorePythonBaseOperator):

      def GetSourceFiles(self) -> list:
         """Gets all source files that are selected for the current upload run
         
         Returns:
            returns a list of strings containing paths to all source files
         """
         ...
      
      def CreateEmptyProgram(self) -> ULPythonProgram:
         """Creates a new empty program
         
         Returns:
            returns the newly created program as ULPythonProgram
         """
         ...
      
      def GetCreatedPrograms(self) -> list:   ...
      def CreateEmptySubprogram(self) -> ULPythonSubprogram:
         """Creates an empty subprogram
         
         Returns:
            returns the newly created subprogram call as ULPythonSubprogram
         """
         ...
      
      def GetCreatedSubprograms(self) -> list:   ...
      def CreateEmptyOperationGroup(self) -> ULPythonOperationGroup:
         """Creates an operation group
         
         Returns:
            returns the newly created operation group as ULPythonOperationGroup
         """
         ...
      
      def GetCreatedOperationGroups(self) -> list:   ...
      def CreateEmptyOperation(self) -> ULPythonOperation:
         """Creates an operation
         
         Returns:
            returns the newly created operation as ULPythonOperation
         """
         ...
      
      def GetCreatedOperations(self) -> list:   ...
      def CreateEmptyMotion(self) -> ULPythonMotion:
         """Creates an empty motion objects
         
         Returns:
            returns the newly created motion as ULPythonMotion
         """
         ...
      
      def GetCreatedMotions(self) -> list:   ...
      def CreateEmptyPosition(self) -> ULPythonPosition:
         """Creates an empty position object
         
         Returns:
            returns the newly created position as ULPythonPosition
         """
         ...
      
      def GetCreatedPositions(self) -> list:   ...
      def CreateEmptyEvent(self) -> ULPythonEvent:
         """Creates an empty event
         
         Returns:
            returns the newly created event as ULPythonEvent
         """
         ...
      
      def GetCreatedEvents(self) -> list:   ...
      def CreateEmptyToolProfile(self) -> ULPythonToolProfile:
         """Creates an empty tool profile
         
         Returns:
            returns the newly created tool profile as ULPythonToolProfile
         """
         ...
      
      def GetCreatedToolProfiles(self) -> list:   ...
      def CreateEmptyBaseProfile(self) -> ULPythonBaseProfile:
         """Creates an empty base profile
         
         Returns:
            returns the newly created base profile as ULPythonBaseProfile
         """
         ...
      
      def CreateOlpBaseFrameProfileFromPositionRotation(self, baseProfileName: str, x: float, y: float, z: float, rX: float, rY: float, rZ: float) -> ULPythonBaseProfile:
         """Creates new olp base frame and Base profile
         
         Args:
            baseProfileName: The name of relative profile
            x: X offset
            y: Y offset
            z: Z offset
            rX: rX rotation
            rY: rY rotation
            rZ: rZ rotation
         
         Returns:
            a Base profile or null object
         """
         ...
      
      def CreateOlpBaseFrameProfileFromMatrix(self, baseProfileName: str,  matrix: list[float]) -> ULPythonBaseProfile:
         """Creates new olp base frame and Base profile
         
         Args:
            baseProfileName: The name of relative profile
            matrix: >Matrix represented by double array[16]
         
         Returns:
            a Base profile or null object
         """
         ...
      
      def GetCreatedBaseProfiles(self) -> list:   ...
      def GetController(self) -> ULPythonController:
         """Gets the controller attached to this instance of the upload operator
         
         Returns:
            returns the active controller for download
         """
         ...
      
      def GetAttributeSetterOperator(self) -> OlpCorePythonAttributeSetterOperator *:
         """Gets the attributes setters operator
         
         Returns:
            returns the attributes setters operator
         """
         ...
      
