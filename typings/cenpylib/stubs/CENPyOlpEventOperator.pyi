"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from typing import overload
from .CENPyOlpAccelerationEvent import *
from .CENPyOlpAccuracyEvent import *
from .CENPyOlpActor import *
from .CENPyOlpBoolActorEvent import *
from .CENPyOlpDwellEvent import *
from .CENPyOlpEventObject import *
from .CENPyOlpFloatArrayActorEvent import *
from .CENPyOlpSensor import *
from .CENPyOlpSetBoolSignalEvent import *
from .CENPyOlpSetFloatSignalEvent import *
from .CENPyOlpSetIntSignalEvent import *
from .CENPyOlpSetResourcePortEvent import *
from .CENPyOlpSpeedEvent import *
from .CENPyOlpSyncRobotsEvent import *
from .CENPyOlpToolEvent import *
from .CENPyOlpTpElement import *
from .CENPyOlpWaitForBoolSensorEvent import *
from .CENPyOlpWaitForBoolSignalEvent import *
from .CENPyOlpWaitForFloatSignalEvent import *
from .CENPyOlpWaitForIntSignalEvent import *
from .CENPyOlpWaitForResourcePortEvent import *

class CENPyOlpEventOperator:
   def AddEvent(self, uuId: str, pTpElement: CENPyOlpTpElement, iInsertPosition: int, execute: bool=True) -> CENPyOlpEventObject:
      """Add Technology Event on input toolpath element or at the end of the toolpath segment.
      
      Args:
         uuId: unique id of the event to be added
         pTpElement: reference toolpath element
         iInsertPosition: before or after the reference toolpath element
         execute: True = event will be computed immediately; False = event will be created but not computed, compute must be triggered separately. Default is True.
      
      Returns:
         The Event object added
      """
      ...
   
   def ExecuteEvent(self, pyEvent: CENPyOlpEventObject):
      """Triggers a recompute at the given event.
      
      Args:
         pyEvent: Event object.
      """
      ...
   
   def AddEventWaitForBoolSensor(self, target: CENPyOlpTpElement, sensor: CENPyOlpSensor, iInsertPosition: int) -> CENPyOlpWaitForBoolSensorEvent:
      """Adds a WaitForBoolSensor event to target toolpath element.
      
      Args:
         target: toolpath element where the event to be added
         sensor: the sensor to be set
         iInsertPosition: Insert position - before or after the reference toolpath element
      
      Returns:
         the added event
      """
      ...
   
   def AddEventBoolActor(self, target: CENPyOlpTpElement, actor: CENPyOlpActor, iInsertPosition: int) -> CENPyOlpBoolActorEvent:
      """Adds a BoolActor event to target toolpath element.
      
      Args:
         target: toolpath element where the event to be added
         actor: the actor to be set
         iInsertPosition: Insert position - before or after the reference toolpath element
      
      Returns:
         the added event
      """
      ...
   
   def AddEventFloatArrayActor(self, target: CENPyOlpTpElement, actor: CENPyOlpActor, iInsertPosition: int) -> CENPyOlpFloatArrayActorEvent:
      """Adds a FloatArrayActor event to target toolpath element.
      
      Args:
         target: toolpath element where the event to be added
         actor: the actor to be set
         iInsertPosition: Insert position - before or after the reference toolpath element
      
      Returns:
         the added event
      """
      ...
   
   def AddEventSetBoolSignal(self, value: bool, target: CENPyOlpTpElement, signalNumber: int, iInsertPosition: int) -> CENPyOlpSetBoolSignalEvent:
      """Adds a SetBoolSignal event to target toolpath element.
      
      Args:
         value: the bool value to be set
         target: toolpath element where the event to be added
         signalNumber: the signal number
         iInsertPosition: Insert position - before or after the reference toolpath element
      
      Returns:
         the added event
      """
      ...
   
   def AddEventSetFloatSignal(self, value: float, target: CENPyOlpTpElement, signalNumber: int, iInsertPosition: int) -> CENPyOlpSetFloatSignalEvent:
      """Adds a SetFloatSignal event to target toolpath element.
      
      Args:
         value: the float value to be set
         target: toolpath element where the event to be added
         signalNumber: the signal number
         iInsertPosition: Insert position - before or after the reference toolpath element
      
      Returns:
         the added event
      """
      ...
   
   def AddEventSetIntSignal(self, value: int, target: CENPyOlpTpElement, signalNumber: int, iInsertPosition: int) -> CENPyOlpSetIntSignalEvent:
      """Adds a SetIntSignal event to target toolpath element.
      
      Args:
         value: the integer value to be set
         target: toolpath element where the event to be added
         signalNumber: the signal number
         iInsertPosition: Insert position - before or after the reference toolpath element
      
      Returns:
         the added event
      """
      ...
   
   def AddEventWaitForBoolSignal(self, value: bool, target: CENPyOlpTpElement, signalNumber: int, iInsertPosition: int) -> CENPyOlpWaitForBoolSignalEvent:
      """Adds a WaitForBoolSignalEvent to target toolpath element.
      
      Args:
         value: the bool value to be set
         target: toolpath element where the event to be added
         signalNumber: the signal number
         iInsertPosition: Insert position - before or after the reference toolpath element
      
      Returns:
         the added event
      """
      ...
   
   def AddEventWaitForFloatSignal(self, value: float, target: CENPyOlpTpElement, signalNumber: int, iInsertPosition: int) -> CENPyOlpWaitForFloatSignalEvent:
      """Adds a WaitForFloatSignalEvent to target toolpath element.
      
      Args:
         value: the float value to be set
         target: toolpath element where the event to be added
         signalNumber: the signal number
         iInsertPosition: Insert position - before or after the reference toolpath element
      
      Returns:
         the added event
      """
      ...
   
   def AddEventWaitForIntSignal(self, value: int, target: CENPyOlpTpElement, signalNumber: int, iInsertPosition: int) -> CENPyOlpWaitForIntSignalEvent:
      """Adds a WaitForIntSignalEvent to target toolpath element.
      
      Args:
         value: the integer value to be set
         target: toolpath element where the event to be added
         signalNumber: the signal number
         iInsertPosition: Insert position - before or after the reference toolpath element
      
      Returns:
         the added event
      """
      ...
   
   def AddSpeed(self, target: CENPyOlpTpElement, iInsertPosition: int) -> CENPyOlpSpeedEvent:
      """Adds a Speed event to target toolpath element.
      
      Args:
         target: toolpath element where speed event to be added
         iInsertPosition: Insert position - before or after the reference toolpath element
      
      Returns:
         The added event
      """
      ...
   
   @overload
   def AddToolEvent(self, target: CENPyOlpTpElement, iInsertPosition: int) -> CENPyOlpToolEvent:
      """Adds a Tool event to target toolpath element.
      
      Args:
         target: toolpath element where tool event to be added
         iInsertPosition: Insert position - before or after the target toolpath element
      
      Returns:
         The tool Event added
      """
      ...
   
   @overload
   def AddToolEvent(self, target: CENPyOlpTpElement, iInsertPosition: int, exactStop: bool) -> CENPyOlpToolEvent:
      """Adds a Tool event to target toolpath element.
      
      Args:
         target: toolpath element where tool event to be added
         iInsertPosition: Insert position - before or after the target toolpath element
         exactStop: Exact stop on event.
      
      Returns:
         The tool Event added
      """
      ...
   
   def AddAccuracyEvent(self, target: CENPyOlpTpElement, iInsertPosition: int) -> CENPyOlpAccuracyEvent:
      """Adds a Accuracy event to target toolpath element.
      
      Args:
         target: toolpath element where accuracy event to be added.
         iInsertPosition: Insert position - before or after the target toolpath element
      
      Returns:
         The accuracy Event added
      """
      ...
   
   def AddDwellEvent(self, target: CENPyOlpTpElement, iInsertPosition: int) -> CENPyOlpDwellEvent:
      """Adds a Dwell event to target toolpath element.
      
      Args:
         target: The element on which the event is to be added.
         iInsertPosition: Insert position - before or after the target toolpath element
      
      Returns:
         The added event; null if adding the event fails
      """
      ...
   
   def AddSyncRobotsEvent(self, target: CENPyOlpTpElement, iInsertPosition: int) -> CENPyOlpSyncRobotsEvent:
      """Adds a Synchronize Robots event to target toolpath element.
      
      Args:
         target: toolpath element where synchronize robots event to be added.
         iInsertPosition: Insert position - before or after the target toolpath element
      
      Returns:
         The Synchronize Robots Event added
      """
      ...
   
   def AddAccelerationEvent(self, target: CENPyOlpTpElement, iInsertPosition: int) -> CENPyOlpAccelerationEvent:
      """Adds a Acceleration event to target toolpath element.
      
      Args:
         target: toolpath element where Acceleration event to be added.
         iInsertPosition: Insert position - before or after the target toolpath element
      
      Returns:
         The Acceleration Event added
      """
      ...
   
   @overload
   def AddSetResourcePortEvent(self, target: CENPyOlpTpElement, iInsertPosition: int) -> CENPyOlpSetResourcePortEvent:
      """Adds a SetResourcePort event to target toolpath element.
      
      Args:
         target: Toolpath element where the event will be added
         iInsertPosition: Insert position - before or after the target toolpath element
      
      Returns:
         The created event
      """
      ...
   
   @overload
   def AddSetResourcePortEvent(self, target: CENPyOlpTpElement, iInsertPosition: int, exactStop: bool) -> CENPyOlpSetResourcePortEvent:
      """Adds a SetResourcePort event to target toolpath element.
      
      Args:
         target: Toolpath element where the event will be added
         iInsertPosition: Insert position - before or after the target toolpath element
         exactStop: Exact stop on event.
      
      Returns:
         The created event
      """
      ...
   
   def AddWaitForResourcePortEvent(self, target: CENPyOlpTpElement, iInsertPosition: int) -> CENPyOlpWaitForResourcePortEvent:
      """Adds a WaitForResourcePort event to target toolpath element.
      
      Args:
         target: Toolpath element where the event will be added
         iInsertPosition: Insert position - before or after the target toolpath element
      
      Returns:
         The created event
      """
      ...
   
