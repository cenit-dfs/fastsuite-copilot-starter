"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from typing import overload
from .CENPyOlpOperation import *
from .CENPyOlpOperationGroup import *
from .CENPyOlpProgram import *

class CENPyOlpComputeHandler:
   def EnableAutoRecompute(self):
      """Enable the recompute: all requests to the compute handler will be handled as usual
      """
      ...
   
   def DisableAutoRecompute(self):
      """Disable the recompute: all requests to the compute handler will be ignored
      """
      ...
   
   @overload
   def TriggerRecompute(self, program: CENPyOlpProgram, recomputeEnterState: int):
      """Put a recompute request. The request will be executed regardless of the current compute mode.
      
      Args:
         program: Computable object.
         recomputeEnterState: Recompute enter state.
      """
      ...
   
   @overload
   def TriggerRecompute(self, opGroup: CENPyOlpOperationGroup, recomputeEnterState: int):
      """Put a recompute request. The request will be executed regardless of the current compute mode.
      
      Args:
         opGroup: Computable object.
         recomputeEnterState: Recompute enter state.
      """
      ...
   
   @overload
   def TriggerRecompute(self, operation: CENPyOlpOperation, recomputeEnterState: int):
      """Put a recompute request. The request will be executed regardless of the current compute mode.
      
      Args:
         operation: Computable object.
         recomputeEnterState: Recompute enter state.
      """
      ...
   
