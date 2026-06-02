"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpComputeHandler import *
from .CENPyOlpController import *
from .CENPyOlpEventHandler import *
from .CENPyOlpInterpolationHandler import *
from .CENPyOlpLogOperator import *
from .CENPyOlpOperation import *
from .CENPyOlpOperationGroup import *
from .CENPyOlpProcessGeometryOperator import *
from .CENPyOlpProgram import *
from .CENPyOlpTeachHandler import *

class CENPyOlpBalancingSequencingOperator:
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Retrieve the logger operator associated with this sequencing operator.
      
      Returns:
         Log operator interface.
      """
      ...
   
   def GetAllControllers(self) -> list[CENPyOlpController]:
      """Get a list of all available controllers.
      
      Returns:
         Controllers available in project as a list CENPyOlpController objects.
      """
      ...
   
   def GetActiveController(self) -> CENPyOlpController:
      """Get active controller.
      
      Returns:
         Active controller.
      """
      ...
   
   def SetActiveController(self, controller: CENPyOlpController) -> int:
      """Set active controller.
      
      Args:
         controller: Controller to be set as active".
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise
      """
      ...
   
   def SequenceOperations(self, operationsToMove: list, referenceOperation: CENPyOlpOperation, insertLocation: SequenceInsertionType) -> int:
      """This method reorders operations by sequencing the given operations after or before a referenced operation.
      For example :
      operations of the operation - group : [O1, O2, O3, O4, O5]
      Switch O4 and O1 after O2.
      Input :
      operationsToSequence = [O4, O1],
      refOperation = O2, insertType = SequenceInsertionType::InsertAfterRef
      Result -> (operations after sequencing) : [O2, O4, O1, O3, O5]
      
      Args:
         operationsToMove: List of CENPyOlpOperation objects to sequence
         referenceOperation: Referenced operation CENPyOlpOperation , after or before the operationsToSequence will be sequenced.
         insertLocation: The insert-type: SequenceInsertionType::InsertAfterRef or SequenceInsertionType::InsertBeforeRef
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise
      """
      ...
   
   def MoveOperationsToController(self, operationsToMove: list, refController: CENPyOlpController, splitWithCopy: bool=False) -> int:
      """Moves the given operations to the active program of the specified controller.
      If the controller has no active program yet, a new default program is created.
      
      Args:
         operationsToMove: List of operations CENPyOlpOperation objects to move.
         refController: Target controller whose active program receives the operations.
         splitWithCopy: Make a copy (do not remove operation from the source)
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise.
      """
      ...
   
   def MoveOperationsToProgram(self, operationsToMove: list, refProgram: CENPyOlpProgram, splitWithCopy: bool=False) -> int:
      """Moves the given operations to the specified program.
      If the program is not active, the operations will still be moved to it.
      
      Args:
         operationsToMove: List of CENPyOlpOperation objects to move.
         refProgram: Target program to which the operations will be moved.
         splitWithCopy: Make a copy (do not remove operation from the source)
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise.
      """
      ...
   
   def CopyOperationsToController(self, operationsToCopy: list, refController: CENPyOlpController) -> int:
      """Copies the given operations to the active program of the specified controller.
      If the controller has no active program yet, a new default program is created.
      
      Args:
         operationsToCopy: List of operations CENPyOlpOperation objects to copy.
         refController: Target controller whose active program receives the operations.
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise.
      """
      ...
   
   def CopyOperationsToProgram(self, operationsToCopy: list, refProgram: CENPyOlpProgram) -> int:
      """Copies the given operations to the specified program.
      If the program is not active, the operations will still be copied to it.
      
      Args:
         operationsToCopy: List of CENPyOlpOperation objects to copy.
         refProgram: Target program to which the operations will be copied.
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise.
      """
      ...
   
   def CanSequenceOperations(self, operationsToCheck: list, referenceOperation: CENPyOlpOperation, insertLocation: SequenceInsertionType) -> int:
      """Checks if operations could be sequenced with SequenceOperations() method.
      
      Args:
         operationsToCheck: The list of CENPyOlpOperation objects to be checked
         referenceOperation: Referenced operation, after or before the operationsToSequence will be sequenced.
         insertLocation: The insert-type: SequenceInsertionType::InsertAfterRef or SequenceInsertionType::InsertBeforeRef
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise
      """
      ...
   
   def SequenceOperationGroups(self, operationGroupsToSequence: list, referenceOperationGroup: CENPyOlpOperationGroup, insertLocation: SequenceInsertionType) -> int:
      """This method reorders operation groups by sequencing the given groups to a new position. Example:
      operation groups of the program: [C0, C1, C2, C3, C4, C5]
      Switch C4 and C1 after C2.
      Input:
      operationGroupsToSequence = [CO4, CO1],
      refOperationGroup = CO2,
      insertType = SequenceInsertionType::InsertAfterRef
      Resulting operation groups after sequencing:
      [C0 C2, C4, C1, C3, C5]
      
      Args:
         operationGroupsToSequence: list of CENPyOlpOperationGroup objects to sequence
         referenceOperationGroup: Reference operation groups
         insertLocation: The insert-type: SequenceInsertionType::InsertAfterRef or SequenceInsertionType::InsertBeforeRef
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise
      """
      ...
   
   def CanSequenceOperationGroups(self, operationGroupsToCheck: list, refOperationGroup: CENPyOlpOperationGroup, insertLocation: SequenceInsertionType) -> int:
      """Checks if operation groups could be sequenced using SequenceOperationGroups() method.
      
      Args:
         refOperationGroup: Reference operation groups
         insertLocation: The insert-type: SequenceInsertionType::InsertAfterRef or SequenceInsertionType::InsertBeforeRef
         operationGroupsToCheck: The list of CENPyOlpOperationGroup objects to be checked
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise
      """
      ...
   
   def MoveOperationGroupsToController(self, operationGroupsToMove: list, refController: CENPyOlpController) -> int:
      """Moves the given operation groups to the active program of the specified controller.
      If the controller has no active program yet, a new default program is created.
      
      Args:
         operationGroupsToMove: The list of CENPyOlpOperationGroup objects to move.
         refController: Target controller whose active program receives the operation groups.
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise.
      """
      ...
   
   def MoveOperationGroupsToProgram(self, operationGroupsToMove: list, refProgram: CENPyOlpProgram) -> int:
      """Moves the given operation groups to the specified program.
      If the program is not active, the operation groups will still be moved to it.
      
      Args:
         operationGroupsToMove: The list of CENPyOlpOperationGroup objects to move.
         refProgram: Target program to which the operation groups will be moved.
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise.
      """
      ...
   
   def GetComputeHandler(self, activeProgram: CENPyOlpProgram) -> CENPyOlpComputeHandler:
      """Get the compute handler of the parent controller.
      
      Args:
         activeProgram: The active program on the active controller.
      
      Returns:
         Compute handler as CENPyOlpComputeHandler object.
      """
      ...
   
   def GetInterpolationHandler(self, activeProgram: CENPyOlpProgram) -> CENPyOlpInterpolationHandler:
      """Get an interpolation handler.
      
      Args:
         activeProgram: The active program on the active controller.
      
      Returns:
         Interpolation handler.
      """
      ...
   
   def GetTeachHandler(self, activeProgram: CENPyOlpProgram) -> CENPyOlpTeachHandler:
      """Get the teach handler for the current session.
      
      Args:
         activeProgram: The active program on the active controller.
      
      Returns:
         Teach handler.
      """
      ...
   
   def GetEventHandler(self) -> CENPyOlpEventHandler:
      """Get the event handler.
      
      Returns:
         Event handler.
      """
      ...
   
   def RunAutomatedPathOptimizationOnOperations(self, listOfOperations: list) -> int:
      """Performs automated path optimization on the given operations.
      
      Args:
         listOfOperations: List of CENPyOlpOperation objects to optimize.
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise
      """
      ...
   
   def RunAutomatedLinkPathOptimizationOnOperations(self, listOfOperations: list) -> int:
      """Performs automated link-path optimization on the given operations.
      A link path is the path up to approach of an given operation, starting from the retract of the previous operation.
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise
      """
      ...
   
   def RemoveAutomatedPathOptimizationOnOperations(self, listOfOperations: list) -> int:
      """Removes automated path optimization from the given operations.
      
      Args:
         listOfOperations: List of CENPyOlpOperation objects to remove path optimization from.
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise
      """
      ...
   
   def RemoveAutomatedLinkOptimizationOnOperations(self, listOfOperations: list) -> int:
      """Removes automated link-path optimization from the given operations.
      A link path is the path up to approach of an given operation, starting from the retract of the previous operation.
      
      Args:
         listOfOperations: List of CENPyOlpOperation objects to remove link-path optimization from.
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise
      """
      ...
   
   def GetAllProcessGeometries(self) -> list[CENPyOlpProcessGeometryOperator]:
      """Returns all process geometries.
      
      Returns:
         List of CENPyOlpProcessGeometryOperator process geometries.
      """
      ...
   
