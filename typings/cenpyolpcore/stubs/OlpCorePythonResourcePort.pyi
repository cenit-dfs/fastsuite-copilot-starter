"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""


from .PortDataType import PortDataType
from .PortDirection import PortDirection

class OlpCorePythonResourcePort:
      def GetName(self) -> str:
         """Gets the name of the resource port
         
         Returns:
            returns the resource port name as string
         """
         ...
      
      def GetComment(self) -> str:
         """Gets the comment of the resource port
         
         Returns:
            returns the resource port comment as string
         """
         ...
      
      def GetValueType(self) -> PortDataType:
         """Returns the value type of this port (bool, int, float)
         
         Returns:
            None
         """
         ...
      
      def GetPortDirection(self) -> PortDirection:
         """Returns the direction of this port (input or output)
         
         Returns:
            None
         """
         ...
      
