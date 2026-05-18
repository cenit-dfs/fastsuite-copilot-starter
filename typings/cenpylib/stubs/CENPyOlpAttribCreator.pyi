"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribGroup import *
from .CENPyOlpAttributeBool import *
from .CENPyOlpAttributeDouble import *
from .CENPyOlpAttributeEnum import *
from .CENPyOlpAttributeInt import *
from .CENPyOlpAttributeString import *
from .CENPyOlpAttributeTable import *
from .CENPyOlpSystemAttribCreator import *

class CENPyOlpAttribCreator:
   def AddInteger(self, name: str, val: int, min: int, max: int, olpAttribType: int, nls: str) -> CENPyOlpAttributeInt:
      """Create a new integer attribute.
      
      Args:
         name: name of the attribute
         val: default value of the attribute
         min: minimum value of the attribute
         max: maximum value of the attribute
         olpAttribType: attribute properties
         nls: NLS string
      
      Returns:
         Created attribute object.
      """
      ...
   
   def AddDouble(self, name: str, val: float, min: float, max: float, step: float, olpAttribType: int, attribType: int, nls: str) -> CENPyOlpAttributeDouble:
      """Create a new double attribute.
      
      Args:
         name: name of the attribute
         val: default value of the attribute
         min: minimum value of the attribute
         max: maximum value of the attribute
         step: step size for the arrow keys
         olpAttribType: attribute properties
         attribType: type of the Double of the attribute (length, etc.)
         nls: NLS string
      
      Returns:
         Created attribute object.
      """
      ...
   
   def AddString(self, name: str, val: str, olpAttribType: int, nls: str) -> CENPyOlpAttributeString:
      """Create a new string attribute.
      
      Args:
         name: name of the attribute
         val: default value of the attribute
         olpAttribType: attribute properties
         nls: NLS string
      
      Returns:
         Created attribute object.
      """
      ...
   
   def AddBool(self, name: str, val: bool, olpAttribType: int, nls: str) -> CENPyOlpAttributeBool:
      """Create a new bool attribute.
      
      Args:
         name: name of the attribute
         val: default value of the attribute
         olpAttribType: attribute properties
         nls: NLS string
      
      Returns:
         Created attribute object.
      """
      ...
   
   def AddEnum(self, name: str, literals: object, value: str, olpAttribType: int, nls: str) -> CENPyOlpAttributeEnum:
      """Create a new enum attribute.
      
      Args:
         name: name of the attribute
         literals: list of given items
         value: default value of the attribute
         olpAttribType: attribute properties
         nls: NLS string
      
      Returns:
         Created attribute object.
      """
      ...
   
   def AddTable(self, name: str, olpAttribType: int, nls: str) -> CENPyOlpAttributeTable:
      """Create a new table attribute.
      
      Args:
         name: name of the attribute
         olpAttribType: attribute properties
         nls: NLS string
      
      Returns:
         Created attribute object.
      """
      ...
   
   def GetSystemAttribCreator(self) -> CENPyOlpSystemAttribCreator:
      """Get an operator which creates system attributes.
      
      Returns:
         System attribute creator object.
      """
      ...
   
   def AddAttribGroup(self, name: str) -> CENPyOlpAttribGroup:
      """Create a new attribute group.
      
      Args:
         name: name of the group which will be added.
      
      Returns:
         Created group object.
      """
      ...
   
   def GetAllAttribGroups(self) -> list[CENPyOlpAttribGroup]:
      """Gets all attribute groups.
      
      Returns:
         List of CENPyOlpAttribGroup objects, found attribute groups.
      """
      ...
   
