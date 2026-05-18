"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribute import *
from .CENPyOlpAttributeBool import *
from .CENPyOlpAttributeDouble import *
from .CENPyOlpAttributeEnum import *
from .CENPyOlpAttributeInt import *
from .CENPyOlpAttributeTable import *
from .CENPyOlpSystemAttribGetter import *

class CENPyOlpAttribGetter:
   def GetInteger(self, name: str) -> int:
      """Get the Integer Value for the given Integer attribute.
      
      Args:
         name: Name of the attribute.
      
      Returns:
         Value of the Integer Attribute.
      """
      ...
   
   def GetDouble(self, name: str) -> float:
      """Get the Double Value for the given Double attribute.
      
      Args:
         name: Name of the attribute.
      
      Returns:
         Value of the Double Attribute.
      """
      ...
   
   def GetString(self, name: str) -> str:
      """Get the String Value for the given String attribute.
      
      Args:
         name: Name of the attribute.
      
      Returns:
         Value of the String Attribute.
      """
      ...
   
   def GetBool(self, name: str) -> bool:
      """Get the Bool Value for the given Bool attribute.
      
      Args:
         name: Name of the attribute.
      
      Returns:
         Value of the Bool Attribute.
      """
      ...
   
   def GetEnumIndex(self, name: str) -> int:
      """Get the Index for the given Enum attribute.
      
      Args:
         name: Name of the attribute.
      
      Returns:
         Index of the Enum Attribute.
      """
      ...
   
   def GetAttributeTableByName(self, name: str, containsCellId: str="") -> CENPyOlpAttributeTable:
      """Get a user-defined Table attribute by the given name.
      
      Args:
         name: Name of the attribute to find.
         containsCellId: Row ID (empty by default).
      
      Returns:
         Attribute table object.
      """
      ...
   
   def GetAttributeByName(self, name: str) -> CENPyOlpAttribute:
      """Get a user-defined attribute by the given name.
      
      Args:
         name: Name of the attribute to find.
      
      Returns:
         Attribute object.
      """
      ...
   
   def GetAttributeBoolByName(self, name: str) -> CENPyOlpAttributeBool:
      """Get the Bool attribute by the given name.
      
      Args:
         name: Name of the attribute to find.
      
      Returns:
         Bool attribute object.
      """
      ...
   
   def GetAttributeEnumByName(self, name: str) -> CENPyOlpAttributeEnum:
      """Get the Enum attribute by the given name.
      
      Args:
         name: Name of the attribute to find.
      
      Returns:
         Enum attribute object.
      """
      ...
   
   def GetAttributeDoubleByName(self, name: str) -> CENPyOlpAttributeDouble:
      """Get the Double attribute by the given name.
      
      Args:
         name: Name of the attribute to find.
      
      Returns:
         Double attribute object.
      """
      ...
   
   def GetAttributeIntegerByName(self, name: str) -> CENPyOlpAttributeInt:
      """Get the Integer attribute by the given name.
      
      Args:
         name: Name of the attribute to find.
      
      Returns:
         Integer attribute object.
      """
      ...
   
   def GetSystemAttribGetter(self) -> CENPyOlpSystemAttribGetter:
      """Get the system attrib getter.
      
      Returns:
         System attrib getter object.
      """
      ...
   
   def GetScopeSortedTableRows(self, tableAttribName: str) -> list:
      """Get all IDs (first column) of the table from both program and controller tables.
      Duplicated IDs are removed.
      
      Args:
         tableAttribName: Name of the desired table.
      
      Returns:
         List with all IDs.
      """
      ...
   
