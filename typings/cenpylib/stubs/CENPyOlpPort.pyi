"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""


class CENPyOlpPort:
   def GetName(self) -> str:
      """Get the internal port name.
      
      Returns:
         The port name.
      """
      ...
   
   def GetComment(self) -> str:
      """Get the human readable port comment. This is the externally visible name that can be seen and customized by the user.
      
      Returns:
         The comment of the port.
      """
      ...
   
   def GetValueType(self) -> int:
      """Get the value type of the resource.
      
      Returns:
         The value type of the port as unsigned integer.
      """
      ...
   
   def GetPortDirection(self) -> int:
      """Get the direction of the port.
      
      Returns:
         The direction of the port as unsigned integer.
      """
      ...
   
