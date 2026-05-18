"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribCreator import *
from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpController import *
from .CENPyOlpLogOperator import *

class CENPyOlpEvent_AttribInitOperator:
   def GetAttribCreator(self) -> CENPyOlpAttribCreator:
      """Get attribute creator interface.
      
      Returns:
         Attribute creator interface.
      """
      ...
   
   def GetAttribGetter(self) -> CENPyOlpAttribGetter:
      """Get attribute getter interface.
      
      Returns:
         Attribute getter interface.
      """
      ...
   
   def GetAttribSetter(self) -> CENPyOlpAttribSetter:
      """Get attribute setter interface.
      
      Returns:
         Attribute setter interface.
      """
      ...
   
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Get logger operator.
      
      Returns:
         Logger operator.
      """
      ...
   
   def GetController(self) -> CENPyOlpController:
      """Get OLP controller.
      
      Returns:
         OLP controller.
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
   
