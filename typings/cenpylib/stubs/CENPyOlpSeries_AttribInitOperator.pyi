"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribCreator import *
from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpController import *
from .CENPyOlpCsvParserOperator import *
from .CENPyOlpLogOperator import *

class CENPyOlpSeries_AttribInitOperator:
   def GetAttribCreator(self) -> CENPyOlpAttribCreator:
      """Gets the attribute creator for the represented series object.
      
      Returns:
         Attribute creator.
      """
      ...
   
   def GetAttribGetter(self) -> CENPyOlpAttribGetter:
      """Gets the attribute getter for the represented series object.
      
      Returns:
         Attribute getter.
      """
      ...
   
   def GetAttribSetter(self) -> CENPyOlpAttribSetter:
      """Gets the attribute setter for the represented series object.
      
      Returns:
         Attribute setter.
      """
      ...
   
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Gets the logger for the represented series object.
      
      Returns:
         Log interface.
      """
      ...
   
   def GetController(self) -> CENPyOlpController:
      """The controller where this series is used.
      
      Returns:
         The parent controller of the series.
      """
      ...
   
   def GetCsvParserOperator(self) -> CENPyOlpCsvParserOperator:
      """Get csv parser operator.
      
      Returns:
         Csv parser operator.
      """
      ...
   
