"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpLogOperator import *
from .CENPyOlpProcessGeometryOperator import *
from .CENPyOlpTpElement import *

class CENPyOlpEventRuleOperator:
   def GetAttribGetter(self) -> CENPyOlpAttribGetter:
      """Get attribute getter interface.
      
      Returns:
         Attribute getter interface.
      """
      ...
   
   def GetAttribSetter(self) -> CENPyOlpAttribSetter:
      """Get attribute setter interface.
      
      Returns:
         Attribute setter interface.
      """
      ...
   
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Get attribute logger interface.
      
      Returns:
         Attribute logger interface.
      """
      ...
   
   def GetCurrentProcessGeometryOperator(self) -> CENPyOlpProcessGeometryOperator:
      """Get the process geometry operator of the parent operation.
      
      Returns:
         PG operator if there is one, otherwise None.
      """
      ...
   
   def FindTpElementsByType(self, iEventProcessType: int) -> list[CENPyOlpTpElement]:
      """Gets the toolpath elements with attached events of given EventProcessType.
      
      Args:
         iEventProcessType: TPE type where to attach events.
      
      Returns:
         List of CENPyOlpTpElement objects, found toolpath elements.
      """
      ...
   
   def FindTpElementsByPositions(self, positions: list, tolerance: float) -> list[CENPyOlpTpElement]:
      """Gets the toolpath elements fitting to positions in given array by taking given tolerance into account.
      
      Args:
         positions: List of positions, each position in [0.0, 1.0].
         tolerance: Given length tolerance.
      
      Returns:
         List of CENPyOlpTpElement objects, found toolpath elements.
      """
      ...
   
   def FindTpElementsById(self, requestId: int) -> list[CENPyOlpTpElement]:
      """Gets the toolpath elements fitting given request id.
      
      Args:
         requestId: Given request id - originally passed through by technology.
      
      Returns:
         List of CENPyOlpTpElement objects, found toolpath elements with given request ID.
      """
      ...
   
   def FindTpeByTechRequestId(self, techRequestId: int) -> list[CENPyOlpTpElement]:
      """Gets the toolpath elements with the given technology request ID.
      
      Args:
         techRequestId: Technology request ID.
      
      Returns:
         List of CENPyOlpTpElement objects, found toolpath elements marked with given technology request ID.
      """
      ...
   
   def AddTpe(self, tpe: CENPyOlpTpElement):
      """Add a toolpath element to the list of TPEs.
      
      Args:
         tpe: Toolpath element to be added.
      """
      ...
   
   def SetActiveEvent(self, index: int):
      """Set the active event by the list index.
      
      Args:
         index: Index of the desired event.
      """
      ...
   
