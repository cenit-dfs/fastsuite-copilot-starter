"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""


class CENPyOlpAttribute:
   def SetOlpProperty(self, iOlpProperty: int):
      """Sets Olp Property of attribute.
      
      Args:
         iOlpProperty: input of Olp Property, one or combination of following values can be given - USER_ATTRIBUTE | PROCESS_ATTRIBUTE | OPERATION_ATTRIBUTE | OPERATION_GROUP_ATTRIBUTE | GLOBAL_ATTRIBUTE
      """
      ...
   
   def GetVisibility(self) -> bool:
      """Get visibility status of attribute.
      
      Returns:
         visibility status
      """
      ...
   
   def SetVisibility(self, visible: bool):
      """Set visibility status of attribute.
      
      Args:
         visible: input of visibility status
      """
      ...
   
   def GetName(self) -> str:
      """Get name of attribute.
      
      Returns:
         name
      """
      ...
   
   def SetName(self, name: str):
      """Set name of attribute.
      
      Args:
         name: name of attribute
      """
      ...
   
   def GetRecomputeEnterState(self) -> int:
      """Returns the enter state for recompute valid for this attribute.
      
      Returns:
         Recompute enter state.
      """
      ...
   
   def SetReComputeEnterState(self, recomputableEnterState: int):
      """Sets the enter state for recompute for this attribute.
      
      Args:
         recomputableEnterState: Recompute enter state.
      """
      ...
   
   def IsValid(self) -> bool:
      """Checks if attribute is a valid olp attribute
      
      Returns:
         True if valid, False if not valid or null
      """
      ...
   
   def SetReadOnly(self, readOnly: bool):
      """Set readonly status of attribute.
      
      Args:
         readOnly: input of readonly status
      """
      ...
   
   def GetReadOnly(self) -> bool:
      """Get readonly status of attribute.
      
      Returns:
         readonly status
      """
      ...
   
   def SetIconName(self, iconName: str):
      """Set the icon name for this attribute. 
      Attention: Currently this method has no effect in ActiveProgramDashboard and in ProgrammingDefaultsDashboard because the icons there are managed in settings.xml
      
      Args:
         iconName: The icon to be used for this attribute
      """
      ...
   
   def GetIconName(self) -> str:
      """Returns the icon name for this attribute
      
      Returns:
         The icon for this attribute
      """
      ...
   
   def SetTooltipKey(self, tooltipKey: str):
      """Set the tooltipKey for this attribute.
      
      Args:
         tooltipKey: Key for tooltip
      """
      ...
   
