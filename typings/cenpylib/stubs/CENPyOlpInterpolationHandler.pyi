"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from typing import overload
from .CENPyOlpTpElement import *
from .CENPyOlpTrack import *

class CENPyOlpInterpolationHandler:
   def CreatePathInterpolation(self, startTpElement: CENPyOlpTpElement, endTpElement: CENPyOlpTpElement, types: list) -> int:
      """Create path interpolations between given toolpath elements.
      
      Args:
         startTpElement: Start toolpath element.
         endTpElement: End toolpath element.
         types: One or more types of interpolation to create.
      
      Returns:
         ERR_NO_ERROR (0) if successful, error code otherwise.
      """
      ...
   
   def DeletePathInterpolation(self, startTpElement: CENPyOlpTpElement, endTpElement: CENPyOlpTpElement, types: list) -> int:
      """Delete path interpolations between given toolpath elements.
      
      Args:
         startTpElement: Start toolpath element.
         endTpElement: End toolpath element.
         types: One or more types of interpolation to delete.
      
      Returns:
         ERR_NO_ERROR (0) if successful, error code otherwise.
      """
      ...
   
   def SwitchPathInterpolationType(self, startTpElement: CENPyOlpTpElement, endTpElement: CENPyOlpTpElement, types: list) -> int:
      """Switch path interpolations types for given toolpath elements between Relative and Absolute,
      or between JoltSmooth and JoltFix.
      
      Args:
         startTpElement: Start toolpath element.
         endTpElement: End toolpath element.
         types: One or more current types of interpolation that should be switched.
      
      Returns:
         ERR_NO_ERROR (0) if successful, error code otherwise.
      """
      ...
   
   def AddPathInterpolationSupport(self, tpElement: CENPyOlpTpElement, types: list) -> int:
      """Add given toolpath element as support for the specified types of path interpolations.
      
      Args:
         tpElement: Reference toolpath element.
         types: One or more types of interpolation to add support to.
      
      Returns:
         ERR_NO_ERROR (0) if successful, error code otherwise.
      """
      ...
   
   def RemovePathInterpolationSupport(self, tpElement: CENPyOlpTpElement, types: list) -> int:
      """Remove given toolpath element as support for the specified types of path interpolations.
      
      Args:
         tpElement: Reference toolpath element.
         types: One or more types of interpolation to remove support from.
      
      Returns:
         ERR_NO_ERROR (0) if successful, error code otherwise.
      """
      ...
   
   def CreateSurfaceInterpolation(self, startTrack: CENPyOlpTrack, endTrack: CENPyOlpTrack, types: list) -> int:
      """Create surface interpolations between given toolpath tracks.
      
      Args:
         startTrack: Start track.
         endTrack: End track.
         types: One or more types of interpolation to create.
      
      Returns:
         ERR_NO_ERROR (0) if successful, error code otherwise.
      """
      ...
   
   def DeleteSurfaceInterpolation(self, startTrack: CENPyOlpTrack, endTrack: CENPyOlpTrack, types: list) -> int:
      """Delete surface interpolations between given toolpath tracks.
      
      Args:
         startTrack: Start track.
         endTrack: End track.
         types: One or more types of interpolation to delete.
      
      Returns:
         ERR_NO_ERROR (0) if successful, error code otherwise.
      """
      ...
   
   def SwitchSurfaceInterpolationType(self, startTrack: CENPyOlpTrack, endTrack: CENPyOlpTrack, types: list) -> int:
      """Switch surface interpolations types for given toolpath tracks between Relative and Absolute,
      or between JoltSmooth and JoltFix.
      
      Args:
         startTrack: Start track.
         endTrack: End track.
         types: One or more current types of interpolation that should be switched.
      
      Returns:
         ERR_NO_ERROR (0) if successful, error code otherwise.
      """
      ...
   
   def AddSurfaceInterpolationSupport(self, track: CENPyOlpTrack, types: list) -> int:
      """Add given toolpath track as support for the specified types of surface interpolations.
      
      Args:
         track: Reference track.
         types: One or more types of interpolation to add support to.
      
      Returns:
         ERR_NO_ERROR (0) if successful, error code otherwise.
      """
      ...
   
   def RemoveSurfaceInterpolationSupport(self, track: CENPyOlpTrack, types: list) -> int:
      """Remove given toolpath track as support for the specified types of surface interpolations.
      
      Args:
         track: Reference track.
         types: One or more types of interpolation to remove support from.
      
      Returns:
         ERR_NO_ERROR (0) if successful, error code otherwise.
      """
      ...
   
   @overload
   def IsInterpolated(self, tpElement: CENPyOlpTpElement, type: int) -> bool:
      """Check whether or not the given toolpath element has the path interpolation of the given type.
      
      Args:
         tpElement: Reference toolpath element.
         type: Type of interpolation to check for.
      
      Returns:
         True if the toolpath element has interpolation of the given type, otherwise False.
      """
      ...
   
   @overload
   def IsInterpolated(self, track: CENPyOlpTrack, type: int) -> bool:
      """Check whether or not the given track has the surface interpolation of the given type.
      Track is considered as interpolated if its event based start toolpath element has interpolation.
      
      Args:
         track: Reference track.
         type: Type of interpolation to check for.
      
      Returns:
         True if the toolpath element has interpolation of the given type, otherwise False.
      """
      ...
   
   @overload
   def IsSupport(self, tpElement: CENPyOlpTpElement, type: int) -> bool:
      """Check whether or not the given toolpath element is a support of any kind for a particular interpolation type.
      
      Args:
         tpElement: Reference toolpath element.
         type: Type of interpolation to check for.
      
      Returns:
         True if the toolpath element is a support, otherwise False.
      """
      ...
   
   @overload
   def IsSupport(self, track: CENPyOlpTrack, type: int) -> bool:
      """Check whether or not the given track is a support of any kind for a particular interpolation type.
      Track is considered as a support if its event based start toolpath element is a support.
      
      Args:
         track: Reference toolpath element.
         type: Type of interpolation to check for.
      
      Returns:
         True if the track is a support, otherwise False.
      """
      ...
   
