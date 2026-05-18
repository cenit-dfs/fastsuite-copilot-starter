"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribute import *

class CENPyOlpAttributeDouble(CENPyOlpAttribute):
   def SetValue(self, value: float):
      """Set double value of attribute.
      
      Args:
         value: new value
      """
      ...
   
   def GetValue(self) -> float:
      """Get double value of attribute.
      
      Returns:
         value of the attribute
      """
      ...
   
   def SetMinimum(self, min: float):
      """Set the minimum range value. Must not be higher than maximum!
      
      Args:
         min: minimum range value
      """
      ...
   
   def GetMinimum(self) -> float:
      """Get the attribute minimum value.
      
      Returns:
         attribute minimum value
      """
      ...
   
   def SetMaximum(self, max: float):
      """Set the maximum range value. Must not be lower than minimum!
      
      Args:
         max: maximum range value
      """
      ...
   
   def GetMaximum(self) -> float:
      """Get the attribute maximum value
      
      Returns:
         attribute maximum value
      """
      ...
   
   def SetStepSize(self, step: float):
      """Set the attribute step size.
      
      Args:
         step: attribute step size
      """
      ...
   
   def GetStepSize(self) -> float:
      """Get the attribute step size.
      
      Returns:
         attribute step size
      """
      ...
   
