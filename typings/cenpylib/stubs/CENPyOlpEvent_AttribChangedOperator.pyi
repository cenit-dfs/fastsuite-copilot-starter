"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpController import *
from .CENPyOlpLogOperator import *

class CENPyOlpEvent_AttribChangedOperator:
   def GetAttribGetter(self) -> CENPyOlpAttribGetter:
      """Get attribute getter interface which handles the Olp attribute container.
      
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
   
   def GetChangedAttributeName(self) -> str:
      """Gets the changed attribute name for the represented series object.
      
      Returns:
         Name of the changed attribute.
      """
      ...
   
   def IsEventCreatedAutomatically(self) -> bool:
      """Get if the reference Event was created by a rule, another event, or inserted manually.
      
      Returns:
         True if the Event was created by a rule or by another Event, False if inserted manually.
      """
      ...
   
