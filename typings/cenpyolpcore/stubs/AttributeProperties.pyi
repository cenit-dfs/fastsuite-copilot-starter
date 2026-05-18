from enum import Enum

class AttributeProperties(Enum):
   """Defines the possible attribute properties"""
   Unset : int = 0
   UserAttribute : int = 1
   ProcessAttribute : int = 2
   OperationAttribute : int = 4
   OperationGroupAttribute : int = 8
   GlobalAttribute : int = 16
   ReadOnlyAttribute : int = 32
   ControllerAttribute : int = 64
