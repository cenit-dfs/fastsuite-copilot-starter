"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from cenpydownload import DULPythonEvent   
from .ULPythonMotion import *

class ULPythonEvent(DULPythonEvent):

      def SetMotions(self   , pyMotions: list):
         """Set the motions for the event
         
         Args:
            pyMotions: motions to be set
         """
         ...
      
      def AddMotion(self   , motion: ULPythonMotion):
         """add a motion to the event
         
         Args:
            motion: motion to be added
         """
         ...
      
      def SetAttributes(self   , attributes: list):
         """Set the attributes of the event
         
         Args:
            attributes: attributes to be set
         """
         ...
      
      def SetName(self   , name: str):
         """Set the name for the program component
         
         Args:
            name: name to be set
         """
         ...
      
      def SetInsertPosition(self   , insertPosition: int):
         """Sets the insert position for this event
         
         Args:
            insertPosition: new insert position
         """
         ...
      
      def AddAttribute(self   , attrib: Core::Python::Attributes::OlpCorePythonAttribute ):
         """Add an attribute to the attribute list
         
         Args:
            attrib: attribute to be added
         """
         ...
      
