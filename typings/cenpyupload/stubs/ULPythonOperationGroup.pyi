"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from cenpydownload import DULPythonOperationGroup   
from .ULPythonBaseProfile import *
from .ULPythonOperation import *
from .ULPythonProgram import *
from .ULPythonToolProfile import *

class ULPythonOperationGroup(DULPythonOperationGroup):

      def SetOperations(self   , operations: list):
         """Set the operations for the operation group
         
         Args:
            operations: operations to be set
         """
         ...
      
      def AddOperation(self   , pyOperation: ULPythonOperation):
         """add an operation to this operation group
         
         Args:
            pyOperation: operation to be added at the end of operations lis of this group
         """
         ...
      
      def SetUsedBaseProfile(self   , pyBaseProfile: ULPythonBaseProfile):
         """Set the used base profile for the operation group
         
         Args:
            pyBaseProfile: used base profile
         """
         ...
      
      def SetUsedToolProfile(self   , pyToolProfile: ULPythonToolProfile):
         """Set the used tool profile for the operation group
         
         Args:
            pyToolProfile: used tool profile
         """
         ...
      
      def SetProgram(self   , pyProgram: ULPythonProgram):
         """Set the parent program for the operation group
         
         Args:
            pyProgram: program to be set
         """
         ...
      
      def SetAttributes(self   , attributes: list):
         """Set the attributes of the operation group
         
         Args:
            attributes: attributes to be set
         """
         ...
      
      def SetName(self   , name: str):
         """Set the name of the profile
         
         Args:
            name: name to be set
         """
         ...
      
      def AddAttribute(self   , attrib: Core::Python::Attributes::OlpCorePythonAttribute ):
         """Add an attribute to the attribute list
         
         Args:
            attrib: attribute to be added
         """
         ...
      
