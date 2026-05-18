"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpAttribute import *
from .CENPyOlpLogOperator import *

class CENPyOlpSeries_AttribChangedOperator:
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
   
   def GetChangedAttribute(self) -> CENPyOlpAttribute:
      """Gets the changed attribute object for the represented series object.
      
      Returns:
         Changed attribute object.
      """
      ...
   
   def GetChangedAttributeName(self) -> str:
      """Gets the changed attribute name for the represented series object.
      
      Returns:
         Name of the changed attribute.
      """
      ...
   
