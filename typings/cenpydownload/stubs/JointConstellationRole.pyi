"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from enum import Enum

class JointConstellationRole(Enum):
   """Constellation role means a more "refined" joint type.
   The joints are categorized based on what their parent items do."""
   Unset : int = 0
   Rail : int = 1
   WorkpiecePositioner : int = 2
   EndEffector : int = 3
   Peripheral : int = 4
   SynchronousOnRobot : int = 5
