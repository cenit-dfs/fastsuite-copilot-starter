# -------------------------------------------------------------------------------------------
# Name: StitchWeldingWorkMethod
# Description: this Python file adjust basic implementation for vendor specific installation 
# Debug info: E2@localhost:5254
# Author: Cenit AG
# Changelog:
#     Version: 1.0
#        Changed by: 
#        Date: 
#     
# -------------------------------------------------------------------------------------------
from centypes import *
from cenpylib import *
import sys, inspect, os
sys.dont_write_bytecode = True
sys.path.append(str(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
import MultiLayerDiagnostics as diag
import MultiLayerMetadata as ml_meta
import MultiLayerProcessTable as process_table
import MultiLayerRecipeState as recipe_state

# -------------------------------------------------------------------------------------------
# general global definitions. Enter here the technology name, followed by ": "
FILE_NAME = "StitchWeldingWorkMethod.py: "

# DEBUG
DEBUG_INIT_ATTRIBS_START = "(Debug) initialization of attributes started."
DEBUG_INIT_ATTRIBS_END = "(Debug) initialization of attributes ended."

DEBUG_INIT_EVENTS_START = "(Debug) initialization of events started."
DEBUG_INIT_EVENTS_END = "(Debug) initialization of events ended."

DEBUG_INIT_EVENT_RULES_START = "(Debug) initialization of event rules started."
DEBUG_INIT_EVENT_RULES_END = "(Debug) initialization of event rules ended."

DEBUG_INIT_MFGEO_START = "(Debug) initialization of manufacturing geometry started."
DEBUG_INIT_MFGEO_END = "(Debug) initialization of manufacturing geometry ended."

# ERROR
ERROR_CANNOT_CREATE_ATTRIB = "(Error) Could not create attributes."
ERROR_ATTRIB_SETTER_GETTER = "(Error) Could not get attribute setter or getter."
ERROR_GET_ATTRIB = "(Error) Could not get attribute."
ERROR_SET_ATTRIB = "(Error) Could not set attribute."

ST_KUKA_TRACKING_ON_DISTANCE = "KukaTrackingOnDistance"
ST_KUKA_TRACKING_SETID = "KukaTrackingSetId"
ST_KUKA_TRACKING_SEAM_PATTERN_NR = "KukaTrackingSeamPatternNr"
ST_KUKA_TRACKING_SEARCH_LENGTH = "KukaTrackingSearchLength"
ST_KUKA_TRACKING_CONT_AFTER_ERR = "KukaTrackingContAfterErr"
ST_KUKA_TRACKING_CONT_AFTER_ERR_LIST = ["Without offset","With offset"]
ST_KUKA_TRACKING_MAX_LIN_CORRECTION = "KukaTrackingMaxLinCorrection"
ST_KUKA_TRACKING_CORR_ELIM_DISTANCE = "KukaTrackingCorrElimDistance"
ST_KUKA_TRACKING_OFF_DISTANCE = "KukaTrackingOffDistance"
ST_KUKA_TRACKING_OFF_KEEPDISTANCE = "KukaTrackingOffKeepDistance"
ST_KUKA_SEARCH_START_SETID = "KukaSearchStartSetId"
ST_KUKA_SEARCH_START_TASK_NR = "KukaSearchStartTaskNr"
ST_KUKA_SEARCH_START_SEARCH_LENGTH = "KukaSearchStartSearchLength"
ST_KUKA_SEARCH_START_CORR_ELIM_DISTANCE = "KukaSearchStartCorrElimDistance"
ST_KUKA_SEARCH_START_MAX_CORRECTION = "KukaSearchStartMaxCorrection"
ST_KUKA_SEARCH_START_ERROR_REACTION = "KukaSearchStartErrorReaction"
ST_KUKA_SEARCH_START_TRACK_MODE = "KukaSearchStartTrackMode"
ST_KUKA_SEARCH_START_TRACK_MODE_LIST = ["Both", "Side", "Height"]
ST_KUKA_SEARCH_START_SIDE_OFFSET = "KukaSearchStartSideOffset"
ST_KUKA_SEARCH_START_HEIGHT_OFFSET = "KukaSearchStartHeightOffset"
ST_KUKA_SEARCH_START_PATH_OFFSET = "KukaSearchStartPathOffset"
ST_SEAMTRACKING_DISTANCE = "SeamTrackingDistance"

ATTRIBUTE_GLOBAL_LEVEL = USER_ATTRIBUTE | GLOBAL_ATTRIBUTE | PROCESS_ATTRIBUTE
ATTRIBUTE_LEVEL = USER_ATTRIBUTE | GLOBAL_ATTRIBUTE | OPERATION_GROUP_ATTRIBUTE | OPERATION_ATTRIBUTE | PROCESS_ATTRIBUTE
MAX_INTEGER = 2147483647

# Multilayer welding (docs/ctrl-specific/KUKA/spec/multilayer.md section 8.3): operation
# metadata plus the direction override control. Not global - each operation gets its own value.
MULTILAYER_OPERATION_LEVEL = USER_ATTRIBUTE | PROCESS_ATTRIBUTE | OPERATION_ATTRIBUTE


def _HasCadMatchAttributes(pgOperator):
   """True when the geometry carries all four attributes E2 uses for automatic WPS matching."""
   if pgOperator == None:
      return False
   try:
      for name in ml_meta.PG_CAD_MATCH_INTEGER_ATTRIBUTES:
         if not pgOperator.GetAttributeIntegerByName(name).IsValid():
            return False
      for name in ml_meta.PG_CAD_MATCH_STRING_ATTRIBUTES:
         if not pgOperator.GetAttributeStringByName(name).IsValid():
            return False
      for name in ml_meta.PG_CAD_MATCH_DOUBLE_ATTRIBUTES:
         if not pgOperator.GetAttributeDoubleByName(name).IsValid():
            return False
      return True
   except Exception:
      return False


# -------------------------------------------------------------------------------------------
# Work method post init attributes
def PostWmInitAttributes(Operator : CENPyOlpWM_AttribInitOperator):
   # get logger
   logging = Operator.GetLoggerOperator()
   # debug logging
   logging.LogDebug(FILE_NAME + DEBUG_INIT_ATTRIBS_START)

   # get creator, getter & setter
   attribCreator = Operator.GetAttribCreator()
   attribGetter = Operator.GetAttribGetter()
   attribSetter = Operator.GetAttribSetter()
   controller = Operator.GetController()
   # check none
   if (attribCreator == None) or (attribGetter == None) or (attribSetter == None) or (controller == None):
      return

   try:
      #Kuka-specific Seam Tracking attributes
      attribDouble = attribCreator.AddDouble(ST_KUKA_TRACKING_ON_DISTANCE,0.0,-0.1,0.1,0.001,ATTRIBUTE_LEVEL,ATTRIB_LENGTH,ST_KUKA_TRACKING_ON_DISTANCE)
      attribDouble.SetVisibility(False)
      attribString = attribCreator.AddString(ST_KUKA_TRACKING_SETID,'S1',ATTRIBUTE_LEVEL,ST_KUKA_TRACKING_SETID)
      attribInteger = attribCreator.AddInteger(ST_KUKA_TRACKING_SEAM_PATTERN_NR,2,1,255,ATTRIBUTE_LEVEL,ST_KUKA_TRACKING_SEAM_PATTERN_NR)
      attribDouble = attribCreator.AddDouble(ST_KUKA_TRACKING_SEARCH_LENGTH,0.150,0.005,0.150,0.001,ATTRIBUTE_LEVEL,ATTRIB_LENGTH,ST_KUKA_TRACKING_SEARCH_LENGTH)
      attribIntENM = attribCreator.AddEnum(ST_KUKA_TRACKING_CONT_AFTER_ERR,ST_KUKA_TRACKING_CONT_AFTER_ERR_LIST,ST_KUKA_TRACKING_CONT_AFTER_ERR_LIST[0],ATTRIBUTE_GLOBAL_LEVEL,ST_KUKA_TRACKING_CONT_AFTER_ERR)
      attribDouble = attribCreator.AddDouble(ST_KUKA_TRACKING_MAX_LIN_CORRECTION,0.050,0.0,0.05,0.001,ATTRIBUTE_LEVEL,ATTRIB_LENGTH,ST_KUKA_TRACKING_MAX_LIN_CORRECTION)
      attribDouble = attribCreator.AddDouble(ST_KUKA_TRACKING_CORR_ELIM_DISTANCE,0.200,0.005,0.2,0.001,ATTRIBUTE_LEVEL,ATTRIB_LENGTH,ST_KUKA_TRACKING_CORR_ELIM_DISTANCE)
      attribDouble = attribCreator.AddDouble(ST_KUKA_TRACKING_OFF_DISTANCE,0.0,-0.1,0.1,0.001,ATTRIBUTE_LEVEL,ATTRIB_LENGTH,ST_KUKA_TRACKING_OFF_DISTANCE)
      attribDouble.SetVisibility(False)
      attribBool   = attribCreator.AddBool(ST_KUKA_TRACKING_OFF_KEEPDISTANCE,True,ATTRIBUTE_LEVEL,ST_KUKA_TRACKING_OFF_KEEPDISTANCE)
      attribCreator.AddString(ST_KUKA_SEARCH_START_SETID,'S4',ATTRIBUTE_LEVEL,ST_KUKA_SEARCH_START_SETID)
      attribCreator.AddInteger(ST_KUKA_SEARCH_START_TASK_NR,1,1,255,ATTRIBUTE_LEVEL,ST_KUKA_SEARCH_START_TASK_NR)
      attribCreator.AddDouble(ST_KUKA_SEARCH_START_SEARCH_LENGTH,0.100,0.005,0.150,0.001,ATTRIBUTE_LEVEL,ATTRIB_LENGTH,ST_KUKA_SEARCH_START_SEARCH_LENGTH)
      attribCreator.AddDouble(ST_KUKA_SEARCH_START_CORR_ELIM_DISTANCE,0.020,0.005,0.2,0.001,ATTRIBUTE_LEVEL,ATTRIB_LENGTH,ST_KUKA_SEARCH_START_CORR_ELIM_DISTANCE)
      attribCreator.AddDouble(ST_KUKA_SEARCH_START_MAX_CORRECTION,0.025,0.0,0.05,0.001,ATTRIBUTE_LEVEL,ATTRIB_LENGTH,ST_KUKA_SEARCH_START_MAX_CORRECTION)
      attribCreator.AddEnum(ST_KUKA_SEARCH_START_ERROR_REACTION,ST_KUKA_TRACKING_CONT_AFTER_ERR_LIST,ST_KUKA_TRACKING_CONT_AFTER_ERR_LIST[0],ATTRIBUTE_LEVEL,ST_KUKA_SEARCH_START_ERROR_REACTION)
      attribCreator.AddEnum(ST_KUKA_SEARCH_START_TRACK_MODE,ST_KUKA_SEARCH_START_TRACK_MODE_LIST,ST_KUKA_SEARCH_START_TRACK_MODE_LIST[0],ATTRIBUTE_LEVEL,ST_KUKA_SEARCH_START_TRACK_MODE)
      attribCreator.AddDouble(ST_KUKA_SEARCH_START_SIDE_OFFSET,0.0,-0.1,0.1,0.001,ATTRIBUTE_LEVEL,ATTRIB_LENGTH,ST_KUKA_SEARCH_START_SIDE_OFFSET)
      attribCreator.AddDouble(ST_KUKA_SEARCH_START_HEIGHT_OFFSET,0.0,-0.1,0.1,0.001,ATTRIBUTE_LEVEL,ATTRIB_LENGTH,ST_KUKA_SEARCH_START_HEIGHT_OFFSET)
      attribCreator.AddDouble(ST_KUKA_SEARCH_START_PATH_OFFSET,0.0,-0.1,0.1,0.001,ATTRIBUTE_LEVEL,ATTRIB_LENGTH,ST_KUKA_SEARCH_START_PATH_OFFSET)
   except:
      logging.LogError("Cannot initialize vendor specific touch sensing work method attributes")

   seamTrackingDistance = attribGetter.GetAttributeByName(ST_SEAMTRACKING_DISTANCE)
   seamTrackingDistance.SetOlpProperty(GLOBAL_ATTRIBUTE | USER_ATTRIBUTE | OPERATION_ATTRIBUTE | OPERATION_GROUP_ATTRIBUTE | PROCESS_ATTRIBUTE)

   # Multilayer welding - user-facing direction override (spec section 8.2, container
   # MultiLayerConfiguration/MultiLayerPlanning; visibility owned by
   # ArcWeldingTechnology.PostTechOnAttribChanged, not here).
   attribIntENM = attribCreator.AddEnum(ml_meta.ATTR_DIRECTION_OVERRIDE, ml_meta.DIRECTION_OVERRIDE_LITERALS, ml_meta.DIRECTION_OVERRIDE_DEFAULT, MULTILAYER_OPERATION_LEVEL, ml_meta.ATTR_DIRECTION_OVERRIDE)
   attribIntENM.SetVisibility(False)

   # Multilayer welding - stable read-only operation metadata (spec section 8.3). Written
   # only by PostWmSyncPgAttributes below; never surfaced in a TechTab container, so they
   # start hidden. Read-only to users; downloaders/future sequencing scripts consume them.
   attribInteger = attribCreator.AddInteger(ml_meta.ATTR_METADATA_VERSION, ml_meta.SCHEMA_VERSION, 0, MAX_INTEGER, MULTILAYER_OPERATION_LEVEL, ml_meta.ATTR_METADATA_VERSION)
   attribInteger.SetReadOnly(True)
   attribInteger.SetVisibility(False)
   attribBool = attribCreator.AddBool(ml_meta.ATTR_USES_PROCESS_TABLE, False, MULTILAYER_OPERATION_LEVEL, ml_meta.ATTR_USES_PROCESS_TABLE)
   attribBool.SetReadOnly(True)
   attribBool.SetVisibility(False)
   attribInteger = attribCreator.AddInteger(ml_meta.ATTR_WPS_MAIN_ID, -1, -1, MAX_INTEGER, MULTILAYER_OPERATION_LEVEL, ml_meta.ATTR_WPS_MAIN_ID)
   attribInteger.SetReadOnly(True)
   attribInteger.SetVisibility(False)
   attribInteger = attribCreator.AddInteger(ml_meta.ATTR_WPS_SUB_ID, -1, -1, MAX_INTEGER, MULTILAYER_OPERATION_LEVEL, ml_meta.ATTR_WPS_SUB_ID)
   attribInteger.SetReadOnly(True)
   attribInteger.SetVisibility(False)
   attribString = attribCreator.AddString(ml_meta.ATTR_WPS_NAME, "", MULTILAYER_OPERATION_LEVEL, ml_meta.ATTR_WPS_NAME)
   attribString.SetReadOnly(True)
   attribString.SetVisibility(False)
   attribInteger = attribCreator.AddInteger(ml_meta.ATTR_LAYER_NUMBER, -1, -1, MAX_INTEGER, MULTILAYER_OPERATION_LEVEL, ml_meta.ATTR_LAYER_NUMBER)
   attribInteger.SetReadOnly(True)
   attribInteger.SetVisibility(False)
   attribInteger = attribCreator.AddInteger(ml_meta.ATTR_BEAD_NUMBER, -1, -1, MAX_INTEGER, MULTILAYER_OPERATION_LEVEL, ml_meta.ATTR_BEAD_NUMBER)
   attribInteger.SetReadOnly(True)
   attribInteger.SetVisibility(False)
   attribInteger = attribCreator.AddInteger(ml_meta.ATTR_FLAT_PASS_INDEX, -1, -1, MAX_INTEGER, MULTILAYER_OPERATION_LEVEL, ml_meta.ATTR_FLAT_PASS_INDEX)
   attribInteger.SetReadOnly(True)
   attribInteger.SetVisibility(False)
   attribString = attribCreator.AddString(ml_meta.ATTR_SEAM_UUID, "", MULTILAYER_OPERATION_LEVEL, ml_meta.ATTR_SEAM_UUID)
   attribString.SetReadOnly(True)
   attribString.SetVisibility(False)
   attribString = attribCreator.AddString(ml_meta.ATTR_RECIPE_FINGERPRINT, "", MULTILAYER_OPERATION_LEVEL, ml_meta.ATTR_RECIPE_FINGERPRINT)
   attribString.SetReadOnly(True)
   attribString.SetVisibility(False)
   attribIntENM = attribCreator.AddEnum(ml_meta.ATTR_RECIPE_STATE, ml_meta.RECIPE_STATE_LITERALS, ml_meta.RECIPE_STATE_NOT_APPLICABLE, MULTILAYER_OPERATION_LEVEL, ml_meta.ATTR_RECIPE_STATE)
   attribIntENM.SetReadOnly(True)
   attribIntENM.SetVisibility(False)
   for geometryAttribute in (
      ml_meta.ATTR_WORK_ANGLE_OFFSET,
      ml_meta.ATTR_ABSOLUTE_TRAVEL_ANGLE,
      ml_meta.ATTR_NORMAL_OFFSET,
      ml_meta.ATTR_CONTOUR_START_OFFSET,
      ml_meta.ATTR_CONTOUR_OFFSET,
   ):
      attribDouble = attribCreator.AddDouble(geometryAttribute, 0.0, -1000000.0, 1000000.0, 0.001, MULTILAYER_OPERATION_LEVEL, ATTRIB_STANDARD, geometryAttribute)
      attribDouble.SetReadOnly(True)
      attribDouble.SetVisibility(False)

   # debug logging
   logging.LogDebug(FILE_NAME + DEBUG_INIT_ATTRIBS_END)

def PostWmInitEvents(WmEventInitOperator: CENPyOlpWM_EventInitOperator):
   WmEventInitOperator.RegisterPyTechnologyEvent('SeamTrackOnEvent.py')
   WmEventInitOperator.RegisterPyTechnologyEvent('SeamTrackOffEvent.py')
   WmEventInitOperator.RegisterPyTechnologyEvent('SeamTrackingSearchStart.py')
   WmEventInitOperator.RegisterPyTechnologyEvent('SeamTrackingLeadInEvent.py')

   # WmEventInitOperator.RegisterPyTechnologyEvent('ArcSpotEvent.py')
   # WmEventInitOperator.RegisterPyTechnologyEvent(PY_SEAMFIND_TEACH_EVENT_FILE)
   # add Python Approach&Retract Event to WM
   # WmEventInitOperator.RegisterPyTechnologyEvent(PY_SEAMFIND_SCAN_EVENT_FILE)
   # WmEventInitOperator.RegisterPyTechnologyEvent(PY_SEAMFIND_REF_EVENT_FILE)
   # WmEventInitOperator.RegisterPyTechnologyEvent(PY_LINELASERPOV_EVENT_FILE)
   pass

def PostWmInitRules(WmRuleInitOperator: CENPyOlpWM_RuleInitOperator):
   # get logger
   logging = WmRuleInitOperator.GetLoggerOperator()
   # Remove C++ APPROACH Event from Rule

# -------------------------------------------------------------------------------------------
# Work method post sync process geometry attributes
def PostWmSyncPgAttributes(Operator: CENPyOlpWM_SyncPgAttribOperator):
   # get logger
   logging = Operator.GetLoggerOperator()

   # get getter & setter
   attribGetter = Operator.GetAttribGetter()
   attribSetter = Operator.GetAttribSetter()
   controller = Operator.GetController()
   if (attribGetter == None) or (attribSetter == None) or (controller == None):
      return

   # Multilayer welding resolver (spec section 7.4). Matches process-table rows by the
   # selected WPS name + data-valid, treating a WPS with more than one pass as Multilayer
   # (index 36 is not a usable flag - see the section 7.2 correction), then persists stable
   # main/sub/layer/bead identity. Never re-consults _isUsed once identity has been
   # persisted for this WPS name (section 7.3).
   # Persisting here is mandatory, not a convenience: WPSAutomaticNames is scoped
   # User|Global with no Process flag, so it is unreadable from the download APIs. Only the
   # section-8.3 operation attributes (User|Process|Operation) survive to download time.
   pgOperator = Operator.GetCurrentProcessGeometryOperator()
   seamUuid = pgOperator.GetProcessGeometryIdentifier() if pgOperator != None else ""

   def resetToNotMultilayer():
      attribSetter.SetBool(ml_meta.ATTR_USES_PROCESS_TABLE, False)
      attribSetter.SetInteger(ml_meta.ATTR_METADATA_VERSION, ml_meta.SCHEMA_VERSION)
      attribSetter.SetEnumIndex(ml_meta.ATTR_RECIPE_STATE, ml_meta.RECIPE_STATE_LITERALS.index(ml_meta.RECIPE_STATE_NOT_APPLICABLE))
      setDirectionOverrideVisible(False)

   # MultiLayerDirectionOverride is operation-scope, so the technology-level recompute in
   # ArcWeldingTechnology cannot see it; own its visibility here (spec section 8.4).
   def setDirectionOverrideVisible(visible):
      overrideAttrib = attribGetter.GetAttributeByName(ml_meta.ATTR_DIRECTION_OVERRIDE)
      if overrideAttrib.IsValid():
         overrideAttrib.SetVisibility(visible)

   def syncEffectiveGeometry():
      systemGetter = attribGetter.GetSystemAttribGetter()
      if systemGetter is None:
         return
      geometryAttributes = (
         (ml_meta.ATTR_WORK_ANGLE_OFFSET, attribGetter.GetDouble("LocalOffsetRx")),
         (ml_meta.ATTR_ABSOLUTE_TRAVEL_ANGLE, attribGetter.GetDouble("LocalOffsetRy")),
         (ml_meta.ATTR_NORMAL_OFFSET, systemGetter.GetSheetOffset().GetValue()),
         (ml_meta.ATTR_CONTOUR_START_OFFSET, systemGetter.GetStartPointValue().GetValue()),
         (ml_meta.ATTR_CONTOUR_OFFSET, systemGetter.GetOffsetY().GetValue()),
      )
      changed = False
      for mirrorName, nativeValue in geometryAttributes:
         if abs(attribGetter.GetDouble(mirrorName) - nativeValue) > 1e-9:
            changed = True
         attribSetter.SetDouble(mirrorName, nativeValue)
      if changed:
         attribSetter.SetEnumIndex(
            ml_meta.ATTR_RECIPE_STATE,
            ml_meta.RECIPE_STATE_LITERALS.index(ml_meta.RECIPE_STATE_DETACHED),
         )

   # ML001/ML002 describe the two normal contexts in the spec section 8.4 matrix
   # (non-process-table welding, single-layer WPS), so at sync time they are routine
   # classification results and must stay at debug level. Only a WPS that really is
   # Multilayer but cannot be resolved (ML003/ML004) warrants a warning here; the
   # user-visible ML001/ML002 warning belongs to download, where Multilayer output was
   # actually requested and has to fall back to native.
   def logDiagnostic(code, message=None, severe=True):
      d = diag.make_diagnostic(code, message=message, seam_uuid=(seamUuid or None))
      text = FILE_NAME + "[" + d.code + "] " + d.message
      if severe:
         logging.LogWarn(text)
      else:
         logging.LogDebug(text)

   # Both WPS attributes are program-level (User|Global). WPSAutomatic selects how a dataset is
   # chosen: false means the user picked one by name in WPSAutomaticNames; true means E2 matches
   # a dataset against CAD-imported process attributes on the geometry. Only the named path is
   # implemented, so the automatic path must warn (ML018) rather than silently degrade - but only
   # when the geometry actually carries the match attributes, otherwise this is ordinary welding.
   # WPSAutomaticNames is not a usable gate on its own: it keeps a stale value in programs that
   # never used the process table.
   wpsAutomaticAttrib = attribGetter.GetAttributeBoolByName(ml_meta.ATTR_WPS_AUTOMATIC)
   if (not wpsAutomaticAttrib.IsValid()) or wpsAutomaticAttrib.GetState():
      resetToNotMultilayer()
      if _HasCadMatchAttributes(pgOperator):
         logDiagnostic("ML018", message="Geometry carries CAD match attributes but automatic WPS matching is not implemented")
      else:
         logDiagnostic("ML001", severe=False)
      return

   wpsNameAttrib = attribGetter.GetAttributeEnumByName(ml_meta.ATTR_WPS_AUTOMATIC_NAMES)
   wpsName = wpsNameAttrib.GetValue() if wpsNameAttrib.IsValid() else ""
   if not wpsName:
      resetToNotMultilayer()
      logDiagnostic("ML001", severe=False)
      return

   # Already resolved for this exact WPS name: stable identity was persisted on a previous
   # sync, so do not re-run first-unused selection (it is a creation-time cursor only).
   alreadyResolved = attribGetter.GetBool(ml_meta.ATTR_USES_PROCESS_TABLE)
   currentName = attribGetter.GetString(ml_meta.ATTR_WPS_NAME)
   if alreadyResolved and currentName == wpsName:
      syncEffectiveGeometry()
      setDirectionOverrideVisible(True)
      return

   try:
      rawRows = controller.GetWeldingDataSetsFromDataBase()
   except Exception:
      logging.LogError(FILE_NAME + "Could not read welding data sets from database.")
      resetToNotMultilayer()
      return

   candidates = process_table.find_candidate_rows(rawRows, wpsName)
   if not candidates:
      resetToNotMultilayer()
      logDiagnostic("ML002", message="WPS '" + wpsName + "' has no valid Multilayer row", severe=False)
      return

   ambiguousMainIds = process_table.find_ambiguous_main_ids(rawRows, wpsName)
   if len(ambiguousMainIds) > 1:
      logDiagnostic("ML004", message="Duplicate WPS name/main-ID ambiguity: '" + wpsName + "' -> main IDs " + str(sorted(ambiguousMainIds)))

   selection = process_table.select_first_unused(rawRows, wpsName)
   if selection == None:
      resetToNotMultilayer()
      logDiagnostic("ML003", message="No unused Multilayer row left for WPS '" + wpsName + "'")
      return

   _, record = selection

   attribSetter.SetBool(ml_meta.ATTR_USES_PROCESS_TABLE, True)
   attribSetter.SetInteger(ml_meta.ATTR_METADATA_VERSION, ml_meta.SCHEMA_VERSION)
   attribSetter.SetInteger(ml_meta.ATTR_WPS_MAIN_ID, record.main_id)
   attribSetter.SetInteger(ml_meta.ATTR_WPS_SUB_ID, record.sub_id)
   attribSetter.SetString(ml_meta.ATTR_WPS_NAME, record.name)
   attribSetter.SetInteger(ml_meta.ATTR_LAYER_NUMBER, record.layer)
   attribSetter.SetInteger(ml_meta.ATTR_BEAD_NUMBER, record.bead)
   attribSetter.SetString(ml_meta.ATTR_SEAM_UUID, seamUuid or "")
   attribSetter.SetDouble(ml_meta.ATTR_WORK_ANGLE_OFFSET, record.geometry.work_angle_offset)
   attribSetter.SetDouble(ml_meta.ATTR_ABSOLUTE_TRAVEL_ANGLE, record.geometry.absolute_travel_angle)
   attribSetter.SetDouble(ml_meta.ATTR_NORMAL_OFFSET, record.geometry.normal_offset)
   attribSetter.SetDouble(ml_meta.ATTR_CONTOUR_START_OFFSET, record.geometry.contour_start_offset)
   attribSetter.SetDouble(ml_meta.ATTR_CONTOUR_OFFSET, record.geometry.contour_offset)

   # MultiLayerFlatPassIndex stays -1 here: it requires the full seam view built by
   # MultiLayerPlanner.build_multilayer_plan, not available from a single operation sync.
   fingerprint = recipe_state.compute_recipe_fingerprint([record])
   attribSetter.SetString(ml_meta.ATTR_RECIPE_FINGERPRINT, fingerprint)
   attribSetter.SetEnumIndex(ml_meta.ATTR_RECIPE_STATE, ml_meta.RECIPE_STATE_LITERALS.index(ml_meta.RECIPE_STATE_CURRENT_SNAPSHOT))
   setDirectionOverrideVisible(True)

   logging.LogDebug(FILE_NAME + "Multilayer WPS '" + wpsName + "' resolved: main=" + str(record.main_id) +
                    " sub=" + str(record.sub_id) + " layer=" + str(record.layer) + " bead=" + str(record.bead))

# -------------------------------------------------------------------------------------------
def PostWmOnAttribChanged(Operator: CENPyOlpWM_AttribChangedOperator):
   # get logger
   logging = Operator.GetLoggerOperator()   
