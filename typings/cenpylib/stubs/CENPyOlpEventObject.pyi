"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""


class CENPyOlpEventObject:
   def IsAttributeValid(self, name: str) -> bool:
      """Method to determine if the attribute with the given name is valid
      
      Args:
         name: name of the attribute
      
      Returns:
         True if attribute is valid (exists)
      """
      ...
   
   def SetEnumIndex(self, name: str, iVal: int):
      """Sets the index of the active enum literal of the attribute with the given name
      
      Args:
         name: name of the attribute
         iVal: new literal index
      """
      ...
   
   def GetEnumIndex(self, name: str) -> int:
      """Gets the index of the active enum literal of the attribute with the given name
      
      Args:
         name: name of the enum attribute
      
      Returns:
         literal index
      """
      ...
   
   def SetInteger(self, name: str, iVal: int):
      """Sets a new value to the given attribute
      
      Args:
         name: name of the attribute
         iVal: new value of the attribute
      """
      ...
   
   def GetInteger(self, name: str) -> int:
      """Gets the integer attribute value for the given attribute name
      
      Args:
         name: name of the attribute
      
      Returns:
         Attribute value.
      """
      ...
   
   def SetDouble(self, name: str, iVal: float):
      """Sets a new value to the given attribute
      
      Args:
         name: name of the attribute
         iVal: new value of the attribute
      """
      ...
   
   def GetDouble(self, name: str) -> float:
      """Gets a the value for the given attribute
      
      Args:
         name: name of the attribute
      
      Returns:
         Attribute value.
      """
      ...
   
   def SetString(self, name: str, iVal: str):
      """Sets a new value to the given attribute
      
      Args:
         name: name of the attribute
         iVal: new value of the attribute
      """
      ...
   
   def GetString(self, name: str) -> str:
      """Gets a the value for the given attribute
      
      Args:
         name: name of the attribute
      
      Returns:
         Attribute value.
      """
      ...
   
   def SetBool(self, name: str, iVal: bool):
      """Sets a new value to the given attribute
      
      Args:
         name: name of the attribute
         iVal: new value of the attribute
      """
      ...
   
   def GetBool(self, name: str) -> bool:
      """Gets a the value for the given attribute
      
      Args:
         name: name of the attribute
      
      Returns:
         Attribute value.
      """
      ...
   
   def GetOlpEventInsertPosition(self) -> int:
      """Get the event's insert Position before/after.
      
      Returns:
         insert Position before/after
      """
      ...
   
   def GetOlpEventName(self) -> str:
      """Get the event's Name.
      
      Returns:
         the Name of the OlpEvent
      """
      ...
   
