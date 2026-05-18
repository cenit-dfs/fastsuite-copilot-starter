"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribCreator import *
from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpAttribute import *
from .CENPyOlpController import *
from .CENPyOlpLogOperator import *
from .CENPyOlpProgramComponent import *
from .CENPyOlpTech_RuleUpdateOperator import *
from .CENPyOlpWM_RuleUpdateOperator import *

class CENPyOlpTech_UpdateOperator:
   def GetAttribGetter(self, prgComponent: CENPyOlpProgramComponent) -> CENPyOlpAttribGetter:
      """Get attribute getter by given program component.
      
      Args:
         prgComponent: Program component.
      
      Returns:
         Attribute getter.
      """
      ...
   
   def GetAttribSetter(self, prgComponent: CENPyOlpProgramComponent) -> CENPyOlpAttribSetter:
      """Get attribute setter by given program component.
      
      Args:
         prgComponent: Program component.
      
      Returns:
         Attribute setter.
      """
      ...
   
   def GetAttribCreator(self, prgComponent: CENPyOlpProgramComponent) -> CENPyOlpAttribCreator:
      """Get attribute creator by given program component.
      
      Args:
         prgComponent: Program component.
      
      Returns:
         Attribute creator.
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
   
   def GetOlpProgram(self) -> CENPyOlpProgramComponent:
      """Get the parent program.
      
      Returns:
         Parent program.
      """
      ...
   
   def RemoveAttribute(self, prgComponent: CENPyOlpProgramComponent, attributeName: str) -> bool:
      """Remove an attribute from a program component.
      
      Args:
         prgComponent: Program component.
         attributeName: Name of attribute to remove.
      
      Returns:
         True if the attribute was found in the program component and removed, False otherwise.
      """
      ...
   
   def SetAttribOwner(self, attrib: CENPyOlpAttribute, attribOwnerName: str):
      """Set owner of attribute.
      
      Args:
         attrib: Attribute object.
         attribOwnerName: Name of attribute owner.
      """
      ...
   
   def GetTechEventRuleUpdateOperator(self, rule: CENPyOlpProgramComponent) -> CENPyOlpTech_RuleUpdateOperator:
      """Get technology event rule update operator.
      
      Args:
         rule: Event rule.
      
      Returns:
         Technology event rule update operator.
      """
      ...
   
   def GetWmEventRuleUpdateOperator(self, rule: CENPyOlpProgramComponent) -> CENPyOlpWM_RuleUpdateOperator:
      """Get work method event rule update operator.
      
      Args:
         rule: Event rule.
      
      Returns:
         Work method event rule update operator.
      """
      ...
   
   def GetCycleExplodeStatus(self, prgComponent: CENPyOlpProgramComponent) -> int:
      """Get cycle explode status.
      
      Args:
         prgComponent: Program component.
      
      Returns:
         Unsigned cycle explode status.
      """
      ...
   
   def CopyAttribute(self, attributeName: str, prgComponent: CENPyOlpProgramComponent) -> CENPyOlpAttribute:
      """Copy an attribute with given name from technology definition into given component.
        When attribute does not exist in component it is created, otherwise overwritten.
      
      Args:
         attributeName: Name of attribute.
         prgComponent: Program component.
      
      Returns:
         Copied attribute of program component. In case of any failure, None is returned.
      """
      ...
   
   def GetLastSavedPythonTechnologyVersion(self) -> int:
      """Get the python technology script version, which was used during the last program processing and saved in the process file.
      
      Returns:
         Current Python technology version number.
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
   
