"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribute import *

class CENPyOlpAttribGroup:
   def AddAttribute(self, attribute: CENPyOlpAttribute):
      """Add an attribute to attribute group.
      
      Args:
         attribute: attribute to be added
      """
      ...
   
   def GetName(self) -> str:
      """Get name of attribute group.
      
      Returns:
         name of attribute group
      """
      ...
   
   def IsAttributeInGroup(self, attributeName: str) -> bool:
      """Check if attribute with given name is contained in group
      
      Args:
         attributeName: name of attribute to be checked
      
      Returns:
         True: is contained; False: is not contained
      """
      ...
   
   def GetAttributeNames(self) -> list:
      """Get names of attributes in attribute group.
      
      Returns:
         names of attributes in attribute group
      """
      ...
   
