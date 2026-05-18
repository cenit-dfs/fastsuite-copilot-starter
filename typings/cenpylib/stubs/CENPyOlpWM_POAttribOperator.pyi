"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpController import *
from .CENPyOlpCsvParserOperator import *
from .CENPyOlpLogOperator import *
from .CENPyOlpProcessGeometryOperator import *
from .CENPyOlpWM_GeometryOperator import *

class CENPyOlpWM_POAttribOperator:
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
   
   def GetCsvParserOperator(self) -> CENPyOlpCsvParserOperator:
      """Get the CSV parser operator interface.
      
      Returns:
         CSV parser operator interface.
      """
      ...
   
   def GetGeometryOperator(self) -> CENPyOlpWM_GeometryOperator:
      """Get the geometry operator.
      
      Returns:
         Geometry operator.
      """
      ...
   
   def GetContourLength(self) -> float:
      """Get the contour length if there is a contour process geometry, for all other types 0.0 is returned.
      
      Returns:
         Contour length for a contour process geometry, for all other types 0.0 is returned.
      """
      ...
   
   def GetController(self) -> CENPyOlpController:
      """Get the parent controller interface.
      
      Returns:
         Controller interface.
      """
      ...
   
   def GetCurrentProcessGeometryOperator(self) -> CENPyOlpProcessGeometryOperator:
      """Get the Process Geometry Operator of the PG that is attached to the current operation.
      
      Returns:
         Process Geometry Operator if there is a PG, otherwise - None.
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
   
