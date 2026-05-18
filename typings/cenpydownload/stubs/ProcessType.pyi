"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""

from enum import Enum

class ProcessType(Enum):
   """Process types used for an ICENToolpathElement"""
   NONE : int = 0
   ProcessPoint : int = 1
   TeachInsert : int = 2
   ProcessCurve : int = 3
   Approach : int = 4
   Retract : int = 5
   TrackLink : int = 6
   Cycle : int = 7
   Auxiliary : int = 8
   ToolChange : int = 9
   LeadIn : int = 10
   LeadOut : int = 11
   Gap : int = 12
   ExplodedCycle : int = 13
   ProcessSurface : int = 14
   ProcessInsert : int = 15
   ViaPoint : int = 16
   TPLink : int = 17
   TPLinkVia : int = 18
