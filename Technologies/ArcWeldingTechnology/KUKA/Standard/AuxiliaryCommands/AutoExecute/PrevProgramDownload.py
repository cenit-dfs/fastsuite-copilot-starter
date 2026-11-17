# -------------------------------------------------------------------------------------------
# Name: Update Touch Direction Vectors Before Download
# Description: Updates ApprDirX and ApprDirZ attributes in ConnectTouchProcessPointEvent
#              events to reflect current workpiece position
# Debug info: E2@localhost:5254
# Author: CENIT AG
# Changelog:
#     Version: 1.0
#        Changed by:
#        Date: 
# -------------------------------------------------------------------------------------------

# Import libraries
from centypes import *
from cenpylib import *
from cenpylib.stubs.CENPyOlpTpElement import CENPyOlpTpElement
from cenpylib.stubs.CENPyOlpEventHandler import CENPyOlpEventHandler
from cenpylib.stubs.CENPyOlpMatrix import CENPyOlpMatrix
from centypes import *
import sys, os, inspect, re
sys.dont_write_bytecode = True
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(
   inspect.getfile(inspect.currentframe()))))), "Scripts"))
import MultiLayerMetadata as ml_meta
import MultiLayerPlanner as planner

# event names
TOUCH_CONNECT_EVENT = "ConnectTouchProcessPointEvent"
ARC_ON_EVENT = "ArcOnEvent"

# Matches operation names following the "Seam_..."/"SeamN_..." convention so they can be
# disambiguated with the seam's ordinal - two seams taught as "Seam_Layer1_Pass1" are otherwise
# indistinguishable by name (seam_uuid is already unique; the display name was not).
SEAM_NAME_PATTERN = re.compile(r"^Seam\d*_(.*)$")

# Sys_Att_ProcessFlowDirection is a KUKA system attribute (Boundary conditions > "Reverse process
# direction" in the UI), not a technology-created one - it must be written through
# CENPyOlpAttribSetter.GetSystemAttribSetter().SetProcessFlowDirection(), not SetBool(name, ...).
# SetBool silently no-ops on system attribute names, which is why every captured fixture
# (including Alternating ones, which should show ~half True) has always read False.
ATTR_PROCESS_FLOW_DIRECTION = "Sys_Att_ProcessFlowDirection"

def GetCommandName():
   return "PrevProgramDownload"
   
def GetCommandUuId():
   return "A1B2C3D4-565E-4D87-9B2C-FA551B6E2D31"
   
def GetIconName():
   return "COM_ScriptsRun"

