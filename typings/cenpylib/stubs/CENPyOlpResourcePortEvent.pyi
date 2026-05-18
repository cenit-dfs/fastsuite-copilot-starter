"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpBuiltInEvent import *
from .CENPyOlpPort import *
from .CENPyOlpResource import *

class CENPyOlpResourcePortEvent(CENPyOlpBuiltInEvent):
   def SetResource(self, resource: CENPyOlpResource):
      """Assigns a resource to this event. The event can only set ports of the one resource that is currently assigned.
      Please note! In order to add resource ports and set their values, the resource must be set to a port event.
      
      Args:
         resource: Resource that should be assigned to this event.
      """
      ...
   
   def GetResource(self) -> CENPyOlpResource:
      """Get the resource that is currently assigned to this event.
      
      Returns:
         Parent resource.
      """
      ...
   
   def AddResourcePortBool(self, port: CENPyOlpPort, value: bool):
      """Adds a port and a bool value for the port that this event should set.
      When the event is executed in simulation it will set the designated values to the ports that were added.
      If the port does not belong to the assigned resource it will not be added.
      If the port is not a bool input port it will not be added.
      If the port is already added its current value will be overwritten.
      
      Args:
         port: The port to be added.
         value: The value for the port.
      """
      ...
   
   def AddResourcePortByte(self, port: CENPyOlpPort, value: int):
      """Adds a port and a byte value for the port that this event should set.
      When the event is executed in simulation it will set the designated values to the ports that were added.
      If the port does not belong to the assigned resource it will not be added.
      If the port is not a byte input port it will not be added.
      If the port is already added its current value will be overwritten.
      
      Args:
         port: The port to be added.
         value: The value for the port.
      """
      ...
   
   def AddResourcePortInt(self, port: CENPyOlpPort, value: int):
      """Adds a port and an integer value for the port that this event should set.
      When the event is executed in simulation it will set the designated values to the ports that were added.
      If the port does not belong to the assigned resource it will not be added.
      If the port is not a 32 - bit integer port it will not be added.
      If the port is already added its current value will be overwritten.
      
      Args:
         port: The port to be added.
         value: The value for the port.
      """
      ...
   
   def AddResourcePortInt16(self, port: CENPyOlpPort, value: int):
      """Adds a port and an 16 bit integer value for the port that this event should set.
      When the event is executed in simulation it will set the designated values to the ports that were added.
      If the port does not belong to the assigned resource it will not be added.
      If the port is not a 16 - bit integer port it will not be added.
      If the port is already added its current value will be overwritten.
      
      Args:
         port: The port to be added.
         value: The value for the port.
      """
      ...
   
   def AddResourcePortFloat(self, port: CENPyOlpPort, value: float):
      """Adds a port and a floating point value for the port that this event should set.
      When the event is executed in simulation it will set the designated values to the ports that were added.
      If the port does not belong to the assigned resource it will not be added.
      If the port is not a float input port it will not be added.
      If the port is already added its current value will be overwritten.
      
      Args:
         port: The port to be added.
         value: The value for the port.
      """
      ...
   
