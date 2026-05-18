"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""


from enum import Enum

class EventType(Enum):
   """This enum represents a merge of existing OlpEventType & BuiltInEventTypes enums"""
   Unset : int = 0
   Olp : int = 1
   Approach : int = 2
   Retract : int = 3
   Connect : int = 4
   ToolChange : int = 5
   Process : int = 6
   LeadIn : int = 7
   LeadOut : int = 8
   GapBegin : int = 9
   GapEnd : int = 10
   BoolActor : int = 11
   Speed : int = 12
   Accuracy : int = 13
   Tool : int = 14
   Suppress : int = 15
   Dwell : int = 16
   Acceleration : int = 17
   Optimization : int = 18
   SyncRobots : int = 19
   SetResourcePort : int = 20
   WaitForResourcePort : int = 21
   LogicPort : int = 22
   Insert : int = 23
   Modify : int = 24
