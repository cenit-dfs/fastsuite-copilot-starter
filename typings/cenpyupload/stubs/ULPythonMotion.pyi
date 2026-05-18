"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from cenpydownload import DULPythonMotion   
from .ULPythonEvent import *
from .ULPythonOperation import *
from .ULPythonPosition import *

class ULPythonMotion(DULPythonMotion):

      def SetOperation(self   , operation: ULPythonOperation):
         """Set the motion operation
         
         Args:
            operation: operation to be set
         """
         ...
      
      def SetPosition(self   , position: ULPythonPosition):
         """Set the motion's position
         
         Args:
            position: position to be set
         """
         ...
      
      def SetViaPosition(self   , viaPosition: ULPythonPosition):
         """Set the motion's via position
         
         Args:
            viaPosition: via position to be set
         """
         ...
      
      def SetMotionType(self   , motionType: int):
         """Set motion type
         
         Args:
            motionType: motion type
         """
         ...
      
      def SetEventsBefore(self   , eventsBefore: list):
         """Set the events before for the motion
         
         Args:
            eventsBefore: before events to be set
         """
         ...
      
      def SetEventsAfter(self   , eventsAfter: list):
         """Set the after events for the motion
         
         Args:
            eventsAfter: after events to be set
         """
         ...
      
      def AddEventBefore(self   , event: ULPythonEvent):
         """Adds an event for this motion, at the end of events list positioned before
         
         Args:
            event: event to add before this motion
         """
         ...
      
      def AddEventAfter(self   , event: ULPythonEvent):
         """Adds an event for this motion, at the end of events positioned after
         
         Args:
            event: event to add after this motion
         """
         ...
      
      def SetAttributes(self   , attributes: list):
         """Set the attributes of the motion
         
         Args:
            attributes: attributes to be set
         """
         ...
      
      def SetName(self   , name: str):
         """Set the name for the motion
         
         Args:
            name: name to be set
         """
         ...
      
