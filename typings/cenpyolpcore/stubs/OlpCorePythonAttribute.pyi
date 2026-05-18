"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""


from .AttributeProperties import AttributeProperties

class OlpCorePythonAttribute:
      def GetOlpProperty(self) -> AttributeProperties:
         """Gets the <c>AttributeProperties</c> of this instance
         
         Returns:
            returns the set AttributeProperties
         """
         ...
      
      def GetReadOnly(self) -> bool:
         """Gets whether or not this attribute is globally read-only
         
         Returns:
            returns True if the attribute is read-only, False otherwise
         """
         ...
      
      def GetName(self) -> str:
         """Gets the name of the attribute
         
         Returns:
            returns the name of the attribute as cen_string
         """
         ...
      
      def GetGroupName(self) -> str:
         """Gets the group name
         
         Returns:
            returns the name of the attribute group as cen_string
         """
         ...
      
      def GetValueUnitType(self) -> int:
         """Gets the Unit Type the value is represented in
         
         Returns:
            returns the Unit Type the value is represented in
         """
         ...