# -------------------------------------------------------------------------------------------
def ModifyActiveProgram(Operator: CENPyOlpProgramModifyOperator):
   """
   Updates ApprDirX and ApprDirZ direction vectors in all ConnectTouchProcessPointEvent
   events based on current TPE matrices (accounting for workpiece repositioning).
   """
   # get logger
   logging = Operator.GetLoggerOperator()
   logging.LogDebug("PrevProgramDownload.py: Execution started - Updating touch direction vectors.")

   # get active program
   program = Operator.GetActiveProgram()
   if program is None:
      logging.LogWarn("PrevProgramDownload.py: No active program found.")
      return

   # Runs first so the touch-vector early returns below cannot skip Multilayer planning.
   ApplyMultilayerPlan(Operator, program, logging)

   # get event handler
   eventHandler = Operator.GetEventHandler()
   if eventHandler is None:
      logging.LogWarn("PrevProgramDownload.py: Could not get event handler.")
      return

   # get all toolpath elements in the active program
   tpes = program.GetTpElements()
   if not tpes:
      logging.LogDebug("PrevProgramDownload.py: No toolpath elements found in program.")
      return

   # counters for summary
   events_updated = 0
   events_failed = 0
   tpes_processed = 0

   # iterate through all toolpath elements
   for tpe in tpes:
      try:
         # get all ConnectTouchProcessPointEvent events for this TPE
         events = eventHandler.GetEventsByName(tpe, TOUCH_CONNECT_EVENT)
         # events = eventHandler.GetEventsByName(tpe, ARC_ON_EVENT)
         
         if not events or len(events) == 0:
            continue
         
         tpes_processed += 1
         
         # get current matrix (accounts for workpiece position changes)
         try:
            currBF = Operator.GetController().GetActiveBaseFrameMatrix()
            # currBfPos = currBF.GetPosition().GetXYZ()
            # currBF_X = currBF.GetXDirection().GetXYZ()
            # currBF_Y = currBF.GetYDirection().GetXYZ()
            # currBF_Z = currBF.GetZDirection().GetXYZ()

            unalignedWorldStateMatrix = Operator.CreateMatrix()
            unalignedWorldStateMatrix = tpe.GetBaseFrameTransformedMatrixUnaligned()
            # posU = unalignedWorldStateMatrix.GetPosition().GetXYZ()
            # x2U = unalignedWorldStateMatrix.GetXDirection().GetXYZ()
            # y2U = unalignedWorldStateMatrix.GetYDirection().GetXYZ()
            # z2U = unalignedWorldStateMatrix.GetZDirection().GetXYZ()
            
            current_matrix3 = unalignedWorldStateMatrix.Multiply(currBF.Inverse(), unalignedWorldStateMatrix)
            # pos3 = current_matrix3.GetPosition().GetXYZ()
            xDir = current_matrix3.GetXDirection().GetXYZ()
            # yDir = current_matrix3.GetYDirection().GetXYZ()
            zDir = current_matrix3.GetZDirection().GetXYZ()

         except Exception as matrix_ex:
            logging.LogWarn(f"PrevProgramDownload.py: Could not get Path matrix or direction vectors for TPE '{tpe.GetName()}': {str(matrix_ex)}")
            events_failed += len(events)
            continue
         
         # update all ConnectTouchProcessPointEvent events for this TPE
         for event in events:
            try:
               # update the direction attributes
               event.SetString('ApprDirX', str(xDir))
               event.SetString('ApprDirZ', str(zDir))
               events_updated += 1
               
            except Exception as event_ex:
               logging.LogWarn(f"PrevProgramDownload.py: Failed to update event on TPE '{tpe.GetName()}': {str(event_ex)}")
               events_failed += 1
               continue
      
      except Exception as tpe_ex:
         logging.LogWarn(f"PrevProgramDownload.py: Error processing TPE: {str(tpe_ex)}")
         continue

   # log summary
   logging.LogDebug(f"PrevProgramDownload.py: Execution completed.")
   logging.LogDebug(f"  TPEs with ConnectTouchProcessPointEvent: {tpes_processed}")
   logging.LogDebug(f"  Events successfully updated: {events_updated}")
   if events_failed > 0:
      logging.LogDebug(f"  Events failed to update: {events_failed}")

   return
# --------------------------- End of ModifyActiveProgram -------------------------------------


