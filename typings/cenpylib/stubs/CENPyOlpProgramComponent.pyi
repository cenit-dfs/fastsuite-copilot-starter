"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpProgramComponent import *

class CENPyOlpProgramComponent:
   def GetType(self) -> int:
      """Get program component type.
      
      Returns:
         Program component type.
      """
      ...
   
   def GetParentComponent(self) -> CENPyOlpProgramComponent:
      """Get the parent program component.
      
      Returns:
         Parent program component.
      """
      ...
   
   def GetChildComponents(self) -> list[CENPyOlpProgramComponent]:
      """Get list of all child components.
      
      Returns:
         List of CENPyOlpProgramComponent objects, found child components.
      """
      ...
   
   def GetCreatorName(self) -> str:
      """Get the Technology/WorkMethod/Event name of program component.
      
      Returns:
         Technology/WorkMethod/Event name.
      """
      ...
   
