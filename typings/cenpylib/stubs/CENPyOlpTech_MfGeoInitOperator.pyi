"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpAttribute import *
from .CENPyOlpLogOperator import *
from .CENPyOlpProcessGeometryOperator import *

class CENPyOlpTech_MfGeoInitOperator:
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
   
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Get the log operator interface.
      
      Returns:
         Log operator interface.
      """
      ...
   
   def AddSystemAttrib(self, attrib: CENPyOlpAttribute):
      """Create the manufacturing geometry from the given system attributes.
      Note: This method will not create new attributes. Only system attributes which has been created in the
      IOlpTechnology::InitAttributes or in IOlpWorkMethod::InitAttributes can be added here.
      
      Args:
         attrib: Attribute object.
      """
      ...
   
   def GetCurrentProcessGeometryOperator(self) -> CENPyOlpProcessGeometryOperator:
      """Get the Process Geometry Operator of the PG that is attached to the current operation.
      
      Returns:
         Process Geometry Operator if there is a PG, otherwise - None.
      """
      ...
   