# -------------------------------------------------------------------------------------------
# Multilayer planning (docs/ctrl-specific/KUKA/spec/multilayer.md sections 10.5 and 12).
# Runs before every download so the tree, simulation and generated program agree; the
# downloader must never reorder or reverse independently (section 10.4).
def ApplyMultilayerPlan(Operator: CENPyOlpProgramModifyOperator, program, logging):
   programGetter = program.GetAttribGetter()
   if programGetter is None:
      return

   passInputs = []
   for ordinal, operation in enumerate(program.GetOperations()):
      getter = operation.GetAttribGetter()
      if getter is None or not getter.GetBool(ml_meta.ATTR_USES_PROCESS_TABLE):
         continue
      setter = operation.GetAttribSetter()
      systemGetter = getter.GetSystemAttribGetter()
      if setter is not None and systemGetter is not None:
         effectiveGeometry = (
            (ml_meta.ATTR_WORK_ANGLE_OFFSET, getter.GetDouble("LocalOffsetRx")),
            (ml_meta.ATTR_ABSOLUTE_TRAVEL_ANGLE, getter.GetDouble("LocalOffsetRy")),
            (ml_meta.ATTR_NORMAL_OFFSET, systemGetter.GetSheetOffset().GetValue()),
            (ml_meta.ATTR_CONTOUR_START_OFFSET, systemGetter.GetStartPointValue().GetValue()),
            (ml_meta.ATTR_CONTOUR_OFFSET, systemGetter.GetOffsetY().GetValue()),
         )
         geometryChanged = False
         for mirrorName, nativeValue in effectiveGeometry:
            if abs(getter.GetDouble(mirrorName) - nativeValue) > 1e-9:
               geometryChanged = True
            setter.SetDouble(mirrorName, nativeValue)
         if geometryChanged:
            setter.SetEnumIndex(
               ml_meta.ATTR_RECIPE_STATE,
               ml_meta.RECIPE_STATE_LITERALS.index(ml_meta.RECIPE_STATE_DETACHED),
            )
      overrideAttrib = getter.GetAttributeEnumByName(ml_meta.ATTR_DIRECTION_OVERRIDE)
      overrideValue = overrideAttrib.GetValue() if overrideAttrib.IsValid() else ml_meta.DIRECTION_OVERRIDE_DEFAULT
      passInputs.append(planner.PassInput(
         seam_uuid=getter.GetString(ml_meta.ATTR_SEAM_UUID),
         wps_main_id=getter.GetInteger(ml_meta.ATTR_WPS_MAIN_ID),
         wps_sub_id=getter.GetInteger(ml_meta.ATTR_WPS_SUB_ID),
         wps_name=getter.GetString(ml_meta.ATTR_WPS_NAME),
         layer=getter.GetInteger(ml_meta.ATTR_LAYER_NUMBER),
         bead=getter.GetInteger(ml_meta.ATTR_BEAD_NUMBER),
         source_operation=operation,
         source_operation_ordinal=ordinal,
         recipe_fingerprint=getter.GetString(ml_meta.ATTR_RECIPE_FINGERPRINT),
         direction_override=planner.DirectionOverride(overrideValue),
      ))

   if not passInputs:
      return

   outputMode = _ReadEnum(programGetter, ml_meta.ATTR_OUTPUT_MODE, ml_meta.OUTPUT_MODE_DEFAULT)
   sequenceMode = planner.SequenceMode(_ReadEnum(programGetter, ml_meta.ATTR_SEQUENCE_MODE, ml_meta.SEQUENCE_MODE_DEFAULT))
   directionMode = planner.DirectionMode(_ReadEnum(programGetter, ml_meta.ATTR_DIRECTION_MODE, ml_meta.DIRECTION_MODE_DEFAULT))

   # Defensive fallback: LayerBeadAcrossSeams is not production-ready (planner section 10.4)
   # and MultiLayerSequenceMode is now read-only in the UI, but a program created before that
   # lock can still carry the old value - a UI lock never resets an already-set value.
   if sequenceMode == planner.SequenceMode.LAYER_BEAD_ACROSS_SEAMS:
      logging.LogWarn("PrevProgramDownload.py: MultiLayerSequenceMode=LayerBeadAcrossSeams is "
                       "not production-ready; forcing CompleteSeam for this download.")
      sequenceMode = planner.SequenceMode.COMPLETE_SEAM

   plan = planner.build_multilayer_plan(passInputs, outputMode, sequenceMode, directionMode)

   for multilayerPass in plan.execution:
      operation = multilayerPass.source_operation
      setter = operation.GetAttribSetter()
      if setter is None:
         continue
      setter.SetInteger(ml_meta.ATTR_FLAT_PASS_INDEX, multilayerPass.flat_index_in_seam)

      # Disambiguate operation names that follow the Seam_.../SeamN_... convention but do not
      # encode which seam they belong to. Re-derived every run so it self-corrects if seam
      # ordinals ever shift, rather than only firing once.
      currentName = operation.GetName()
      nameMatch = SEAM_NAME_PATTERN.match(currentName)
      if nameMatch:
         wantName = f"Seam{multilayerPass.seam_ordinal + 1}_{nameMatch.group(1)}"
         if currentName != wantName:
            operation.SetName(wantName)

      wantReverse = multilayerPass.direction == planner.Direction.REVERSE
      sysSetter = setter.GetSystemAttribSetter()
      if sysSetter is None:
         logging.LogWarn(f"PrevProgramDownload.py: GetSystemAttribSetter() returned None for seam "
                          f"{multilayerPass.seam_uuid!r} pass {multilayerPass.flat_index_in_seam} - "
                          f"Sys_Att_ProcessFlowDirection not set.")
         continue
      sysSetter.SetProcessFlowDirection(wantReverse)

      # Read back to confirm the write actually stuck - no working example of
      # SetProcessFlowDirection exists anywhere in this repo or the community submodule to
      # confirm the call against, so verify it directly instead of trusting it silently.
      getter = operation.GetAttribGetter()
      sysGetter = getter.GetSystemAttribGetter() if getter is not None else None
      gotReverse = sysGetter.GetProcessFlowDirection().GetState() if sysGetter is not None else None
      if gotReverse != wantReverse:
         logging.LogWarn(f"PrevProgramDownload.py: Sys_Att_ProcessFlowDirection did not stick for seam "
                          f"{multilayerPass.seam_uuid!r} pass {multilayerPass.flat_index_in_seam} - "
                          f"wanted {wantReverse}, read back {gotReverse!r}.")

   for diagnostic in plan.diagnostics:
      logging.LogWarn(f"PrevProgramDownload.py: [{diagnostic.code}] {diagnostic.message}")

   logging.LogDebug(f"PrevProgramDownload.py: Multilayer plan applied to {len(plan.execution)} pass(es) "
                    f"across {len(plan.seams)} seam(s), direction mode {directionMode.value}.")


def _ReadEnum(attribGetter, name, default):
   attrib = attribGetter.GetAttributeEnumByName(name)
   return attrib.GetValue() if attrib.IsValid() else default