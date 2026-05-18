"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribCreator import *
from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpController import *
from .CENPyOlpCsvParserOperator import *
from .CENPyOlpLogOperator import *

class CENPyOlpWM_AttribInitOperator:
   def GetAttribCreator(self) -> CENPyOlpAttribCreator:
      """Get attribute creator interface which handles the Olp attribute container.
      
      Returns:
         Attribute creator interface.
      """
      ...
   
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
   
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Get the log operator interface.
      
      Returns:
         Log operator interface.
      """
      ...
   
   def GetController(self) -> CENPyOlpController:
      """Get the parent controller interface.
      
      Returns:
         Controller interface.
      """
      ...
   
   def GetCsvParserOperator(self) -> CENPyOlpCsvParserOperator:
      """Get the CSV parser operator interface.
      
      Returns:
         CSV parser operator interface.
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
   
