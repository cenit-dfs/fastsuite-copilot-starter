"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpController import *
from .CENPyOlpLogOperator import *
from .CENPyOlpMatrix import *

class CENPyOlpEvent_PEOperator:
   def GetAttribGetter(self) -> CENPyOlpAttribGetter:
      """Get attribute getter interface.
      
      Returns:
         Attribute getter interface.
      """
      ...
   
   def GetAttribSetter(self) -> CENPyOlpAttribSetter:
      """Get attribute setter interface
      
      Returns:
         Attribute setter interface
      """
      ...
   
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Get logger operator.
      
      Returns:
         Logger operator.
      """
      ...
   
   def GetRefToolpathElementPosition(self) -> CENPyOlpMatrix:
      """Determines the base frame position of the reference element of an event.
      Be aware: This will return nullptr if it is not called on an OlpEventDefinition.
      
      Returns:
         Nullptr or the base frame position of the reference toolpath element.
      """
      ...
   
   def GetCurrentToolFrameIndex(self) -> int:
      """Get the current tool frame index of the reference TPE.
      
      Returns:
         Tool frame index.
      """
      ...
   
   def GetCurrentBaseFrameIndex(self) -> int:
      """Get the current base frame index of the reference TPE.
      
      Returns:
         Base frame index.
      """
      ...
   
   def GetCurrentToolFrameMatrix(self) -> CENPyOlpMatrix:
      """Get the current tool frame matrix of the reference TPE.
      
      Returns:
         Tool frame matrix.
      """
      ...
   
   def GetCurrentBaseFrameMatrix(self) -> CENPyOlpMatrix:
      """Get the current base frame matrix of the reference TPE.
      
      Returns:
         Base frame matrix.
      """
      ...
   
   def GetTechTabFolder(self) -> int:
      """Gets the technology table folder path.
      If the relative path contains a file name with extension then it will return the path to that file.
      
      Args:
         relativePath: Name of a file/relative path to a file.
         feedbackErrorWhenFileNotFound: By default (True) a feedback error is passed when file not found.
      
      Returns:
         Technology table folder or a file path.
      """
      ...
   
   def IsEventCreatedAutomatically(self) -> bool:
      """Get if the reference Event was created by a rule, another event, or inserted manually.
      
      Returns:
         True if the Event was created by a rule or by another Event, False if inserted manually.
      """
      ...
   
   def GetController(self) -> CENPyOlpController:
      """Get OLP controller.
      
      Returns:
         OLP controller.
      """
      ...
   
