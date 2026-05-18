"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from centypes import *
from .CENPyOlpController import *
from .CENPyOlpCsvParserOperator import *
from .CENPyOlpLogOperator import *
from .CENPyOlpProcessGeometryOperator import *
from .CENPyOlpProgram import *

class CENPyOlpProgramProcessGeometryOperator:
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Get a log operator interface.
      
      Returns:
         Log operator interface.
      """
      ...
   
   def GetCsvParserOperator(self) -> CENPyOlpCsvParserOperator:
      """Get a CSV parser operator interface.
      
      Returns:
         CSV parser operator interface.
      """
      ...
   
   def GetController(self) -> CENPyOlpController:
      """Get a parent controller interface.
      
      Returns:
         Controller interface.
      """
      ...
   
   def GetActiveProgram(self) -> CENPyOlpProgram:
      """Get an active controller program, nullptr, if there is no program.
      
      Returns:
         Active program.
      """
      ...
   
   def GetSelectedProcessGeometries(self, geoTypeFilter: int=PROCGEO_NONE) -> list[CENPyOlpProcessGeometryOperator]:
      """Get a list of all selected process geometries.
      
      Args:
         geoTypeFilter: Type of process geometry to return. Returns all PGs if type is None(0).
      
      Returns:
         List of CENPyOlpProcessGeometryOperator objects, selected process geometries.
      """
      ...
   
   def GetStartStateNames(self) -> list:
      """Get a list of all initial state names from the current project.
      
      Returns:
         Initial state names list.
      """
      ...
   
