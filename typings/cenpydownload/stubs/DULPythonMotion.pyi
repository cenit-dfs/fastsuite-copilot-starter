"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from .MotionType import MotionType
from .DULPythonPosition import *
from cenpyolpcore import OlpCorePythonProgramComponent

class DULPythonMotion(OlpCorePythonProgramComponent):
      def GetPosition(self) -> DULPythonPosition:
         """Gets motion position
         
         Returns:
            returns position of this motion
         """
         ...
      
      def GetViaPosition(self) -> DULPythonPosition:
         """Gets motion via position
         
         Returns:
            returns position of this motion
         """
         ...

      def GetMotionType(self) -> MotionType:
         """Gets motion type of this motion
         
         Returns:
            returns motion type of this motion
         """
         ...
      
      def IsCircularMotion(self) -> bool:
         """Gets the flag indicating a circular motion
         
         Returns:
            returns True if motion is circular, False otherwise
         """
         ...
      
      def IsLinearMotion(self) -> bool:
         """Gets the flag indicating a linear motion
         
         Returns:
            returns True if motion is linear, False otherwise
         """
         ...
      
      def IsReferenceMotion(self) -> bool:
         """Gets the flag indicating a reference motion
         
         Returns:
            returns True if motion is event suppressed, False otherwise
         """
         ...
      
      def IsPtPMotion(self) -> bool:
         """Gets the flag indicating a point-to-point motion
         
         Returns:
            returns True if motion is PtP, False otherwise
         """
         ...
      
      def GetEventsBefore(self) -> list:
         """Gets list of events executed before
         
         Returns:
            before events list
         """
         ...
      
      def GetEventsAfter(self) -> list:
         """Gets list of events executed after
         
         Returns:
            after events list
         """
         ...
      
