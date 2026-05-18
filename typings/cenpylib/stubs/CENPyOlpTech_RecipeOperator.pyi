"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribGetter import *
from .CENPyOlpLogOperator import *
from .CENPyOlpOperationGroup import *
from .CENPyOlpProcessGeometryOperator import *

class CENPyOlpTech_RecipeOperator:
   def GetSelectedProcessGeometries(self) -> list[CENPyOlpProcessGeometryOperator]:
      """Get all selected process geometries which are computed at the moment.
      
      Returns:
         List of CENPyOlpProcessGeometryOperator objects, selected process geometries.
      """
      ...
   
   def GetOperationGroup(self) -> CENPyOlpOperationGroup:
      """Create a new or returns an already existing OperationGroup from within a technology. Normally the OperationGroup is created by the kernel,
      but you can also create it from within a technology. In case of inserting new operations into the already existing group, this group will be returned.
      
      Returns:
         Operation Group.
      """
      ...
   
   def GetAttribGetter(self) -> CENPyOlpAttribGetter:
      """Get attrib getter to find existing attributes.
      
      Returns:
         Attrib getter object.
      """
      ...
   
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Get log operator that logs messages into output window.
      
      Returns:
         Logger object.
      """
      ...
   
   def GetGroupsToCompute(self) -> list[CENPyOlpOperationGroup]:
      """Get all groups which need to be computed. Normally these are groups where new operations have been added by the technology recipe.
      
      Returns:
         List of CENPyOlpOperationGroup objects, groups to be computed.
      """
      ...
   
