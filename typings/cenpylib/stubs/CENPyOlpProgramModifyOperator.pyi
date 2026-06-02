"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpComputeHandler import *
from .CENPyOlpController import *
from .CENPyOlpCsvParserOperator import *
from .CENPyOlpEventHandler import *
from .CENPyOlpInterpolationHandler import *
from .CENPyOlpLogOperator import *
from .CENPyOlpMatrix import *
from .CENPyOlpProcessGeometryOperator import *
from .CENPyOlpProgram import *
from .CENPyOlpTeachHandler import *
from .CENPyOlpTpElement import *

class CENPyOlpProgramModifyOperator:
   def GetAttribGetter(self) -> CENPyOlpAttribGetter:
      """Get attribute getter interface which handles the Olp attribute container.
      
      Returns:
         Attribute getter interface.
      """
      ...
   
   def GetAttribSetter(self) -> CENPyOlpAttribSetter:
      """Get attribute setter interface which handles the Olp attribute container.
      
      Returns:
         Attribute setter interface.
      """
      ...
   
   def GetController(self) -> CENPyOlpController:
      """Get the parent controller interface.
      
      Returns:
         Controller interface.
      """
      ...
   
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Get the log operator interface.
      
      Returns:
         Log operator interface.
      """
      ...
   
   def GetCsvParserOperator(self) -> CENPyOlpCsvParserOperator:
      """Get the CSV parser operator interface.
      
      Returns:
         CSV parser operator interface.
      """
      ...
   
   def GetActiveProgram(self) -> CENPyOlpProgram:
      """Get the active program of the controller, nullptr, if there is no program.
      
      Returns:
         Active off-line program.
      """
      ...
   
   def GetComputeHandler(self) -> CENPyOlpComputeHandler:
      """Get the compute handler of the parent controller.
      
      Returns:
         Compute handler.
      """
      ...
   
   def GetInterpolationHandler(self) -> CENPyOlpInterpolationHandler:
      """Get an interpolation handler.
      
      Returns:
         Interpolation handler.
      """
      ...
   
   def GetTeachHandler(self) -> CENPyOlpTeachHandler:
      """Get the teach handler for the current session.
      
      Returns:
         Teach handler.
      """
      ...
   
   def GetEventHandler(self) -> CENPyOlpEventHandler:
      """Get the event handler.
      
      Returns:
         Event handler.
      """
      ...
   
   def GetProgramTpElementsByName(self, programName: str) -> list[CENPyOlpTpElement]:
      """Get all toolpath elements of the program with the given name. If there is no program with that name the list is going to be empty.
      
      Returns:
         List of CENPyOlpTpElement objects, found toolpath elements.
      """
      ...
   
   def CreateMatrix(self) -> CENPyOlpMatrix:
      """Creates a new unit matrix.
      
      Returns:
         Newly created matrix
      """
      ...
   
   def GetAllProcessGeometries(self) -> list[CENPyOlpProcessGeometryOperator]:
      """Returns all process geometries.
      
      Returns:
         List of CENPyOlpProcessGeometryOperator process geometries.
      """
      ...
   
