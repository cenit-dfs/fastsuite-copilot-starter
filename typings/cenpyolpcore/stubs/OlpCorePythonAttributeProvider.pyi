"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""


from .OlpCorePythonBoolAttribute import *
from .OlpCorePythonDoubleArrayAttribute import *
from .OlpCorePythonDoubleAttribute import *
from .OlpCorePythonIntegerArrayAttribute import *
from .OlpCorePythonIntegerAttribute import *
from .OlpCorePythonLiteralAttribute import *
from .OlpCorePythonStringArrayAttribute import *
from .OlpCorePythonStringAttribute import *

class OlpCorePythonAttributeProvider:
      def GetAttributes(self) -> list:
         """Gets all attributes
         
         Returns:
            Returns a list containing all attributes of this provider
         """
         ...
      
      def GetIntegerAttribute(self   , attributeName: str   , bubbleUp: bool) -> OlpCorePythonIntegerAttribute:
         """Gets the first integer attribute with the given name.
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns the first attribute with the given name, None if no matching attribute was found
         """
         ...
      
      def GetDoubleAttribute(self   , attributeName: str   , bubbleUp: bool) -> OlpCorePythonDoubleAttribute:
         """Gets the first double attribute with the given name.
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns the first attribute with the given name, None if no matching attribute was found
         """
         ...
      
      def GetStringAttribute(self   , attributeName: str   , bubbleUp: bool) -> OlpCorePythonStringAttribute:
         """Gets the first string attribute with the given name.
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns the first attribute with the given name, None if no matching attribute was found
         """
         ...
      
      def GetBoolAttribute(self   , attributeName: str   , bubbleUp: bool) -> OlpCorePythonBoolAttribute:
         """Gets the first bool attribute with the given name.
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns the first attribute with the given name, None if no matching attribute was found
         """
         ...
      
      def GetIntegerArrayAttribute(self   , attributeName: str   , bubbleUp: bool) -> OlpCorePythonIntegerArrayAttribute:
         """Gets the first integer array attribute with the given name.
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns the first attribute with the given name, None if no matching attribute was found
         """
         ...
      
      def GetDoubleArrayAttribute(self   , attributeName: str   , bubbleUp: bool) -> OlpCorePythonDoubleArrayAttribute:
         """Gets the first double array attribute with the given name.
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns the first attribute with the given name, None if no matching attribute was found
         """
         ...
      
      def GetStringArrayAttribute(self   , attributeName: str   , bubbleUp: bool) -> OlpCorePythonStringArrayAttribute:
         """Gets the first string array attribute with the given name.
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns the first attribute with the given name, None if no matching attribute was found
         """
         ...
      
      def GetLiteralAttribute(self   , attributeName: str   , bubbleUp: bool) -> OlpCorePythonLiteralAttribute:
         """Gets the first literal attribute with the given name.
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns the first attribute with the given name, None if no matching attribute was found
         """
         ...
      
      def GetInteger(self   , attributeName: str   , bubbleUp: bool) -> int:
         """Gets the value of the first integer attribute found with the given attribute name
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns the first attribute value with the given name, int::min() if no matching attribute was found
         """
         ...
      
      def GetDouble(self   , attributeName: str   , bubbleUp: bool) -> float:
         """Gets the value of the first double attribute found with the given attribute name
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns the first attribute value with the given name, NaN if no matching attribute was found
         """
         ...
      
      def GetString(self   , attributeName: str   , bubbleUp: bool) -> str:
         """Gets the value of the first string attribute found with the given attribute name
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns the first attribute value with the given name, empty string if no matching attribute was found
         """
         ...
      
      def GetBool(self   , attributeName: str   , bubbleUp: bool) -> bool:
         """Gets the value of the first bool attribute found with the given attribute name
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns the first attribute value with the given name, False if no matching attribute was found
         """
         ...
      
      def GetIntegerArray(self   , attributeName: str   , bubbleUp: bool) -> list:
         """Gets the values of the first integer array attribute found with the given attribute name
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns a list with the values of the first attribute found. If no attribute was found, the list is empty
         """
         ...
      
      def GetDoubleArray(self   , attributeName: str   , bubbleUp: bool) -> list:
         """Gets the values of the first double array attribute found with the given attribute name
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns a list with the values of the first attribute found. If no attribute was found, the list is empty
         """
         ...
      
      def GetStringArray(self   , attributeName: str   , bubbleUp: bool) -> list:
         """Gets the values of the first string array attribute found with the given attribute name
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns a list with the values of the first attribute found. If no attribute was found, the list is empty
         """
         ...
      
      def GetLiteral(self   , attributeName: str   , bubbleUp: bool) -> str:
         """Gets the value of the first literal attribute found with the given attribute name
         
         Args:
            attributeName: name of the attribute
            bubbleUp: bubble up the parents if possible
         
         Returns:
            returns the first attribute value with the given name, empty string if no matching attribute was found
         """
         ...
      
