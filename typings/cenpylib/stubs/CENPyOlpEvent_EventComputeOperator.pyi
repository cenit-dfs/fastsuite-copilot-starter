"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from typing import overload
from .CENPyOlpAttribGetter import *
from .CENPyOlpAttribSetter import *
from .CENPyOlpController import *
from .CENPyOlpEventOperator import *
from .CENPyOlpLogOperator import *
from .CENPyOlpMatrix import *
from .CENPyOlpPoint import *
from .CENPyOlpPosition import *
from .CENPyOlpSeamFindingOperator import *
from .CENPyOlpTouchSensingOperator import *
from .CENPyOlpTpElement import *
from .CENPyOlpVector import *

class CENPyOlpEvent_EventComputeOperator:
   def GetAttribGetter(self) -> CENPyOlpAttribGetter:
      """Get attribute getter interface.
      
      Returns:
         Attribute getter interface.
      """
      ...
   
   def GetAttribSetter(self) -> CENPyOlpAttribSetter:
      """Get attribute setter interface.
      
      Returns:
         Attribute setter interface.
      """
      ...
   
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Gets logger operator.
      
      Returns:
         Logger operator.
      """
      ...
   
   def CreateMatrix(self) -> CENPyOlpMatrix:
      """Creates a new unit matrix.
      
      Returns:
         Newly created matrix
      """
      ...
   
   def CreatePoint(self, x: float, y: float, z: float) -> CENPyOlpPoint:
      """Creates a point with the given coordinates
      
      Args:
         x: x-coordinate
         y: y-coordinate
         z: z-coordinate
      
      Returns:
         Newly created point
      """
      ...
   
   def CreateVector(self, x: float, y: float, z: float) -> CENPyOlpVector:
      """Creates a IOlpVector with the given directions
      
      Args:
         x: X-direction
         y: Y-direction
         z: Z-direction
      
      Returns:
         Newly create vector
      """
      ...
   
   def GetRefTpElement(self) -> CENPyOlpTpElement:
      """Each olp event definition is attached to a toolpath element, which is the reference toolpath element.
      
      Returns:
         Reference toolpath element of the event definition
      """
      ...
   
   def MoveLin(self, target: CENPyOlpMatrix) -> CENPyOlpTpElement:
      """Adds a "move linear" element at the end.
      
      Args:
         target: target matrix of the move linear element.
      
      Returns:
         Linear toolpath element added.
      """
      ...
   
   @overload
   def MoveCir(self, target: CENPyOlpMatrix, via: CENPyOlpMatrix) -> CENPyOlpTpElement:
      """Adds a circular move element at the end
      
      Args:
         target: target point matrix of the move circular
         via: via point matrix of the move circular
      
      Returns:
         Circular toolpath element added.
      """
      ...
   
   @overload
   def MoveCir(self, target: CENPyOlpMatrix, radius: float, direction: int) -> CENPyOlpTpElement:
      """Adds a circular move element at the end. The circular move is in the plane constructed by initial tangent vector of reference point and
      the vector connecting reference with new target point.
      
      Args:
         target: target point matrix of the move circular (if position is not on circle it will be fitted to be on the circle)
         radius: circle radius
         direction: direction of circle (clockwise or counter clockwise)
      
      Returns:
         Circular toolpath element added with direction of target (position might change)
      """
      ...
   
   @overload
   def MoveCir(self, angle: float, radius: float) -> CENPyOlpTpElement:
      """Adds a circular move element at the end. The circular movement is within the xy plane of the reference point. The end tangent is the circle
      tangent at the endpoint.
      
      Args:
         angle: opening angle of circle
         radius: circle radius
      
      Returns:
         Circular toolpath element added.
      """
      ...
   
   def MoveTangentCir(self, start: CENPyOlpMatrix, end: CENPyOlpMatrix, tangentTo: int) -> CENPyOlpTpElement:
      """Adds a circular move element tangential to a matrix
      
      Args:
         start: start point matrix of the move circular
         end: end point matrix of the move circular
         tangentTo: tangent to start or end : UseTangentOf::Start, UseTangentOf::End
      
      Returns:
         Circular toolpath element added.
      """
      ...
   
   def MovePTP(self, target: CENPyOlpMatrix) -> CENPyOlpTpElement:
      """Adds a point to point move element at the end
      
      Args:
         target: target matrix of the move
      
      Returns:
         point-to-point toolpath element added.
      """
      ...
   
   def SkipPath(self, length: float, includeStartAndEnd: bool):
      """Skips the toolpath elements for a given length.
      
      Args:
         length: The length to be skipped.
         includeStartAndEnd: Flag determining whether or not to include start and end point.
      """
      ...
   
   def GetInitialPathMatrixByLength(self, length: float) -> CENPyOlpMatrix:
      """Gets initial path matrix of toolpath element at given length.
      Remark: When at given length no toolpath element exists, temporary one is created (deleted after usage immediately).
      
      Args:
         length: length of path where matrix is calculated.
      
      Returns:
         Matrix at given length, None if no one could be calculated.
      """
      ...
   
   def GetRefToolpathElementPosition(self) -> CENPyOlpMatrix:
      """Determines the base frame position of the reference element of an event.
      Be aware: This will return nullptr if it is not called on an OlpEventDefinition.
      
      Returns:
         Nullptr or the base frame position of the reference toolpath element.
      """
      ...
   
   def GetCurrentToolFrameIndex(self) -> int:
      """Get the current tool frame index of the parent operation.
      
      Returns:
         Tool frame index.
      """
      ...
   
   def GetCurrentToolResourceName(self) -> int:
      """Get the resource name of the active tool.
      
      Returns:
         Resource name of the active tool.
      """
      ...
   
   def GetCurrentBaseFrameIndex(self) -> int:
      """Get the current base frame index of the parent operation.
      
      Returns:
         Base frame index.
      """
      ...
   
   def GetCurrentToolFrameMatrix(self) -> CENPyOlpMatrix:
      """Get the current tool frame matrix of the parent operation.
      
      Returns:
         Tool frame matrix.
      """
      ...
   
   def GetCurrentBaseFrameMatrix(self) -> CENPyOlpMatrix:
      """Get the current base frame matrix of the parent operation.
      
      Returns:
         Base frame matrix.
      """
      ...
   
   def GetController(self) -> CENPyOlpController:
      """Gets OLP controller.
      
      Returns:
         OLP controller.
      """
      ...
   
   def GetEventOperator(self) -> CENPyOlpEventOperator:
      """Gets the event operator for managing events.
      
      Returns:
         Event operator.
      """
      ...
   
   def SetTechnologyRequestId(self, element: CENPyOlpTpElement, techRequestId: int):
      """Sets a technology request ID to the given toolpath element.
      This technology request id can be used to identify toolpath elements in later executed rules.
      
      Args:
         element: Element to be marked
         techRequestId: Technology request ID
      """
      ...
   
   def GetTouchSensingOperator(self) -> CENPyOlpTouchSensingOperator:
      """Gets a TouchSensing Operator which contains touch sensing positions.
      
      Returns:
         TouchSensing operator.
      """
      ...
   
   def GetSeamFindingOperator(self) -> CENPyOlpSeamFindingOperator:
      """Gets a SeamFinding Operator which contains SeamFinding positions.
      
      Returns:
         SeamFinding operator.
      """
      ...
   
   def GetTechTabFolder(self) -> int:
      """Gets the technology table folder path.
      If the relative path contains a file name with extension then it will return the path to that file.
      
      Args:
         relativePath: Name of a file/relative path to a file.
         feedbackErrorWhenFileNotFound: By default (True) a feedback error is passed when file not found.
      
      Returns:
         Technology table folder or a file path.
      """
      ...
   
   @overload
   def GetTpElementPosition(self, tpElement: CENPyOlpTpElement, posRelation: int) -> CENPyOlpPosition:
      """Get the position of the toolpath element.
      
      Args:
         tpElement: Reference toolpath element.
         posRelation: Relation of the position.
      
      Returns:
         Toolpath element position.
      """
      ...
   
   @overload
   def GetTpElementPosition(self, tpElement: CENPyOlpTpElement, posRelation: int, baseFrameIndex: int) -> CENPyOlpPosition:
      """Get the position of the toolpath element relative to the given base frame, specified by its index.
      
      Args:
         tpElement: Reference toolpath element.
         posRelation: Relation of the position.
         baseFrameIndex: Base frame index.
      
      Returns:
         Toolpath element position.
      """
      ...
   
   def IsEventCreatedAutomatically(self) -> bool:
      """Get if the reference Event was created by a rule, another event, or inserted manually.
      
      Returns:
         True if the Event was created by a rule or by another Event, False if inserted manually.
      """
      ...
   
   @overload
   def ExecuteBrushEventCompute(self, brushNumber: int, gunNumber: int):
      """Executes everything that needs to be done for the compute of a brush event. That is an event that sets a specific brush number to a specific gun number. Gun number 0 means all guns.
      
      Args:
         brushNumber: The number of the brush to be set
         gunNumber: The number of the gun for which the brush should be set. 0 means all guns.
      """
      ...
   
   @overload
   def ExecuteBrushEventCompute(self, brushNumber: int, gunNumber: int, exactStop: bool, triggerRelatedToStart: bool, triggerTime: float, triggerDistance: float):
      """Executes everything that needs to be done for the compute of a brush event. That is an event that sets a specific brush number to a specific gun number. Gun number 0 means all guns.
      
      Args:
         brushNumber: The number of the brush to be set
         gunNumber: The number of the gun for which the brush should be set. 0 means all guns.
         exactStop: Exact stop on event. Default = True.
         triggerRelatedToStart: Trigger delta related to start(True) or end point(False). Default = True.
         triggerDistance: Trigger distance
         triggerTime: Trigger time
      """
      ...
   
   @overload
   def ExecuteGunEventCompute(self, gunState: bool, gunNumber: int):
      """Executes everything that needs to be done for the compute of a gun event. That is an event that turns a specific gun number on or off. Gun number 0 means all guns.
      
      Args:
         gunState: Whether to turn the gun on or off.
         gunNumber: The number of the gun to be turned on or off. 0 means all guns.
      """
      ...
   
   @overload
   def ExecuteGunEventCompute(self, gunState: bool, gunNumber: int, exactStop: bool, triggerRelatedToStart: bool, triggerTime: float, triggerDistance: float):
      """Executes everything that needs to be done for the compute of a gun event. That is an event that turns a specific gun number on or off. Gun number 0 means all guns.
      
      Args:
         gunState: Whether to turn the gun on or off.
         gunNumber: The number of the gun to be turned on or off. 0 means all guns.
         exactStop: Exact stop on event. Default = True.
         triggerRelatedToStart: Trigger delta related to start(True) or end point(False). Default = True.
         triggerDistance: Trigger distance
         triggerTime: Trigger time
      """
      ...
   
   def IsPythonEvent(self) -> bool:
      """Checks if the reference event is a C++ or python event.
      
      Returns:
         True if it is a python event, False if not.
      """
      ...
   
   def OverwriteMotion(self, targetTpe: int, motionType: int, via: CENPyOlpMatrix):
      """Overwrites motion type of target toolpath element
      
      Args:
         targetTpe: target toolpath element to be modified
         motionType: target motion type to be set
         via: initial matrix to be set to via point when target motion type is circular
      """
      ...
   
