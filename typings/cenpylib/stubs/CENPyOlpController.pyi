"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpActor import *
from .CENPyOlpAttribute import *
from .CENPyOlpAttributeBool import *
from .CENPyOlpAttributeDouble import *
from .CENPyOlpAttributeInt import *
from .CENPyOlpAttributeString import *
from .CENPyOlpController import *
from .CENPyOlpFrame import *
from .CENPyOlpMatrix import *
from .CENPyOlpOperation import *
from .CENPyOlpPort import *
from .CENPyOlpProgram import *
from .CENPyOlpResource import *
from .CENPyOlpSensor import *

class CENPyOlpController:
   def GetName(self) -> str:
      """Get the controller name.
      
      Returns:
         Controller name.
      """
      ...
   
   def GetControllerType(self) -> int:
      """Get the controller type.
      
      Returns:
         Controller type.
      """
      ...
   
   def GetManufacturer(self) -> str:
      """Get the controller manufacturer.
      
      Returns:
         Controller manufacturer.
      """
      ...
   
   def GetSeries(self) -> str:
      """Get the controller series.
      
      Returns:
         Controller series.
      """
      ...
   
   def GetModel(self) -> str:
      """Get the controller model.
      
      Returns:
         Controller model.
      """
      ...
   
   def GetActors(self, itemType: int, itemSubType: int, actorType: int) -> list[CENPyOlpActor]:
      """Returns the attached actors of specified type.
      
      Returns:
         List of CENPyOlpActor objects, actors that respect the given filters..
      """
      ...
   
   def GetSensors(self, itemType: int, itemSubType: int, sensorType: int) -> list[CENPyOlpSensor]:
      """Gets all sensors which are on a controlled item.
      
      Args:
         itemType: Filter for the controlled items.
         itemSubType: Filter for the controlled items, applied together with itemType.
         sensorType: Filter for the sensors.
      
      Returns:
         List of CENPyOlpSensor objects, sensors that respect the given filters.
      """
      ...
   
   def GetSignalNumber(self, signalName: str) -> int:
      """Searches for the first signal with the given name, found on a controller signal connection for this controller,
      and returns its signal number.
      
      Args:
         signalName: Signal name to search for.
      
      Returns:
         The signal number of the found signal.
      """
      ...
   
   def GetUuId(self) -> str:
      """Gets the controller's unique ID.
      
      Returns:
         Controller's unique ID.
      """
      ...
   
   def GetActiveToolFrameIndex(self) -> int:
      """Gets the index of the active tool frame.
      
      Returns:
         Active tool frame index.
      """
      ...
   
   def GetActiveBaseFrameIndex(self) -> int:
      """Gets the index of the active base frame.
      
      Returns:
         Active base frame index.
      """
      ...
   
   def GetActiveToolFrameMatrix(self) -> CENPyOlpMatrix:
      """Gets the matrix of the active tool frame.
      
      Returns:
         Active tool frame matrix.
      """
      ...
   
   def GetActiveBaseFrameMatrix(self) -> CENPyOlpMatrix:
      """Gets the matrix of the active base frame.
      
      Returns:
         Active base frame matrix.
      """
      ...
   
   def GetActiveToolFrameName(self) -> str:
      """Get the tool frame name of the active tool.
      
      Returns:
         Tool frame name of the active tool.
      """
      ...
   
   def GetActiveToolResourceName(self) -> str:
      """Get the resource name of the active tool.
      
      Returns:
         Resource name of the active tool.
      """
      ...
   
   def GetResources(self, itemType: int, itemSubType: int) -> list[CENPyOlpResource]:
      """Gets resources that are controlled by this controller.
      
      Args:
         itemType: Item type to filter the resources by.
         itemSubType: Item sub type to filter the resources by
      
      Returns:
         List of CENPyOlpResource objects, resources that respect the given filters.
      """
      ...
   
   def GetMainResourcesMaxTCPFeedrate(self) -> float:
      """Returns the max TCP feedrate of main resource of the controller.
      
      Returns:
         Value of the maximum resource feedrate.
      """
      ...
   
   def IsTeamController(self) -> bool:
      """Returns whether the controller is a team controller.
      
      Returns:
         True if team controller is selected.
      """
      ...
   
   def GetTeamController(self) -> CENPyOlpController:
      """Returns the team controller current controller is connected to. If there is no team controller, returns a nullptr.
      
      Returns:
         Connected team controller.
      """
      ...
   
   def GetControllers(self) -> list[CENPyOlpController]:
      """Returns all controllers connected to this controller.
      
      Returns:
         List of CENPyOlpController objects, controllers connected to this one.
      """
      ...
   
   def GetProgramNames(self) -> list:
      """Returns a list of program names on this controller.
      
      Returns:
         List of program names.
      """
      ...
   
   def GetPrograms(self) -> list[CENPyOlpProgram]:
      """Returns a list of programs on this controller.
      
      Returns:
         List CENPyOlpProgram of programs.
      """
      ...
   
   def CreateProgram(self, name: str="", initStateName: str="", isMain: bool=True) -> CENPyOlpProgram:
      """Creates a new controller program and sets it active.
      
      Args:
         name: Name of the program to create.
         initStateName: Name of the initial state to be used or to be created.
         isMain: If True, a Main program will be created, otherwise a sub-program.
      
      Returns:
         Newly created program.
      """
      ...
   
   def GetLogicPortByName(self, portName: str) -> CENPyOlpPort:
      """Returns the first logic port found on the current controller with the given name.
      
      Args:
         portName: Logic port name to search for.
      
      Returns:
         Olp port.
      """
      ...
   
   def GetOutputDirectory(self) -> str:
      """Returns the download output directory of the program.
      First gets the root download directory of an active program, and if it is empty, gets the output directory from the translator.
      
      Returns:
         File path to the output directory.
      """
      ...
   
   def GetEtwoLanguage(self) -> str:
      """Returns the language setting of E2 as a String (de-DE, en-US, fr-FR, ja-JP, zh-CN).
      
      Returns:
         the Language String.
      """
      ...
   
   def GetAttributeByName(self, attributeName: str) -> CENPyOlpAttribute:
      """Gets a user-defined attribute by the given name.
      
      Args:
         attributeName: Name of the attribute to find.
      
      Returns:
         Olp attribute.
      """
      ...
   
   def GetAttributeIntegerByName(self, attributeName: str) -> CENPyOlpAttributeInt:
      """Gets the Integer attribute by the given name.
      
      Args:
         attributeName: Name of the attribute to find.
      
      Returns:
         Integer attribute.
      """
      ...
   
   def GetAttributeDoubleByName(self, attributeName: str) -> CENPyOlpAttributeDouble:
      """Gets the Double attribute by the given name.
      
      Args:
         attributeName: Name of the attribute to find.
      
      Returns:
         Double attribute.
      """
      ...
   
   def GetAttributeStringByName(self, attributeName: str) -> CENPyOlpAttributeString:
      """Gets the String attribute by the given name.
      
      Args:
         attributeName: Name of the attribute to find.
      
      Returns:
         String attribute.
      """
      ...
   
   def GetAttributeBoolByName(self, attributeName: str) -> CENPyOlpAttributeBool:
      """Gets the Bool attribute by the given name.
      
      Args:
         attributeName: Name of the attribute to find.
      
      Returns:
         Bool attribute.
      """
      ...
   
   def GetLastGeneratedFilePathsFromDownload(self) -> list:
      """Gets the absolute file paths generated during the last download.
      
      Returns:
         Absolute paths to the last generated files. It is empty if the download is not done yet.
      """
      ...
   
   def GetLastSelectedFilePathsFromUpload(self) -> list:
      """Gets the absolute file paths selected during the last upload.
      
      Returns:
         Absolute paths to the last selected files. It is empty if the upload is not done yet.
      """
      ...
   
   def DownloadProgramByName(self, programName: str) -> int:
      """Downloads the program specified by its name from the current controller.
      
      Args:
         programName: Name of the program to find and download, if it exists.
      
      Returns:
         ERR_NO_ERROR(0) if completed successful, error code otherwise.
      """
      ...
   
   def GetWeldingDataSetsFromDataBase(self) -> list:
      """Get defined welding data sets from weld database of the active controller
      
      Returns:
         Defined welding data sets from weld database of the active controller.
      """
      ...
   
   def GetActiveProgram(self) -> CENPyOlpProgram:
      """Get active controller program.
      
      Returns:
         Active created program.
      """
      ...
   
   def SetActiveProgram(self, activeProgram: CENPyOlpProgram) -> int:
      """Set active program on controller.
      <param name="activeProgram">Set active program on controller.</param>
      
      Args:
         activeProgram: Set active program on controller.
      
      Returns:
         None
      """
      ...
   
   def CalculateTotalTimeForSequenceBalance(self) -> int:
      """Method to calculate the total time for all components from active program of the current controller
      
      Returns:
         0 if calculation was done with no errors
      """
      ...
   
   def CalculateTimeForOperationInSequenceBalance(self, operation: CENPyOlpOperation) -> int:
      """Method to start calculate the time for given operation
      
      Args:
         operation: Operation to calculate time
      
      Returns:
         0 if calculation was done with no errors
      """
      ...
   
   def GetToolFrames(self) -> list[CENPyOlpFrame]:
      """Retrieves a list of tool frames associated with the controller.
      
      Returns:
         A list containing the tool frames as CENPyOlpFrame objects.
      """
      ...
   
   def GetBaseFrames(self) -> list[CENPyOlpFrame]:
      """Retrieves a list of base frames associated with the controller.
      
      Returns:
         A list containing the base frames as CENPyOlpFrame objects.
      """
      ...
   
   def SetActiveToolFrame(self, frame: CENPyOlpFrame):
      """Sets the active tool frame on the controller.
      
      Args:
         frame: The tool frame to set as active.
      """
      ...
   
   def SetActiveBaseFrame(self, frame: CENPyOlpFrame):
      """Sets the active base frame on the controller.
      
      Args:
         frame: The base frame to set as active.
      """
      ...
   
