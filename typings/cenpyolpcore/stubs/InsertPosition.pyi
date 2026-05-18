"""
Automatically generated module. COPYRIGHT CENIT AG 2024.
"""


from enum import Enum

class InsertPosition(Enum):
   """Defines the insert position for objects in relation to a reference toolpath element"""
   InsertBefore : int = 0
   InsertAfter : int = 1
   InsertNone : int = 2
   Inherit : int = 3
