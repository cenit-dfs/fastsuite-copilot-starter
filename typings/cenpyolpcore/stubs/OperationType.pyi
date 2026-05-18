"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""


from enum import Enum

class OperationType(Enum):
   """Defines the different types of ICENOperation"""
   Normal : int = 0
   Approach : int = 1
   Retract : int = 2
   Auxiliary : int = 3
   Grab : int = 4
   Release : int = 5
   Upload : int = 6
