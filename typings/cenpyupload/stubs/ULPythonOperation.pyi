"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from cenpydownload import DULPythonOperation   
from .DULPythonBaseProfile import *
from .ULPythonMotion import *
from .ULPythonOperationGroup import *
from .DULPythonToolProfile import *

class ULPythonOperation(DULPythonOperation):

      def SetMotions(self   , motions: list):
         """Set the motions for the operation
         
         Args:
            motions: list of motions to be set
         """
         ...
      
      def AddMotion(self   , motion: ULPythonMotion):
         """add a motion to the operation
         
         Args:
            motion: motion to be added
         """
         ...
      
      def SetUsedBaseProfile(self   , baseProfile: DULPythonBaseProfile):
         """Set the used based profile for the motion
         
         Args:
            baseProfile: used base profile
         """
         ...
      
      def SetUsedToolProfile(self   , toolProfile: DULPythonToolProfile):
         """Set the used tool profile for the motion
         
         Args:
            toolProfile: used tool profile
         """
         ...
      
      def SetOperationGroup(self   , parentOperationGroup: ULPythonOperationGroup):
         """Set the parent operation group for the motion
         
         Args:
            parentOperationGroup: the parent operation group
         """
         ...
      
      def SetAttributes(self   , attributes: list):
         """Set the attributes of the operation
         
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
      
