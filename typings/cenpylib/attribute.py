"""COPYRIGHT Cenit AG 2022"""


class AttribUtility:
   """Attribute utility functions."""

   def GetControllerStringAttributeValue(self, name, controller):
      """Get the value of a user-defined String attribute by name.

      Args:
          name (str): attribute name.
          controller (CENPyOlpController): controller instance.

      Returns:
          bool: True if successful, otherwise False.
      """
      if name and controller:
         attrib = controller.GetAttributeStringByName(name)
         if attrib:
            return attrib.GetString()
      return None
   
   def GetControllerIntegerAttributeValue(self, name, controller):
      """Get the value of a user-defined Integer attribute by name.

      Args:
          name (str): attribute name.
          controller (CENPyOlpController): controller instance.

      Returns:
          bool: True if successful, otherwise False.
      """
      if name and controller:
         attrib = controller.GetAttributeIntegerByName(name)
         if attrib:
            return attrib.GetValue()
      return None

   def GetControllerFloatAttributeValue(self, name, controller):
      """Get the value of a user-defined Float attribute by name.

      Args:
          name (str): attribute name.
          controller (CENPyOlpController): controller instance.

      Returns:
          bool: True if successful, otherwise False.
      """
      if name and controller:
         attrib = controller.GetAttributeFloatByName(name)
         if attrib:
            return attrib.GetValue()
      return None

   def GetControllerBoolAttributeValue(self, name, controller):
      """Get the value of a user-defined Bool attribute by name.

      Args:
          name (str): attribute name.
          controller (CENPyOlpController): controller instance.

      Returns:
          bool: True if successful, otherwise False.
      """
      if name and controller:
         attrib = controller.GetAttributeBoolByName(name)
         if attrib:
            return attrib.GetState()
      return None
