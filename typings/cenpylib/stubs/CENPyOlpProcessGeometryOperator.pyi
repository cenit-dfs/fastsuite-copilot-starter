"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttributeBool import *
from .CENPyOlpAttributeDouble import *
from .CENPyOlpAttributeInt import *
from .CENPyOlpAttributeString import *
from .CENPyOlpController import *
from .CENPyOlpMatrix import *
from .CENPyOlpPoint import *

class CENPyOlpProcessGeometryOperator:
   def GetInteger(self, name: str) -> int:
      """Gets the Integer Value for the given Integer attribute
      
      Args:
         name: name of the attribute.
      
      Returns:
         Value of the Integer Attribute.
      """
      ...
   
   def GetDouble(self, name: str) -> float:
      """Gets the Double Value for the given Double attribute
      
      Args:
         name: name of the attribute.
      
      Returns:
         Value of the Double Attribute.
      """
      ...
   
   def GetString(self, name: str) -> str:
      """Gets the String Value for the given String attribute
      
      Args:
         name: name of the attribute.
      
      Returns:
         Value of the String Attribute.
      """
      ...
   
   def GetBool(self, name: str) -> bool:
      """Gets the Bool Value for the given Bool attribute
      
      Args:
         name: name of the attribute.
      
      Returns:
         Value of the Bool Attribute.
      """
      ...
   
   def GetAttributeIntegerByName(self, attributeName: str) -> CENPyOlpAttributeInt:
      """Gets the Integer attribute by the given name.
      
      Args:
         attributeName: Name of the attribute to find.
      
      Returns:
         Integer attribute.
      """
      ...
   
   def GetAttributeDoubleByName(self, attributeName: str) -> CENPyOlpAttributeDouble:
      """Gets the Double attribute by the given name.
      
      Args:
         attributeName: Name of the attribute to find.
      
      Returns:
         Double attribute.
      """
      ...
   
   def GetAttributeStringByName(self, attributeName: str) -> CENPyOlpAttributeString:
      """Gets the String attribute by the given name.
      
      Args:
         attributeName: Name of the attribute to find.
      
      Returns:
         String attribute.
      """
      ...
   
   def GetAttributeBoolByName(self, attributeName: str) -> CENPyOlpAttributeBool:
      """Gets the Bool attribute by the given name.
      
      Args:
         attributeName: Name of the attribute to find.
      
      Returns:
         Bool attribute.
      """
      ...
   
   def GetProcessGeometryName(self) -> str:
      """Gets the Name of the current used Process Geometry
      
      Returns:
         Name of the Process Geometry.
      """
      ...
   
   def IsRegshape(self) -> bool:
      """Check if the process geometry is a regshape
      
      Returns:
         True if regshape detected, otherwise False.
      """
      ...
   
   def GetRegshapeType(self) -> int:
      """Detects and returns the RegshapeType
      
      Returns:
         detected RegshapeType as an Integer
      """
      ...
   
   def GetRegshapeCenter(self) -> CENPyOlpMatrix:
      """Returns the center of the regshape with respect to the base frame coordinates given by the operation 
      this regshape is assigned to. If this is no regshape nullptr is returned.
      
      Returns:
         regshape center in a Matrix base frame coordinates
      """
      ...
   
   def GetRegshapeLength(self) -> float:
      """Gets the Length of the Regshape
      
      Returns:
         Length of the Regshape in a Double
      """
      ...
   
   def GetRegshapeHeight(self) -> float:
      """Gets the Height of the Regshape
      
      Returns:
         Height of the Regshape in a Double
      """
      ...
   
   def GetRegshapeRadius(self) -> float:
      """Gets the Radius of the Regshape
      
      Returns:
         Radius of the Regshape in a Double
      """
      ...
   
   def GetRegshapeCornerRadius(self) -> float:
      """Gets the CornerRadius of the Regshape (Keyhole)
      
      Returns:
         CornerRadius of the Regshape in a Double
      """
      ...
   
   def GetGeoType(self) -> int:
      """Gets the Process geometry Type
      
      Returns:
         detected RegshapeType as an Integer
      """
      ...
   
   def GetContourLength(self) -> float:
      """Returns the curve length of the contour process geometry.
      
      Returns:
         Contour curve length.
      """
      ...
   
   def IsProcessGeometryBoxWithinWorkingAreaOfController(self, controller: CENPyOlpController) -> bool:
      """Checks if the bounding box of the process geometry is within the working area of the specified controller.
      
      Args:
         controller: Pointer to the CENPyOlpController object representing the controller.
      
      Returns:
         True if the bounding box of the process geometry is within the working area of the controller, otherwise False.
      """
      ...
   
   def GetBoundingBox(self) -> tuple[CENPyOlpPoint, CENPyOlpPoint]:
      """Returns the bounding box of a process geometry.
      
      Returns:
         A tuple of CENPyOlpPoint, CENPyOlpPoint objects representing bounding box of a process geometry as min and max points in world
      """
      ...
   
   def GetProcessGeometryIdentifier(self) -> str:
      """Get the UUID of the process geometry.
      
      Returns:
         Process geometry UUID.
      """
      ...
   
