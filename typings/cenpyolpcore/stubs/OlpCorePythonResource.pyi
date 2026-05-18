"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""


from .ItemSubType import ItemSubType
from .ItemType import ItemType
from .OlpCorePythonItem import *

class OlpCorePythonResource(OlpCorePythonItem):
      def GetItemType(self) -> ItemType:
         """Returns the item type of this resource
         
         Returns:
            None
         """
         ...
      
      def GetItemSubType(self) -> ItemSubType:
         """Returns the item subtype of this resource
         
         Returns:
            None
         """
         ...
      
      def GetSupportedConfigurations(self) -> list:
         """Gets all supported configurations on this resource if the resource is a machine or robot
         
         Returns:
            returns all supported configurations on this resource as list of strings
         """
         ...
      
      def GetSupportedTurns(self) -> list:
         """Gets all supported turns on this resource if the resource is a machine or robot
         
         Returns:
            returns all supported turns on this resource as list of strings
         """
         ...
      
      def GetAllPorts(self) -> list:
         """Get all ports that are currently active in this resource.
         
         Returns:
            a vector with all the ports found on the resource
         """
         ...
      
      def GetPorts(self   , valueType: int   , direction: int) -> list:
         """Get all ports that are currently active in this resource with the value type and the direction specified.
         
         Args:
            valueType: port value type
            direction: port direction
         
         Returns:
            a vector with all the ports found on the resource
         """
         ...
      
