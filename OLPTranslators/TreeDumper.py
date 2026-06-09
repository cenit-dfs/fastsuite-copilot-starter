"""
TreeDumper — YAML OLP Tree Inspector for FASTSUITE E2

Outputs a complete YAML dump of the OLP object tree including all controller
metadata, profiles, resources (with ports), programs, operation groups,
operations, motions, events, and attributes at every level.

Use this translator to generate machine-parseable reference baselines for:
- Downloader development (see what data E2 provides)
- Technology analysis (compare attribute/event sets across vendors)
- Agent-assisted coding (structured input for code generation)

Output: one .yaml file per program in the controller output directory.
"""

import sys, inspect, os
sys.dont_write_bytecode = True
sys.path.append(str(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

from enum import Enum
from cenpylib import FileUtility
from cenpydownload import Downloader
from cenpydownload import DULPythonDownloadOperator
from cenpydownload import DULPythonController
from cenpydownload import DULPythonProgram
from cenpydownload import DULPythonSubprogram
from cenpydownload import DULPythonOperationGroup
from cenpydownload import DULPythonOperation
from cenpydownload import DULPythonEvent
from cenpydownload import DULPythonMotion
from cenpydownload import DULPythonPosition
from cenpydownload import DULPythonJoint
from cenpydownload import DULPythonToolProfile
from cenpydownload import DULPythonBaseProfile
from cenpydownload import DULPythonAccuracyProfile
from cenpydownload import DULPythonMotionProfile
from cenpyolpcore import OlpCorePythonTechnology
from cenpyolpcore import OlpCorePythonResource
from cenpyolpcore import OlpCorePythonBoolAttribute
from cenpyolpcore import OlpCorePythonIntegerAttribute
from cenpyolpcore import OlpCorePythonIntegerArrayAttribute
from cenpyolpcore import OlpCorePythonDoubleAttribute
from cenpyolpcore import OlpCorePythonDoubleArrayAttribute
from cenpyolpcore import OlpCorePythonStringAttribute
from cenpyolpcore import OlpCorePythonStringArrayAttribute
from cenpyolpcore import OlpCorePythonLiteralAttribute
from cenpyolpcore import OlpCorePythonAttribute
from cenpyolpcore import AttributeProperties

DOWNLOAD_CLASS_NAME = "TreeDumper"
TRANSLATOR_VERSION = "1.0"


# =============================================================================
# YAML Emitter — manual string builder (no pyyaml dependency)
# =============================================================================

class YamlEmitter:
   """Builds valid YAML by tracking indentation and emitting typed values."""

   INDENT = "  "  # 2-space indent per level

   def __init__(self):
      self._lines: list[str] = []

   def comment(self, text: str, depth: int = 0):
      self._lines.append(f"{self.INDENT * depth}# {text}")

   def blank(self):
      self._lines.append("")

   def key_value(self, key: str, value, depth: int = 0):
      self._lines.append(f"{self.INDENT * depth}{key}: {self._format_scalar(value)}")

   def key_only(self, key: str, depth: int = 0):
      self._lines.append(f"{self.INDENT * depth}{key}:")

   def list_item_scalar(self, value, depth: int = 0):
      self._lines.append(f"{self.INDENT * depth}- {self._format_scalar(value)}")

   def list_item_mapping_start(self, first_key: str, first_value, depth: int = 0):
      self._lines.append(f"{self.INDENT * depth}- {first_key}: {self._format_scalar(first_value)}")

   def inline_list(self, key: str, values: list, depth: int = 0):
      formatted = ", ".join(self._format_scalar(v) for v in values)
      self._lines.append(f"{self.INDENT * depth}{key}: [{formatted}]")

   def inline_dict(self, key: str, pairs: dict, depth: int = 0):
      formatted = ", ".join(f"{k}: {self._format_scalar(v)}" for k, v in pairs.items())
      self._lines.append(f"{self.INDENT * depth}{key}: {{{formatted}}}")

   def raw(self, text: str):
      self._lines.append(text)

   def get_text(self) -> str:
      return "\n".join(self._lines) + "\n"

   @staticmethod
   def _format_scalar(value) -> str:
      if value is None:
         return "~"
      if isinstance(value, bool):
         return "true" if value else "false"
      if isinstance(value, int):
         return str(value)
      if isinstance(value, float):
         return f"{value:.6f}"
      if isinstance(value, str):
         if value == "":
            return '""'
         # Quote strings that could be misinterpreted
         if value in ("true", "false", "null", "~", "yes", "no", "on", "off"):
            return f'"{value}"'
         if any(c in value for c in (':', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`', '"', "'")):
            return f'"{value}"'
         try:
            float(value)
            return f'"{value}"'
         except (ValueError, TypeError):
            pass
         return f'"{value}"'
      # Enum-like objects
      if isinstance(value, Enum):
         return f'"{value.name}"'
      if hasattr(value, "name"):
         return f'"{value.name}"'
      return f'"{str(value)}"'


# =============================================================================
# Attribute property flag decoder
# =============================================================================

ATTR_PROPERTY_FLAGS = {
   int(AttributeProperties.UserAttribute): "UserAttribute",
   int(AttributeProperties.ProcessAttribute): "ProcessAttribute",
   int(AttributeProperties.OperationAttribute): "OperationAttribute",
   int(AttributeProperties.OperationGroupAttribute): "OperationGroupAttribute",
   int(AttributeProperties.GlobalAttribute): "GlobalAttribute",
   int(AttributeProperties.ReadOnlyAttribute): "ReadOnlyAttribute",
   int(AttributeProperties.ControllerAttribute): "ControllerAttribute",
}

def decode_olp_property(prop) -> list[str]:
   bits = int(prop)
   flags = []
   for bit_val, name in ATTR_PROPERTY_FLAGS.items():
      if bits & bit_val:
         flags.append(name)
   return flags


# =============================================================================
# Safe enum/value extraction
# =============================================================================

MAX_UINT32 = 2**32 - 1

def safe_enum_name(value) -> str:
   if isinstance(value, Enum):
      return value.name
   if hasattr(value, "name"):
      return value.name
   return str(value)

def safe_index(value) -> object:
   """Convert notDefined (max uint32) index to None."""
   if value == MAX_UINT32:
      return None
   return value


# =============================================================================
# TreeDumper Downloader
# =============================================================================

class TreeDumper(Downloader):

   def __init__(self) -> None:
      super().__init__()
      self._fileUtil = FileUtility()
      self._outputFilePath = ""
      self._outputDir = ""
      self._yaml = YamlEmitter()
      # Counters for summary
      self._programCount = 0
      self._groupCount = 0
      self._operationCount = 0
      self._motionCount = 0
      self._eventCount = 0
      self._eventTypes: set = set()
      self._technologies: set = set()
      self._attrCounts = {"controller": 0, "program": 0, "group": 0,
                          "operation": 0, "event": 0, "motion": 0,
                          "position": 0, "resource": 0}
      self._hasSubprograms = False
      self._hasOperationGroups = False

   # ---- Lifecycle ----

   def Initialize(self, operator: DULPythonDownloadOperator):
      controller = operator.GetController()
      self._outputDir = controller.GetOutputDirectory()

   def CreateOutputFile(self, operator: DULPythonDownloadOperator):
      pass

   def OutputHeader(self, operator: DULPythonDownloadOperator, controller: DULPythonController):
      # Reset all state at the start of each program file
      self._yaml = YamlEmitter()
      self._programCount = 0
      self._groupCount = 0
      self._operationCount = 0
      self._motionCount = 0
      self._eventCount = 0
      self._eventTypes = set()
      self._technologies = set()
      self._attrCounts = {"controller": 0, "program": 0, "group": 0,
                          "operation": 0, "event": 0, "motion": 0,
                          "position": 0, "resource": 0}
      self._hasSubprograms = False
      self._hasOperationGroups = False

      y = self._yaml

      # Meta
      y.key_only("meta")
      y.key_value("translator", "TreeDumper", 1)
      y.key_value("translator_version", TRANSLATOR_VERSION, 1)
      y.key_value("language", operator.GetCurrentLanguage(), 1)
      y.blank()

      # Controller
      y.key_only("controller")
      y.key_value("name", controller.GetName(), 1)
      y.key_value("model", controller.GetModel(), 1)
      y.key_value("series", controller.GetSeries(), 1)
      y.key_value("manufacturer", controller.GetManufacturer(), 1)
      y.key_value("type", safe_enum_name(controller.GetControllerType()), 1)
      activeProgram = controller.GetActiveProgram()
      y.key_value("active_program", activeProgram.GetName() if activeProgram else None, 1)
      y.blank()

      # Joints
      y.key_only("joints", 1)
      for joint in controller.GetConnectedJoints():
         self._emit_joint(y, joint, 2)
      y.blank()

      # Tool profiles
      y.key_only("tool_profiles", 1)
      for tp in controller.GetToolProfiles():
         self._emit_tool_profile(y, tp, 2)
      y.blank()

      # Base profiles
      y.key_only("base_profiles", 1)
      for bp in controller.GetBaseProfiles():
         self._emit_base_profile(y, bp, 2)
      y.blank()

      # Accuracy profiles
      y.key_only("accuracy_profiles", 1)
      for ap in controller.GetAccuracyProfiles():
         self._emit_accuracy_profile(y, ap, 2)
      y.blank()

      # Motion profiles (deduplicated by name)
      y.key_only("motion_profiles", 1)
      seen_profiles = set()
      for mp in controller.GetMotionProfiles():
         profile_key = mp.GetName()
         if profile_key not in seen_profiles:
            seen_profiles.add(profile_key)
            self._emit_motion_profile(y, mp, 2)
      y.blank()

      # Controller attributes
      y.key_only("attributes", 1)
      attrs = controller.GetAttributes()
      self._attrCounts["controller"] += len(attrs)
      for attr in attrs:
         self._emit_attribute(y, attr, 2)
      y.blank()

      # Resources
      y.key_only("resources", 1)
      for res in controller.GetResources():
         self._emit_resource(y, res, 2)
      y.blank()

   # ---- Program ----

   def ProgramStart(self, operator: DULPythonDownloadOperator, program: DULPythonProgram):
      y = self._yaml
      self._programCount += 1
      # Set output path from the actual program being processed
      self._outputFilePath = self._outputDir + "\\" + program.GetName() + ".yaml"

      if self._programCount == 1:
         y.key_only("programs")

      y.list_item_mapping_start("name", program.GetName(), 1)
      y.key_value("is_main", program.IsMainProgram(), 2)

      bp = program.GetUsedBaseProfile()
      if bp:
         y.key_value("base_profile", bp.GetName(), 2)
      else:
         y.key_value("base_profile", None, 2)

      tp = program.GetUsedToolProfile()
      if tp:
         y.key_value("tool_profile", tp.GetName(), 2)
      else:
         y.key_value("tool_profile", None, 2)

      y.key_only("attributes", 2)
      attrs = program.GetAttributes()
      self._attrCounts["program"] += len(attrs)
      for attr in attrs:
         self._emit_attribute(y, attr, 3)

      self._hasSubprograms = False
      self._hasOperationGroups = False

   def ProgramEnd(self, operator: DULPythonDownloadOperator, program: DULPythonProgram):
      pass

   # ---- Subprogram ----

   def SubprogramStart(self, operator: DULPythonDownloadOperator, subprogram: DULPythonSubprogram):
      y = self._yaml
      if not self._hasSubprograms:
         y.key_only("subprograms", 2)
         self._hasSubprograms = True
      y.list_item_mapping_start("name", subprogram.GetName(), 3)
      try:
         calling = subprogram.GetCallingProgram()
         y.key_value("calling_program", calling.GetName() if calling else None, 4)
      except Exception:
         y.key_value("calling_program", None, 4)
      try:
         called = subprogram.GetCalledProgram()
         y.key_value("called_program", called.GetName() if called else None, 4)
      except Exception:
         y.key_value("called_program", None, 4)

   def SubprogramEnd(self, operator: DULPythonDownloadOperator, subprogram: DULPythonSubprogram):
      pass

   # ---- Operation Group ----

   def OperationGroupStart(self, operator: DULPythonDownloadOperator, operationGroup: DULPythonOperationGroup):
      y = self._yaml
      self._groupCount += 1

      if not self._hasOperationGroups:
         y.key_only("operation_groups", 2)
         self._hasOperationGroups = True

      y.list_item_mapping_start("name", operationGroup.GetName(), 3)

      tech = operationGroup.GetTechnology()
      if tech:
         self._emit_technology(y, tech, 4)
         self._technologies.add(tech.GetName())
      else:
         y.key_value("technology", None, 4)

      bp = operationGroup.GetUsedBaseProfile()
      y.key_value("base_profile", bp.GetName() if bp else None, 4)

      tp = operationGroup.GetUsedToolProfile()
      y.key_value("tool_profile", tp.GetName() if tp else None, 4)

      y.key_only("attributes", 4)
      attrs = operationGroup.GetAttributes()
      self._attrCounts["group"] += len(attrs)
      for attr in attrs:
         self._emit_attribute(y, attr, 5)

      y.key_only("operations", 4)

   def OperationGroupEnd(self, operator: DULPythonDownloadOperator, operationGroup: DULPythonOperationGroup):
      pass

   # ---- Operation ----

   def OperationStart(self, operator: DULPythonDownloadOperator, operation: DULPythonOperation):
      y = self._yaml
      self._operationCount += 1

      y.list_item_mapping_start("name", operation.GetName(), 5)
      y.key_value("type", safe_enum_name(operation.GetOperationType()), 6)

      bp = operation.GetUsedBaseProfile()
      y.key_value("base_profile", bp.GetName() if bp else None, 6)

      tp = operation.GetUsedToolProfile()
      y.key_value("tool_profile", tp.GetName() if tp else None, 6)

      y.key_only("attributes", 6)
      attrs = operation.GetAttributes()
      self._attrCounts["operation"] += len(attrs)
      for attr in attrs:
         self._emit_attribute(y, attr, 7)

      y.key_only("motions", 6)

   def OperationEnd(self, operator: DULPythonDownloadOperator, operation: DULPythonOperation):
      pass

   # ---- Motion ----

   def HandleMotion(self, operator: DULPythonDownloadOperator, motion: DULPythonMotion):
      y = self._yaml
      self._motionCount += 1

      y.list_item_mapping_start("name", motion.GetName(), 7)
      y.key_value("motion_type", safe_enum_name(motion.GetMotionType()), 8)
      y.key_value("is_ptp", motion.IsPtPMotion(), 8)
      y.key_value("is_linear", motion.IsLinearMotion(), 8)
      y.key_value("is_circular", motion.IsCircularMotion(), 8)
      y.key_value("is_reference", motion.IsReferenceMotion(), 8)

      # Motion attributes
      y.key_only("attributes", 8)
      try:
         motionAttrs = motion.GetAttributes()
         self._attrCounts["motion"] += len(motionAttrs)
         for attr in motionAttrs:
            self._emit_attribute(y, attr, 9)
      except Exception:
         pass  # Some motions may not support GetAttributes

      # Events before
      eventsBefore = motion.GetEventsBefore()
      y.key_only("events_before", 8)
      for event in eventsBefore:
         self._emit_event(y, operator, event, 9)

      # Position — always emit even for reference motions (they may have valid coords)
      pos = motion.GetPosition()
      if pos:
         y.key_only("position", 8)
         self._emit_position(y, operator, pos, 9)
      else:
         y.key_value("position", None, 8)

      if motion.IsCircularMotion():
         via = motion.GetViaPosition()
         if via:
            y.key_only("via_position", 8)
            self._emit_position(y, operator, via, 9)
         else:
            y.key_value("via_position", None, 8)
      else:
         y.key_value("via_position", None, 8)

      # Events after
      eventsAfter = motion.GetEventsAfter()
      y.key_only("events_after", 8)
      for event in eventsAfter:
         self._emit_event(y, operator, event, 9)

   # ---- Event ----

   def HandleEvent(self, operator: DULPythonDownloadOperator, event: DULPythonEvent):
      # Events are handled inline within HandleMotion via _emit_event.
      # This callback is still invoked by the framework for events that
      # contain nested motions — we handle those recursively.
      pass

   def OutputEvent(self, operator: DULPythonDownloadOperator, event: DULPythonEvent):
      pass

   # ---- Output ----

   def CloseOutputFile(self, operator: DULPythonDownloadOperator):
      y = self._yaml
      y.blank()

      # Summary
      y.key_only("summary")
      y.key_value("program_count", self._programCount, 1)
      y.key_value("operation_group_count", self._groupCount, 1)
      y.key_value("operation_count", self._operationCount, 1)
      y.key_value("motion_count", self._motionCount, 1)
      y.key_value("event_count", self._eventCount, 1)
      y.inline_list("event_types_found", sorted(self._eventTypes), 1)
      y.inline_list("technologies_found", sorted(self._technologies), 1)
      y.key_only("attribute_counts", 1)
      for level, count in self._attrCounts.items():
         y.key_value(level, count, 2)

      # Write file
      os.makedirs(os.path.dirname(self._outputFilePath), exist_ok=True)
      with open(self._outputFilePath, "w", encoding="utf-8") as f:
         f.write(y.get_text())
      operator.AddOutputFilePath(self._outputFilePath)

   def WriteOutputFile(self, operator: DULPythonDownloadOperator):
      pass

   # ================================================================
   # Private helpers — emit sub-structures
   # ================================================================

   def _emit_joint(self, y: YamlEmitter, joint: DULPythonJoint, depth: int):
      y.list_item_mapping_start("name", joint.GetName(), depth)
      y.key_value("group_index", joint.GetJointGroupIndex(), depth + 1)
      y.key_value("dof_number", joint.GetDofNumber(), depth + 1)
      y.key_value("joint_index", joint.GetJointIndex(), depth + 1)
      y.key_value("port_name", joint.GetPortName(), depth + 1)
      y.key_value("role", safe_enum_name(joint.GetJointRole()), depth + 1)
      y.key_value("unit", joint.GetUnit(), depth + 1)
      y.key_value("is_external", joint.IsExternal(), depth + 1)
      try:
         y.key_value("kinematic_type", safe_enum_name(joint.GetJointType()), depth + 1)
      except Exception:
         y.key_value("kinematic_type", None, depth + 1)

   def _emit_tool_profile(self, y: YamlEmitter, profile: DULPythonToolProfile, depth: int):
      y.list_item_mapping_start("name", profile.GetName(), depth)
      y.key_value("index", safe_index(profile.GetIndex()), depth + 1)
      y.key_value("tool_type", safe_enum_name(profile.GetToolType()), depth + 1)
      try:
         y.key_value("is_vision_frame", profile.IsVisionFrame(), depth + 1)
      except Exception:
         y.key_value("is_vision_frame", None, depth + 1)
      pos = profile.GetXYZ()
      ori = profile.GetOrientation()
      y.inline_list("xyz_m", [pos[0], pos[1], pos[2]], depth + 1)
      y.inline_list("orientation_deg", [ori[0], ori[1], ori[2]], depth + 1)

   def _emit_base_profile(self, y: YamlEmitter, profile: DULPythonBaseProfile, depth: int):
      y.list_item_mapping_start("name", profile.GetName(), depth)
      y.key_value("index", safe_index(profile.GetIndex()), depth + 1)
      ref = profile.GetReferenceProfile()
      y.key_value("reference_profile", ref.GetName() if ref else None, depth + 1)
      pos = profile.GetXYZ()
      ori = profile.GetOrientation()
      y.inline_list("xyz_m", [pos[0], pos[1], pos[2]], depth + 1)
      y.inline_list("orientation_deg", [ori[0], ori[1], ori[2]], depth + 1)

   def _emit_accuracy_profile(self, y: YamlEmitter, profile: DULPythonAccuracyProfile, depth: int):
      y.list_item_mapping_start("name", profile.GetName(), depth)
      y.key_value("criteria", safe_enum_name(profile.GetAccuracyCriteria()), depth + 1)
      y.key_value("fly_by", safe_enum_name(profile.GetProfileFlyBy()), depth + 1)
      y.key_value("value", profile.GetValue(), depth + 1)
      y.key_value("unit", profile.GetUnit(), depth + 1)

   def _emit_motion_profile(self, y: YamlEmitter, profile: DULPythonMotionProfile, depth: int):
      y.list_item_mapping_start("name", profile.GetName(), depth)
      y.key_value("basis", safe_enum_name(profile.GetMotionProfileBasis()), depth + 1)
      y.key_value("type", safe_enum_name(profile.GetMotionProfileType()), depth + 1)
      y.inline_dict("speed", {"value": profile.GetSpeedValue(), "unit": profile.GetSpeedUnit()}, depth + 1)
      y.inline_dict("acceleration", {"value": profile.GetAccelValue(), "unit": profile.GetAccelUnit()}, depth + 1)

   def _emit_technology(self, y: YamlEmitter, tech: OlpCorePythonTechnology, depth: int):
      y.key_only("technology", depth)
      y.key_value("name", tech.GetName(), depth + 1)
      try:
         y.key_value("version", tech.GetVersion(), depth + 1)
      except Exception:
         y.key_value("version", None, depth + 1)
      try:
         y.key_value("uuid", tech.GetUuid(), depth + 1)
      except Exception:
         y.key_value("uuid", None, depth + 1)

   def _emit_resource(self, y: YamlEmitter, resource: OlpCorePythonResource, depth: int):
      y.list_item_mapping_start("name", resource.GetName(), depth)
      y.key_value("item_type", safe_enum_name(resource.GetItemType()), depth + 1)
      y.key_value("item_sub_type", safe_enum_name(resource.GetItemSubType()), depth + 1)
      y.key_value("manufacturer", resource.GetManufacturer(), depth + 1)
      y.key_value("model", resource.GetModel(), depth + 1)
      y.key_value("series", resource.GetSeries(), depth + 1)

      # Supported configurations and turns
      try:
         configs = resource.GetSupportedConfigurations()
         y.inline_list("supported_configurations", configs, depth + 1)
      except Exception:
         y.key_only("supported_configurations", depth + 1)

      try:
         turns = resource.GetSupportedTurns()
         y.inline_list("supported_turns", turns, depth + 1)
      except Exception:
         y.key_only("supported_turns", depth + 1)

      # Ports
      y.key_only("ports", depth + 1)
      try:
         ports = resource.GetAllPorts()
         for port in ports:
            y.list_item_mapping_start("name", port.GetName(), depth + 2)
            try:
               y.key_value("comment", port.GetComment(), depth + 3)
            except Exception:
               y.key_value("comment", "", depth + 3)
            y.key_value("data_type", safe_enum_name(port.GetValueType()), depth + 3)
            y.key_value("direction", safe_enum_name(port.GetPortDirection()), depth + 3)
      except Exception:
         pass

      # Attributes
      y.key_only("attributes", depth + 1)
      attrs = resource.GetAttributes()
      self._attrCounts["resource"] += len(attrs)
      for attr in attrs:
         self._emit_attribute(y, attr, depth + 2)

   def _emit_event(self, y: YamlEmitter, operator: DULPythonDownloadOperator, event: DULPythonEvent, depth: int):
      self._eventCount += 1
      eventType = event.GetEventType()
      self._eventTypes.add(eventType)

      y.list_item_mapping_start("name", event.GetName(), depth)
      y.key_value("group", event.GetGroupName(), depth + 1)
      y.key_value("insert_position", safe_enum_name(event.GetInsertPosition()), depth + 1)
      y.key_value("event_type", eventType, depth + 1)

      y.key_only("attributes", depth + 1)
      attrs = event.GetAttributes()
      self._attrCounts["event"] += len(attrs)
      for attr in attrs:
         self._emit_attribute(y, attr, depth + 2)

      # Nested motions within event (approach/retract)
      nestedMotions = event.GetMotions()
      if len(nestedMotions) > 0:
         y.key_only("motions", depth + 1)
         for motion in nestedMotions:
            self._emit_nested_motion(y, operator, motion, depth + 2)

   def _emit_nested_motion(self, y: YamlEmitter, operator: DULPythonDownloadOperator, motion: DULPythonMotion, depth: int):
      self._motionCount += 1
      y.list_item_mapping_start("name", motion.GetName(), depth)
      y.key_value("motion_type", safe_enum_name(motion.GetMotionType()), depth + 1)
      y.key_value("is_reference", motion.IsReferenceMotion(), depth + 1)

      pos = motion.GetPosition()
      if pos:
         y.key_only("position", depth + 1)
         self._emit_position(y, operator, pos, depth + 2)

   def _emit_position(self, y: YamlEmitter, operator: DULPythonDownloadOperator, position: DULPythonPosition, depth: int):
      y.key_value("name", position.GetName(), depth)
      y.key_value("process_type", safe_enum_name(position.GetProcessType()), depth)
      y.key_value("target_type", safe_enum_name(position.GetTargetType()), depth)

      xyz = position.GetXYZ()
      ori = position.GetOrientation()
      y.inline_list("xyz_m", [xyz[0], xyz[1], xyz[2]], depth)
      y.inline_list("orientation_deg", [ori[0], ori[1], ori[2]], depth)
      y.key_value("config", position.GetConfig(), depth)
      y.key_value("turn", position.GetTurn(), depth)

      # Main joints
      y.key_only("main_joints", depth)
      for joint, value in position.GetMainJointValues():
         y.list_item_mapping_start("name", joint.GetName(), depth + 1)
         y.key_value("value", value, depth + 2)

      # External joints
      y.key_only("external_joints", depth)
      for joint, value in position.GetExternalJointValues():
         y.list_item_mapping_start("name", joint.GetName(), depth + 1)
         y.key_value("value", value, depth + 2)

      # Position attributes
      y.key_only("attributes", depth)
      try:
         posAttrs = position.GetAttributes()
         self._attrCounts["position"] += len(posAttrs)
         for attr in posAttrs:
            self._emit_attribute(y, attr, depth + 1)
      except Exception:
         pass

   def _emit_attribute(self, y: YamlEmitter, attribute: OlpCorePythonAttribute, depth: int):
      attrName = attribute.GetName()
      propFlags = decode_olp_property(attribute.GetOlpProperty())
      typeName = type(attribute).__name__

      if OlpCorePythonBoolAttribute.__name__ in typeName:
         y.list_item_mapping_start("name", attrName, depth)
         y.key_value("type", "Bool", depth + 1)
         y.key_value("value", attribute.GetValue(), depth + 1)
         y.key_value("group_name", attribute.GetGroupName(), depth + 1)
         y.key_value("read_only", attribute.GetReadOnly(), depth + 1)
         y.key_value("value_unit_type", safe_enum_name(attribute.GetValueUnitType()), depth + 1)
         y.inline_list("olp_property", propFlags, depth + 1)

      elif OlpCorePythonIntegerArrayAttribute.__name__ in typeName:
         y.list_item_mapping_start("name", attrName, depth)
         y.key_value("type", "IntArray", depth + 1)
         y.inline_list("values", attribute.GetValues(), depth + 1)
         y.key_value("group_name", attribute.GetGroupName(), depth + 1)
         y.key_value("read_only", attribute.GetReadOnly(), depth + 1)
         y.key_value("value_unit_type", safe_enum_name(attribute.GetValueUnitType()), depth + 1)
         y.inline_list("olp_property", propFlags, depth + 1)

      elif OlpCorePythonIntegerAttribute.__name__ in typeName:
         y.list_item_mapping_start("name", attrName, depth)
         y.key_value("type", "Int", depth + 1)
         y.key_value("value", attribute.GetValue(), depth + 1)
         y.key_value("min", attribute.GetMinimum(), depth + 1)
         y.key_value("max", attribute.GetMaximum(), depth + 1)
         y.key_value("step_size", attribute.GetStepSize(), depth + 1)
         y.key_value("group_name", attribute.GetGroupName(), depth + 1)
         y.key_value("read_only", attribute.GetReadOnly(), depth + 1)
         y.key_value("value_unit_type", safe_enum_name(attribute.GetValueUnitType()), depth + 1)
         y.inline_list("olp_property", propFlags, depth + 1)

      elif OlpCorePythonDoubleArrayAttribute.__name__ in typeName:
         y.list_item_mapping_start("name", attrName, depth)
         y.key_value("type", "DoubleArray", depth + 1)
         y.inline_list("values", attribute.GetValues(), depth + 1)
         y.key_value("group_name", attribute.GetGroupName(), depth + 1)
         y.key_value("read_only", attribute.GetReadOnly(), depth + 1)
         y.key_value("value_unit_type", safe_enum_name(attribute.GetValueUnitType()), depth + 1)
         y.inline_list("olp_property", propFlags, depth + 1)

      elif OlpCorePythonDoubleAttribute.__name__ in typeName:
         y.list_item_mapping_start("name", attrName, depth)
         y.key_value("type", "Double", depth + 1)
         y.key_value("value", attribute.GetValue(), depth + 1)
         y.key_value("min", attribute.GetMinimum(), depth + 1)
         y.key_value("max", attribute.GetMaximum(), depth + 1)
         y.key_value("step_size", attribute.GetStepSize(), depth + 1)
         y.key_value("group_name", attribute.GetGroupName(), depth + 1)
         y.key_value("read_only", attribute.GetReadOnly(), depth + 1)
         y.key_value("value_unit_type", safe_enum_name(attribute.GetValueUnitType()), depth + 1)
         y.inline_list("olp_property", propFlags, depth + 1)

      elif OlpCorePythonStringArrayAttribute.__name__ in typeName:
         y.list_item_mapping_start("name", attrName, depth)
         y.key_value("type", "StringArray", depth + 1)
         y.inline_list("values", attribute.GetValues(), depth + 1)
         y.key_value("group_name", attribute.GetGroupName(), depth + 1)
         y.key_value("read_only", attribute.GetReadOnly(), depth + 1)
         y.key_value("value_unit_type", safe_enum_name(attribute.GetValueUnitType()), depth + 1)
         y.inline_list("olp_property", propFlags, depth + 1)

      elif OlpCorePythonStringAttribute.__name__ in typeName:
         y.list_item_mapping_start("name", attrName, depth)
         y.key_value("type", "String", depth + 1)
         y.key_value("value", attribute.GetValue(), depth + 1)
         y.key_value("group_name", attribute.GetGroupName(), depth + 1)
         y.key_value("read_only", attribute.GetReadOnly(), depth + 1)
         y.key_value("value_unit_type", safe_enum_name(attribute.GetValueUnitType()), depth + 1)
         y.inline_list("olp_property", propFlags, depth + 1)

      elif OlpCorePythonLiteralAttribute.__name__ in typeName:
         y.list_item_mapping_start("name", attrName, depth)
         y.key_value("type", "Literal", depth + 1)
         y.key_value("value", attribute.GetValue(), depth + 1)
         y.inline_list("values", attribute.GetValues(), depth + 1)
         y.key_value("index", attribute.GetIndex(), depth + 1)
         y.key_value("group_name", attribute.GetGroupName(), depth + 1)
         y.key_value("read_only", attribute.GetReadOnly(), depth + 1)
         y.key_value("value_unit_type", safe_enum_name(attribute.GetValueUnitType()), depth + 1)
         y.inline_list("olp_property", propFlags, depth + 1)
