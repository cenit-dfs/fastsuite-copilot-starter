"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from enum import Enum

class AccuracyCriteria(Enum):
   """The value in the accuracy event can represent more than one thing."""
   Off : int = 0
   On : int = 1
   JointDistance : int = 2
   Distance : int = 3
   Orientation : int = 4
   Velocity : int = 5
