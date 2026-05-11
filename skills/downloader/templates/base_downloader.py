"""
Base Downloader Template — FASTSUITE E2
Copy this file to OLPTranslators/<VENDOR>/ and customize for your robot controller.
Replace "MyVendor" with your vendor/controller name throughout.

Supports: PTP, LIN, CIRC motions | Speed, Accuracy, Acceleration events |
          LogicPort, SetResourcePort, WaitForResourcePort signals |
          TextEvent, Dwell | Tool & Base frame mapping
"""

import sys, inspect, os
sys.dont_write_bytecode = True
sys.path.append(str(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

from cenpylib import FileUtility
from cenpydownload import *
from cenpyolpcore import *
from centypes import *

# --- Class registration (REQUIRED) ---
DOWNLOAD_CLASS_NAME = "MyVendor"

class MyVendor(Downloader):
   """Base downloader template.
   Customize the Output* methods to emit vendor-specific robot code.
   """
   FILE_EXTENSION = '.src'  # Change to your vendor's extension (.mod, .ls, .jbi, etc.)

   def __init__(self) -> None:
      super().__init__()
      self.FileUtil = FileUtility()
      self.outputFilePath = ''
      self.outputDir = ''
      self.programName = ''
      # Output buffers
      self.Header = []
      self.Source = []
      self.Footer = []
      # Current state
      self.CurrentToolIndex = 0
      self.CurrentBaseIndex = 0
      self.CurrentToolName = ''
      self.CurrentBaseName = ''
      self.CurrentLinVelocity = 0.5     # m/s
      self.CurrentPtpVelocity = 20.0    # %
      self.CurrentLinAccuracy = 50.0
      self.CurrentPtpAccuracy = 50.0
      self.CurrentAccuracyActive = False

   # ==================== LIFECYCLE CALLBACKS ====================

   def Initialize(self, operator: DULPythonDownloadOperator):
      """Called ONCE per download. Setup shared resources here."""
      logger = operator.GetLogOperator()
      logger.LogDebug("MyVendor Initialize called")

   def OutputHeader(self, operator: DULPythonDownloadOperator, controller: DULPythonController):
      """Build program header from controller info."""
      logger = operator.GetLogOperator()
      logger.LogDebug("MyVendor OutputHeader called")
      program = controller.GetActiveProgram()
      self.outputDir = controller.GetOutputDirectory()
      self.programName = program.GetName()
      # --- CUSTOMIZE: Add your header syntax ---
      self.Header.append('; Program: ' + self.programName)
      self.Header.append('; Controller: ' + controller.GetName())
      self.Header.append('; Manufacturer: ' + controller.GetManufacturer())

   def ProgramStart(self, operator: DULPythonDownloadOperator, program: DULPythonProgram):
      logger = operator.GetLogOperator()
      logger.LogDebug("MyVendor ProgramStart: " + program.GetName())

   def ProgramEnd(self, operator: DULPythonDownloadOperator, program: DULPythonProgram):
      logger = operator.GetLogOperator()
      logger.LogDebug("MyVendor ProgramEnd: " + program.GetName())
      # --- CUSTOMIZE: Add program end syntax ---
      self.Footer.append('; END')

   def OperationGroupStart(self, operator: DULPythonDownloadOperator, operationGroup: DULPythonOperationGroup):
      logger = operator.GetLogOperator()
      logger.LogDebug("MyVendor OperationGroupStart: " + operationGroup.GetName())
      self.Source.append('; --- Group: ' + operationGroup.GetName() + ' ---')

   def OperationGroupEnd(self, operator: DULPythonDownloadOperator, operationGroup: DULPythonOperationGroup):
      pass

   def OperationStart(self, operator: DULPythonDownloadOperator, operation: DULPythonOperation):
      logger = operator.GetLogOperator()
      logger.LogDebug("MyVendor OperationStart: " + operation.GetName())
      self.Source.append('; Operation: ' + operation.GetName())
      # Read tool and base frame for this operation
      usedBase = operation.GetUsedBaseProfile()
      usedTool = operation.GetUsedToolProfile()
      self.CurrentBaseIndex = usedBase.GetIndex()
      self.CurrentToolIndex = usedTool.GetIndex()
      self.CurrentBaseName = usedBase.GetName()
      self.CurrentToolName = usedTool.GetName()

   def OperationEnd(self, operator: DULPythonDownloadOperator, operation: DULPythonOperation):
      pass

   # ==================== MOTION HANDLING ====================

   def HandleMotion(self, operator: DULPythonDownloadOperator, motion: DULPythonMotion):
      """Main motion handler. Processes events-before, position, motion command, events-after."""
      logger = operator.GetLogOperator()
      # Process events before this motion
      for event in motion.GetEventsBefore():
         self.HandleEvent(operator, event, motion)
      # Output position and motion command
      if not motion.IsReferenceMotion():
         position = motion.GetPosition()
         self.OutputPositionData(operator, position)
         if motion.IsLinearMotion():
            self.OutputMotionCommand(operator, "LIN", position.GetName())
         elif motion.IsCircularMotion():
            viaPos = motion.GetViaPosition()
            self.OutputPositionData(operator, viaPos)
            self.OutputMotionCommand(operator, "CIRC", position.GetName(), viaPos.GetName())
         else:
            self.OutputMotionCommand(operator, "PTP", position.GetName())
      # Process events after this motion
      for event in motion.GetEventsAfter():
         self.HandleEvent(operator, event, motion)

   def OutputPositionData(self, operator: DULPythonDownloadOperator, position: DULPythonPosition):
      """Output position data (coordinates or joint values)."""
      posName = position.GetName()
      targetType = position.GetTargetType()
      if targetType == TargetType.Joint:
         joints = position.GetMainJointValues()
         jointValues = ','.join(['{:.3f}'.format(jv[1]) for jv in joints])
         # --- CUSTOMIZE: Your joint position syntax ---
         self.Source.append('; POS ' + posName + ' = [' + jointValues + ']')
      else:
         xyz = position.GetXYZ()
         angles = position.GetOrientation()
         # --- CUSTOMIZE: Your cartesian position syntax ---
         # Note: E2 provides meters → multiply by 1000 for mm
         self.Source.append('; POS ' + posName + ' = ['
            + '{:.3f}'.format(xyz[0]*1000) + ','
            + '{:.3f}'.format(xyz[1]*1000) + ','
            + '{:.3f}'.format(xyz[2]*1000) + ','
            + '{:.3f}'.format(angles[0]) + ','
            + '{:.3f}'.format(angles[1]) + ','
            + '{:.3f}'.format(angles[2]) + ']')
      # External axes
      externals = position.GetExternalJointValues()
      externals.sort(key=lambda ext: ext[0].GetJointIndex())
      for joint_obj, value in externals:
         if joint_obj.GetJointType() == JointKinematicType.Prismatic:
            value = value * 1000  # m → mm

   def OutputMotionCommand(self, operator: DULPythonDownloadOperator, motionType: str, posName: str, viaName: str = ''):
      """Output the actual motion command."""
      # --- CUSTOMIZE: Your vendor-specific motion syntax ---
      if motionType == 'CIRC':
         self.Source.append(motionType + ' ' + viaName + ', ' + posName)
      else:
         self.Source.append(motionType + ' ' + posName)

   # ==================== EVENT HANDLING ====================

   def HandleEvent(self, operator: DULPythonDownloadOperator, event: DULPythonEvent, motion: DULPythonMotion):
      """Dispatch events by name."""
      self.HandleBuildInEvents(operator, event)
      # Process any motions owned by this event
      for eventMotion in event.GetMotions():
         self.HandleMotion(operator, eventMotion)

   def HandleBuildInEvents(self, operator: DULPythonDownloadOperator, event: DULPythonEvent):
      """Dispatch built-in events."""
      name = event.GetName()
      if name == 'Speed':
         self.SetSpeed(operator, event)
      elif name == 'Accuracy':
         self.SetAccuracy(operator, event)
      elif name == 'Acceleration':
         self.SetAcceleration(operator, event)
      elif name == 'TextEvent':
         self.TextEvent(operator, event)
      elif name == 'Dwell':
         self.DwellEvent(operator, event)
      elif name in ('LogicPort', 'SetResourcePort', 'WaitForResourcePort'):
         self.LogicPortEvent(operator, event)

   def SetSpeed(self, operator: DULPythonDownloadOperator, event: DULPythonEvent):
      pathtype = ''
      speed = 0.0
      for attr in event.GetAttributes():
         if attr.GetName() == 'Value':
            speed = attr.GetValue()
         elif attr.GetName() == 'PathType':
            pathtype = attr.GetValue()
      if pathtype == 'Contour':
         self.CurrentLinVelocity = float(speed)
      else:
         self.CurrentPtpVelocity = float(speed)

   def SetAccuracy(self, operator: DULPythonDownloadOperator, event: DULPythonEvent):
      criteria = ''
      accuracy = 0.0
      pathtype = ''
      for attr in event.GetAttributes():
         if attr.GetName() == 'Value':
            accuracy = attr.GetValue()
         elif attr.GetName() == 'PathType':
            pathtype = attr.GetValue()
         elif attr.GetName() == 'Criteria':
            criteria = attr.GetValue()
      if criteria == 'On':
         self.CurrentAccuracyActive = True
      elif criteria == 'Off':
         self.CurrentAccuracyActive = False

   def SetAcceleration(self, operator: DULPythonDownloadOperator, event: DULPythonEvent):
      pass  # --- CUSTOMIZE: Store acceleration if needed ---

   def TextEvent(self, operator: DULPythonDownloadOperator, event: DULPythonEvent):
      text = ''
      isComment = True
      for attr in event.GetAttributes():
         if attr.GetName() == 'Text':
            text = attr.GetValue()
         elif attr.GetName() == 'IsComment':
            isComment = attr.GetValue()
      if isComment:
         self.Source.append('; ' + text)  # --- CUSTOMIZE: Your comment syntax ---
      else:
         self.Source.append(text)

   def DwellEvent(self, operator: DULPythonDownloadOperator, event: DULPythonEvent):
      time = 0.0
      for attr in event.GetAttributes():
         if attr.GetName() == 'Value':
            time = attr.GetValue()
      # --- CUSTOMIZE: Your dwell/wait syntax ---
      self.Source.append('WAIT ' + str(time))

   def LogicPortEvent(self, operator: DULPythonDownloadOperator, event: DULPythonEvent):
      """Handle signal events (LogicPort, SetResourcePort, WaitForResourcePort).
      SetResourcePort/WaitForResourcePort are MULTI-SIGNAL containers:
        attributes repeat in groups of (SignalName, SignalAddress, SignalNumber, SignalValue).
      LogicPort is a single signal with subtype dispatch.
      """
      logger = operator.GetLogOperator()
      # Level 1: dispatch on EventType enum
      eventType = event.GetEventType()
      if eventType == EventType.SetResourcePort or eventType == EventType.WaitForResourcePort:
         # Collect multiple signals from the attribute list
         signals = []
         currentSignal = {}
         for attr in event.GetAttributes():
            name = attr.GetName()
            if name == 'SignalName':
               if currentSignal.get('SignalName'):
                  signals.append(currentSignal)
               currentSignal = {'SignalName': attr.GetValue(), 'SignalAddress': '', 'SignalNumber': '', 'SignalValue': ''}
            elif name == 'SignalAddress':
               currentSignal['SignalAddress'] = attr.GetValue()
            elif name == 'SignalNumber':
               currentSignal['SignalNumber'] = str(attr.GetValue())
            elif name == 'SignalValue':
               currentSignal['SignalValue'] = str(attr.GetValue())
         if currentSignal.get('SignalName'):
            signals.append(currentSignal)
         # Output one command per signal
         for sig in signals:
            if eventType == EventType.SetResourcePort:
               # --- CUSTOMIZE: Your set output syntax ---
               self.Source.append('SET OUT[' + sig['SignalNumber'] + '] = ' + sig['SignalValue'] + '  ; ' + sig['SignalName'])
            else:
               # --- CUSTOMIZE: Your wait for input syntax ---
               self.Source.append('WAIT IN[' + sig['SignalNumber'] + '] = ' + sig['SignalValue'] + '  ; ' + sig['SignalName'])
      elif eventType == EventType.LogicPort:
         # LogicPort — single signal with subtype dispatch
         eventSubType = ''
         signalName = ''
         signalNumber = ''
         signalValue = ''
         for attr in event.GetAttributes():
            name = attr.GetName()
            if name == 'EventType':
               eventSubType = attr.GetValue()
            elif name == 'SignalName':
               signalName = attr.GetValue()
            elif name == 'SignalNumber':
               signalNumber = str(attr.GetValue())
            elif name == 'SignalValue':
               signalValue = str(attr.GetValue())
         # Read typed value via specific getter for LogicPort subtypes
         if eventSubType == 'CENE2SetSignalInt':
            signalValue = str(event.GetIntegerAttribute('SignalValue', True).GetValue())
         elif eventSubType == 'CENE2SetSignalShortInt':
            signalValue = event.GetStringAttribute('SignalValue', True).GetValue()
         elif eventSubType == 'CENE2SetSignalFloat':
            signalValue = str(event.GetDoubleAttribute('SignalValue', True).GetValue())
         elif eventSubType == 'CENE2SetSignal':
            signalValue = str(event.GetBoolAttribute('SignalValue', True).GetValue())
         # Output based on set vs wait
         if 'CENE2SetSignal' in eventSubType:
            self.Source.append('SET OUT[' + signalNumber + '] = ' + signalValue + '  ; ' + signalName)
         elif eventSubType == 'CENE2WaitForSignal':
            self.Source.append('WAIT IN[' + signalNumber + '] = ' + signalValue + '  ; ' + signalName)
         else:
            logger.LogError('LogicPortEvent: Unknown subtype "' + eventSubType + '" — skipped')
      else:
         logger.LogError('LogicPortEvent: Unhandled EventType — skipped')

   # ==================== SUBPROGRAMS ====================

   def SubprogramStart(self, operator: DULPythonDownloadOperator, subprogram: DULPythonSubprogram):
      pass

   def SubProgramEnd(self, operator: DULPythonDownloadOperator, subprogram: DULPythonSubprogram):
      pass

   # ==================== FILE OUTPUT ====================

   def CreateOutputFile(self, operator: DULPythonDownloadOperator):
      self.outputFilePath = self.outputDir + '\\' + self.programName + self.FILE_EXTENSION

   def WriteOutputFile(self, operator: DULPythonDownloadOperator):
      self.FileUtil.AppendTextArrayToFile(self.outputFilePath, self.Header)
      self.FileUtil.AppendTextArrayToFile(self.outputFilePath, self.Source)
      self.FileUtil.AppendTextArrayToFile(self.outputFilePath, self.Footer)
      self.Header.clear()
      self.Source.clear()
      self.Footer.clear()

   def CloseOutputFile(self, operator: DULPythonDownloadOperator):
      operator.AddOutputFilePath(self.outputFilePath)  # REQUIRED — registers file with E2
