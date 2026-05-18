"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpController import *
from .CENPyOlpLogOperator import *
from .CENPyOlpMatrix import *
from .CENPyOlpProcessGeometryOperator import *

class CENPyOlpWM_SyncPgAttribOperator:
   def GetAttribGetter(self) -> CENPyOlpAttribGetter:
      """Get attribute getter interface which handles the Olp attribute container.
      
      Returns:
         Attribute getter interface.
      """
      ...
   
   def GetAttribSetter(self) -> CENPyOlpAttribSetter:
      """Get attribute setter interface which handles the Olp attribute container.
      
      Returns:
         Attribute setter interface.
      """
      ...
   
   def GetEventAttribGetter(self, eventName: str) -> CENPyOlpAttribGetter:
      """Get event attribute getter interface which handles the Olp attribute container of the event definition.
      
      Returns:
         Attribute getter interface of the event.
      """
      ...
   
   def GetEventAttribSetter(self, eventName: str) -> CENPyOlpAttribSetter:
      """Get event attribute setter interface which handles the Olp attribute container of the event definition.
      
      Returns:
         Attribute setter interface of the event.
      """
      ...
   
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Get the log operator interface.
      
      Returns:
         Log operator interface.
      """
      ...
   
   def GetCurrentProcessGeometryOperator(self) -> CENPyOlpProcessGeometryOperator:
      """Get the process geometry operator of the parent operation.
      
      Returns:
         Process geometry operator.
      """
      ...
   
   def GetController(self) -> CENPyOlpController:
      """Get the parent controller interface.
      
      Returns:
         Controller interface.
      """
      ...
   
   def GetCurrentToolFrameIndex(self) -> int:
      """Get the current tool frame index of the parent operation.
      
      Returns:
         Tool frame index.
      """
      ...
   
   def GetCurrentBaseFrameIndex(self) -> int:
      """Get the current base frame index of the parent operation.
      
      Returns:
         Base frame index.
      """
      ...
   
   def GetCurrentToolFrameMatrix(self) -> CENPyOlpMatrix:
      """Get the current tool frame matrix of the parent operation.
      
      Returns:
         Tool frame matrix.
      """
      ...
   
   def GetCurrentBaseFrameMatrix(self) -> CENPyOlpMatrix:
      """Get the current base frame matrix of the parent operation.
      
      Returns:
         Base frame matrix.
      """
      ...
   
   def GetTechTabFolder(self, relativePath: str, feedbackErrorWhenFileNotFound: bool=True) -> str:
      """Gets the technology table folder path.
      If the relative path contains a file name with extension then it will return the path to that file.
      
      Args:
         relativePath: Name of a file/relative path to a file.
         feedbackErrorWhenFileNotFound: By default (True) a feedback error is passed when file not found.
      
      Returns:
         Technology table folder or a file path.
      """
      ...
   
