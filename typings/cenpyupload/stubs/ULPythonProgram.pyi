"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from cenpydownload import DULPythonProgram   
from .ULPythonBaseProfile import *
from .ULPythonController import *
from .ULPythonOperationGroup import *
from .ULPythonSubprogram import *
from .ULPythonToolProfile import *

class ULPythonProgram(DULPythonProgram):

      def SetOperationsGroups(self   , operationGroups: list):
         """Set the operation groups for the program
         
         Args:
            operationGroups: list of ULPythonOperationGroup operation groups to be set
         """
         ...
      
      def SetSubprograms(self   , subprograms: list):
         """Set the sub programs of the program
         
         Args:
            subprograms: list of ULPythonSubprograms subprograms to be set
         """
         ...
      
      def AddOperationGroup(self   , operationGroup: ULPythonOperationGroup):
         """add an operation group to this program
         
         Args:
            operationGroup: operation group ULPythonOperationGroup to be added
         """
         ...
      
      def AddSubprogram(self   , subprogram: ULPythonSubprogram):
         """add a subprogram to this program
         
         Args:
            subprogram: subprogram ULPythonSubprogram to be added
         """
         ...
      
      def SetUsedBaseProfile(self   , baseProfile: ULPythonBaseProfile):
         """Set the used base profile for the program
         
         Args:
            baseProfile: the used base profile object of type  ULPythonBaseProfile
         """
         ...
      
      def SetUsedToolProfile(self   , toolProfile: ULPythonToolProfile):
         """Set the used tool profile for the program
         
         Args:
            toolProfile: the used tool profile object of type  UlPythonToolProfile
         """
         ...
      
      def SetController(self   , controller: ULPythonController):
         """Set the controller for the program
         
         Args:
            controller: controller to be set, object of type ULPythonController
         """
         ...
      
      def SetIsMainProgram(self   , isMain: bool):
         """Set the program status as main or not
         
         Args:
            isMain: if the program is main or not
         """
         ...
      
      def SetName(self   , name: str):
         """Set the name of the program
         
         Args:
            name: name to be set
         """
         ...
      
      def SetAttributes(self   , attributes: list):
         """Set the attributes of the program
         
         Args:
            attributes: attributes to be set
         """
         ...
      
      def AddAttribute(self   , attrib: Core::Python::Attributes::OlpCorePythonAttribute ):
         """Add an attribute to the attribute list
         
         Args:
            attrib: attribute to be added
         """
         ...
      
