"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpController import *
from .CENPyOlpCsvParserOperator import *
from .CENPyOlpLogOperator import *
from .CENPyOlpMatrix import *

class CENPyOlpFrameChangedOperator:
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
   
   def GetController(self) -> CENPyOlpController:
      """Get the parent controller interface.
      
      Returns:
         Controller interface.
      """
      ...
   
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Get the log operator interface.
      
      Returns:
         Log operator interface.
      """
      ...
   
   def GetCsvParserOperator(self) -> CENPyOlpCsvParserOperator:
      """Get the CSV parser operator interface.
      
      Returns:
         CSV parser operator interface.
      """
      ...
   
   def GetTechTabFolder(self, relativePath: str, feedbackErrorWhenFileNotFound: bool=True) -> str:
      """Get the full path to the specified technology table.
      
      Args:
         relativePath: Relative path with the file name or only the file name.
         feedbackErrorWhenFileNotFound: Activates feedback if no file is found.
      
      Returns:
         Technology table full path.
      """
      ...
   
   def GetChangedFrameName(self) -> str:
      """Get the name of the changed frame.
      
      Returns:
         Changed frame name.
      """
      ...
   
   def GetChangedFrameIndex(self) -> int:
      """Get the index of the changed frame.
      
      Returns:
         Changed frame index.
      """
      ...
   
   def GetChangedFrameType(self) -> int:
      """Get the type of the changed frame.
      
      Returns:
         Changed frame type.
      """
      ...
   
   def GetChangedFrameMatrix(self) -> CENPyOlpMatrix:
      """Get the position matrix of the changed frame.
      
      Returns:
         Position matrix.
      """
      ...
   
   def GetChangedFrameWorldMatrix(self) -> CENPyOlpMatrix:
      """Get the position matrix of the changed frame relative to the world.
      
      Returns:
         World position matrix.
      """
      ...
   
