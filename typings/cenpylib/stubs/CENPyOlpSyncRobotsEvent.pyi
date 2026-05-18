"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpBuiltInEvent import *

class CENPyOlpSyncRobotsEvent(CENPyOlpBuiltInEvent):
   def SetSyncMode(self, syncMode: int):
      """Set the new synchronization mode.
      
      Args:
         syncMode: New synchronization mode.
      """
      ...
   
   def GetSyncMode(self) -> int:
      """Get the synchronization mode.
      
      Returns:
         Synchronization mode.
      """
      ...
   
   def SetRegionState(self, state: bool):
      """Set the region state.
      
      Args:
         state: New region state.
      """
      ...
   
   def GetRegionState(self) -> bool:
      """Get the region state.
      
      Returns:
         Region state.
      """
      ...
   
   def SetLeaderState(self, isLeader: bool):
      """Set the state of the leader flag.
      
      Args:
         isLeader: New leader state flag.
      """
      ...
   
   def GetLeaderState(self) -> bool:
      """Get the state of the leader flag.
      
      Returns:
         State of the leader flag.
      """
      ...
   
   def SetSyncText(self, syncText: str):
      """Set the new synchronization text.
      
      Args:
         syncText: New synchronization text.
      """
      ...
   
   def GetSyncText(self) -> str:
      """Get the synchronization text
      
      Returns:
         Synchronization text.
      """
      ...
   
