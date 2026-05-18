"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpAttribute import *
from .CENPyOlpController import *
from .CENPyOlpCsvParserOperator import *
from .CENPyOlpLogOperator import *
from .CENPyOlpMatrix import *
from .CENPyOlpProgramComponent import *
from .CENPyOlpWM_AttribChangedOperator import *

class CENPyOlpWM_AttribChangedOperator:
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
   
   def GetWorldReference(self) -> CENPyOlpMatrix:
      """Get the world matrix of the Olp attribute object's reference object.
      If the Olp attribute object does not have a reference object, the matrix will be a unit matrix.
      
      Returns:
         World matrix of the reference object.
      """
      ...
   
   def GetController(self) -> CENPyOlpController:
      """Get the parent controller interface.
      
      Returns:
         Controller interface.
      """
      ...
   
   def GetChangedAttribute(self) -> CENPyOlpAttribute:
      """Get the attribute which was changed.
      
      Returns:
         Changed attribute object.
      """
      ...
   
   def GetChangedAttributeName(self) -> str:
      """Get the name of the attribute which was changed.
      
      Returns:
         Changed attribute name.
      """
      ...
   
   def GetChangedComponent(self) -> CENPyOlpProgramComponent:
      """Get object of the container on which the attribute change happened.
      
      Returns:
         Object which contain changed attribute, can be program, operation group or operation.
      """
      ...
   
   def GetOperatorForComponent(self, component: CENPyOlpProgramComponent) -> CENPyOlpWM_AttribChangedOperator:
      """Get the operator for a given program component.
      <param name="component">program component to get an operator for it</param>
      
      Args:
         component: program component to get an operator for it
      
      Returns:
         AttribChangedOperator for program, operation group or operation.
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
   
