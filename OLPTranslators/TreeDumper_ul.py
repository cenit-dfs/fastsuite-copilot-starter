"""
TreeDumper YAML Uploader — FASTSUITE E2

Generic uploader that reads TreeDumper YAML files and reconstructs the OLP
program tree in E2. This is the upload counterpart to TreeDumper.py (download).

Designed as the standard intermediate format:
  Vendor robot code  →  Vendor Parser  →  YAML  →  This Uploader  →  E2 OLP tree

Schema version compatibility is checked at parse time.
"""

import sys
import os
import inspect
sys.dont_write_bytecode = True
sys.path.append(str(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

from cenpyupload import Uploader
from cenpyupload import ULPythonUploadOperator
from cenpydownload import MotionType
from cenpydownload import ProcessType
from cenpydownload import TargetType
from cenpyolpcore import InsertPosition
from cenpyolpcore import AttributeValueUnitType
from io import TextIOWrapper

UPLOAD_CLASS_NAME = "TreeDumperUploader"

# Schema version this uploader supports
SUPPORTED_SCHEMA_VERSIONS = ["1.0"]

def _enum_lookup(enum_class, name, default):
   """Safe enum lookup by name — returns default if name not found."""
   try:
      return getattr(enum_class, name)
   except AttributeError:
      return default


# =============================================================================
# Minimal YAML Parser (no pyyaml dependency)
# =============================================================================

def _parse_yaml_value(raw):
   """Parse a single YAML scalar value from string."""
   raw = raw.strip()
   if raw == "~" or raw == "null" or raw == "":
      return None
   if raw == "true":
      return True
   if raw == "false":
      return False
   if raw.startswith('"') and raw.endswith('"'):
      return raw[1:-1]
   if raw.startswith("'") and raw.endswith("'"):
      return raw[1:-1]
   try:
      if "." in raw or "e" in raw.lower():
         return float(raw)
      return int(raw)
   except (ValueError, TypeError):
      return raw


def _parse_inline_list(raw):
   """Parse a YAML inline list like [a, b, c]."""
   raw = raw.strip()
   if not raw.startswith("[") or not raw.endswith("]"):
      return []
   inner = raw[1:-1].strip()
   if not inner:
      return []
   items = []
   current = ""
   in_quotes = False
   quote_char = None
   for ch in inner:
      if ch in ('"', "'") and not in_quotes:
         in_quotes = True
         quote_char = ch
         current += ch
      elif ch == quote_char and in_quotes:
         in_quotes = False
         current += ch
      elif ch == "," and not in_quotes:
         items.append(_parse_yaml_value(current))
         current = ""
      else:
         current += ch
   if current.strip():
      items.append(_parse_yaml_value(current))
   return items


def _parse_inline_dict(raw):
   """Parse a YAML inline dict like {key: value, key2: value2}."""
   raw = raw.strip()
   if not raw.startswith("{") or not raw.endswith("}"):
      return {}
   inner = raw[1:-1].strip()
   if not inner:
      return {}
   result = {}
   pairs = inner.split(",")
   for pair in pairs:
      if ":" in pair:
         k, v = pair.split(":", 1)
         result[k.strip()] = _parse_yaml_value(v)
   return result


def parse_yaml(text):
   """
   Minimal YAML parser sufficient for TreeDumper output.
   Returns nested dicts/lists matching the YAML structure.
   """
   lines = text.split("\n")
   return _parse_block(lines, 0, 0)[0]


def _get_indent(line):
   return len(line) - len(line.lstrip())


def _parse_block(lines, start, min_indent):
   """Parse a YAML block recursively. Returns (result_dict_or_list, next_line_index)."""
   result = {}
   i = start
   while i < len(lines):
      line = lines[i]
      stripped = line.strip()

      # Skip empty lines and comments
      if not stripped or stripped.startswith("#"):
         i += 1
         continue

      indent = _get_indent(line)
      if indent < min_indent:
         break

      # List item
      if stripped.startswith("- "):
         # This is a list — backtrack and parse as list
         lst, i = _parse_list(lines, i, indent)
         return lst, i

      # Key: value
      if ":" in stripped:
         colon_pos = stripped.index(":")
         key = stripped[:colon_pos].strip()
         rest = stripped[colon_pos + 1:].strip()

         if rest:
            # Inline value, list, or dict
            if rest.startswith("["):
               result[key] = _parse_inline_list(rest)
            elif rest.startswith("{"):
               result[key] = _parse_inline_dict(rest)
            else:
               result[key] = _parse_yaml_value(rest)
            i += 1
         else:
            # Block value — check next lines
            next_i = i + 1
            while next_i < len(lines) and (not lines[next_i].strip() or lines[next_i].strip().startswith("#")):
               next_i += 1
            if next_i < len(lines) and _get_indent(lines[next_i]) > indent:
               child, i = _parse_block(lines, next_i, _get_indent(lines[next_i]))
               result[key] = child
            else:
               result[key] = None
               i = next_i
      else:
         i += 1

   return result, i


def _parse_list(lines, start, list_indent):
   """Parse a YAML list of items."""
   result = []
   i = start
   while i < len(lines):
      line = lines[i]
      stripped = line.strip()

      if not stripped or stripped.startswith("#"):
         i += 1
         continue

      indent = _get_indent(line)
      if indent < list_indent:
         break

      if indent == list_indent and stripped.startswith("- "):
         item_content = stripped[2:].strip()

         if ":" in item_content:
            # List item is a mapping
            colon_pos = item_content.index(":")
            first_key = item_content[:colon_pos].strip()
            first_rest = item_content[colon_pos + 1:].strip()

            item = {}
            if first_rest.startswith("["):
               item[first_key] = _parse_inline_list(first_rest)
            elif first_rest.startswith("{"):
               item[first_key] = _parse_inline_dict(first_rest)
            elif first_rest:
               item[first_key] = _parse_yaml_value(first_rest)
            else:
               # Block value under list item
               next_i = i + 1
               while next_i < len(lines) and (not lines[next_i].strip() or lines[next_i].strip().startswith("#")):
                  next_i += 1
               if next_i < len(lines) and _get_indent(lines[next_i]) > list_indent + 2:
                  child, next_i = _parse_block(lines, next_i, _get_indent(lines[next_i]))
                  item[first_key] = child
               else:
                  item[first_key] = None
               i = next_i

               # Parse remaining keys at same depth as first key
               child_indent = list_indent + 2
               while i < len(lines):
                  cline = lines[i]
                  cs = cline.strip()
                  if not cs or cs.startswith("#"):
                     i += 1
                     continue
                  ci = _get_indent(cline)
                  if ci < child_indent:
                     break
                  if ci == child_indent and ":" in cs and not cs.startswith("- "):
                     ccolon = cs.index(":")
                     ck = cs[:ccolon].strip()
                     cr = cs[ccolon + 1:].strip()
                     if cr.startswith("["):
                        item[ck] = _parse_inline_list(cr)
                     elif cr.startswith("{"):
                        item[ck] = _parse_inline_dict(cr)
                     elif cr:
                        item[ck] = _parse_yaml_value(cr)
                     else:
                        next_i = i + 1
                        while next_i < len(lines) and (not lines[next_i].strip() or lines[next_i].strip().startswith("#")):
                           next_i += 1
                        if next_i < len(lines) and _get_indent(lines[next_i]) > child_indent:
                           child, next_i = _parse_block(lines, next_i, _get_indent(lines[next_i]))
                           item[ck] = child
                        else:
                           item[ck] = None
                        i = next_i
                        continue
                     i += 1
                  elif ci == child_indent and cs.startswith("- "):
                     break
                  else:
                     i += 1
               result.append(item)
               continue

            i += 1
            # Parse remaining keys of this mapping item
            child_indent = list_indent + 2
            while i < len(lines):
               cline = lines[i]
               cs = cline.strip()
               if not cs or cs.startswith("#"):
                  i += 1
                  continue
               ci = _get_indent(cline)
               if ci < child_indent:
                  break
               if ci == child_indent and ":" in cs and not cs.startswith("- "):
                  ccolon = cs.index(":")
                  ck = cs[:ccolon].strip()
                  cr = cs[ccolon + 1:].strip()
                  if cr.startswith("["):
                     item[ck] = _parse_inline_list(cr)
                  elif cr.startswith("{"):
                     item[ck] = _parse_inline_dict(cr)
                  elif cr:
                     item[ck] = _parse_yaml_value(cr)
                  else:
                     next_i = i + 1
                     while next_i < len(lines) and (not lines[next_i].strip() or lines[next_i].strip().startswith("#")):
                        next_i += 1
                     if next_i < len(lines) and _get_indent(lines[next_i]) > child_indent:
                        child, next_i = _parse_block(lines, next_i, _get_indent(lines[next_i]))
                        item[ck] = child
                     else:
                        item[ck] = None
                     i = next_i
                     continue
                  i += 1
               elif ci == child_indent and cs.startswith("- "):
                  break
               else:
                  i += 1

            result.append(item)
         else:
            # Scalar list item
            result.append(_parse_yaml_value(item_content))
            i += 1
      else:
         break

   return result, i


# =============================================================================
# TreeDumperUploader
# =============================================================================

class TreeDumperUploader(Uploader):

   def __init__(self):
      super().__init__()
      self._connectedJoints = []
      self._jointsByName = {}
      # DUL profiles: for ULPythonOperation.SetUsedBaseProfile/ToolProfile
      self._baseProfilesByName = {}
      self._toolProfilesByName = {}
      # UL profiles: for ULPythonProgram/OperationGroup.SetUsedBaseProfile/ToolProfile
      self._baseProfilesByName_ul = {}
      self._toolProfilesByName_ul = {}
      # Keep strong Python references to all created E2 objects to prevent pybind11
      # from releasing C++ objects while E2 still holds raw/weak pointers to them.
      self._createdObjects = []

   def Initialize(self, operator: ULPythonUploadOperator):
      logger = operator.GetLogOperator()
      logger.LogDebug("TreeDumperUploader Initialize")

      controller = operator.GetController()

      # Cache joints by name for position reconstruction
      for joint in controller.GetConnectedJoints():
         self._connectedJoints.append(joint)
         self._jointsByName[joint.GetName()] = joint

      # Cache existing profiles by name.
      # DUL objects go to the plain cache (accepted by ULPythonOperation).
      # ULPythonProgram and ULPythonOperationGroup require ULPythonBaseProfile, so we
      # create UL wrappers that copy the station transform so IK resolves correctly.
      for bp in controller.GetBaseProfiles():
         self._baseProfilesByName[bp.GetName()] = bp
         ulBp = operator.CreateEmptyBaseProfile()
         ulBp.SetName(bp.GetName())
         xyz = bp.GetXYZ()
         if xyz:
            ulBp.SetXYZ(xyz)
         ori = bp.GetOrientation()
         if ori:
            ulBp.SetOrientation(ori)
         self._baseProfilesByName_ul[bp.GetName()] = ulBp

      for tp in controller.GetToolProfiles():
         self._toolProfilesByName[tp.GetName()] = tp
         ulTp = operator.CreateEmptyToolProfile()
         ulTp.SetName(tp.GetName())
         xyz = tp.GetXYZ()
         if xyz:
            ulTp.SetXYZ(xyz)
         ori = tp.GetOrientation()
         if ori:
            ulTp.SetOrientation(ori)
         self._toolProfilesByName_ul[tp.GetName()] = ulTp

   def ParseFile(self, operator: ULPythonUploadOperator, fileObject: TextIOWrapper):
      logger = operator.GetLogOperator()
      logger.LogDebug("TreeDumperUploader ParseFile")

      text = fileObject.read()
      data = parse_yaml(text)

      if not data:
         logger.LogError("Failed to parse YAML file")
         return

      # Schema version check
      meta = data.get("meta", {})
      if meta:
         version = str(meta.get("translator_version", ""))
         if version and version not in SUPPORTED_SCHEMA_VERSIONS:
            logger.LogWarn("YAML schema version " + version + " not in supported list " + str(SUPPORTED_SCHEMA_VERSIONS))

      # Build programs
      programs = data.get("programs", [])
      if not programs:
         logger.LogWarn("No programs found in YAML")
         return

      attrSetter = operator.GetAttributeSetterOperator()

      for progData in programs:
         self._buildProgram(operator, attrSetter, progData, logger)

   def Finalize(self, operator: ULPythonUploadOperator):
      logger = operator.GetLogOperator()
      logger.LogDebug("TreeDumperUploader Finalize")

   # ================================================================
   # Program builder
   # ================================================================

   def _buildProgram(self, operator, attrSetter, progData, logger):
      program = operator.CreateEmptyProgram()
      self._createdObjects.append(program)
      program.SetName(progData.get("name", "Unnamed"))
      program.SetIsMainProgram(progData.get("is_main", True))

      # Base profile (Program requires ULPythonBaseProfile)
      bpName = progData.get("base_profile")
      if bpName and bpName in self._baseProfilesByName_ul:
         program.SetUsedBaseProfile(self._baseProfilesByName_ul[bpName])

      # Tool profile (Program requires ULPythonToolProfile)
      tpName = progData.get("tool_profile")
      if tpName and tpName in self._toolProfilesByName_ul:
         program.SetUsedToolProfile(self._toolProfilesByName_ul[tpName])

      # Program attributes
      attrs = progData.get("attributes", [])
      if attrs:
         for attrData in attrs:
            attr = self._buildAttribute(attrSetter, attrData)
            if attr:
               program.AddAttribute(attr)

      # Operation groups
      groups = progData.get("operation_groups", [])
      if groups:
         for groupData in groups:
            group = self._buildOperationGroup(operator, attrSetter, groupData, logger)
            if group:
               program.AddOperationGroup(group)

   # ================================================================
   # Operation Group builder
   # ================================================================

   def _buildOperationGroup(self, operator, attrSetter, groupData, logger):
      group = operator.CreateEmptyOperationGroup()
      self._createdObjects.append(group)
      group.SetName(groupData.get("name", "Unnamed"))

      # Base profile (OperationGroup requires ULPythonBaseProfile)
      bpName = groupData.get("base_profile")
      if bpName and bpName in self._baseProfilesByName_ul:
         group.SetUsedBaseProfile(self._baseProfilesByName_ul[bpName])

      # Tool profile (OperationGroup requires ULPythonToolProfile)
      tpName = groupData.get("tool_profile")
      if tpName and tpName in self._toolProfilesByName_ul:
         group.SetUsedToolProfile(self._toolProfilesByName_ul[tpName])

      # Group attributes
      attrs = groupData.get("attributes", [])
      if attrs:
         for attrData in attrs:
            attr = self._buildAttribute(attrSetter, attrData)
            if attr:
               group.AddAttribute(attr)

      # Operations
      operations = groupData.get("operations", [])
      if operations:
         for opData in operations:
            opName = opData.get("name", "?")
            try:
               op = self._buildOperation(operator, attrSetter, opData, logger)
               if op:
                  group.AddOperation(op)
                  logger.LogDebug("TreeDumper_ul: added op " + opName)
            except Exception as exc:
               logger.LogError("TreeDumper_ul: failed building op " + opName + ": " + str(exc))

      return group

   # ================================================================
   # Operation builder
   # ================================================================

   def _buildOperation(self, operator, attrSetter, opData, logger):
      operation = operator.CreateEmptyOperation()
      self._createdObjects.append(operation)
      operation.SetName(opData.get("name", "Unnamed"))

      # Base profile
      bpName = opData.get("base_profile")
      if bpName and bpName in self._baseProfilesByName:
         operation.SetUsedBaseProfile(self._baseProfilesByName[bpName])

      # Tool profile
      tpName = opData.get("tool_profile")
      if tpName and tpName in self._toolProfilesByName:
         operation.SetUsedToolProfile(self._toolProfilesByName[tpName])

      # Operation attributes
      attrs = opData.get("attributes", [])
      if attrs:
         for attrData in attrs:
            try:
               attr = self._buildAttribute(attrSetter, attrData)
               if attr:
                  operation.AddAttribute(attr)
            except Exception as exc:
               logger.LogWarn("TreeDumper_ul: skipping op attr " + str(attrData.get("name","?")) + ": " + str(exc))

      # Motions
      motions = opData.get("motions", [])
      if motions:
         for motionData in motions:
            motion = self._buildMotion(operator, attrSetter, motionData, logger)
            if motion:
               operation.AddMotion(motion)

      return operation

   # ================================================================
   # Motion builder
   # ================================================================

   def _buildMotion(self, operator, attrSetter, motionData, logger):
      motion = operator.CreateEmptyMotion()
      self._createdObjects.append(motion)
      motion.SetName(motionData.get("name", ""))

      # Motion type
      mtName = motionData.get("motion_type", "Linear")
      mt = _enum_lookup(MotionType, mtName, MotionType.Linear)
      motion.SetMotionType(mt)

      # Events before
      eventsBefore = motionData.get("events_before", [])
      if eventsBefore:
         builtEvents = []
         for evData in eventsBefore:
            ev = self._buildEvent(operator, attrSetter, evData, logger)
            if ev:
               builtEvents.append(ev)
         if builtEvents:
            motion.SetEventsBefore(builtEvents)

      # Position
      posData = motionData.get("position")
      if posData and isinstance(posData, dict):
         pos = self._buildPosition(operator, posData, logger)
         if pos:
            motion.SetPosition(pos)
      elif motionData.get("is_reference", False):
         # Reference motions (e.g. touch-sensing) have no coordinates in YAML.
         # E2 still requires a position object; technology computes actual coords.
         refPos = operator.CreateEmptyPosition()
         self._createdObjects.append(refPos)
         refPos.SetName(motionData.get("name", ""))
         refPos.SetProcessType(_enum_lookup(ProcessType, "Auxiliary", ProcessType.Auxiliary))
         motion.SetPosition(refPos)

      # Via position (circular motions)
      viaData = motionData.get("via_position")
      if viaData and isinstance(viaData, dict):
         viaPos = self._buildPosition(operator, viaData, logger)
         if viaPos:
            motion.SetViaPosition(viaPos)

      # Events after
      eventsAfter = motionData.get("events_after", [])
      if eventsAfter:
         builtEvents = []
         for evData in eventsAfter:
            ev = self._buildEvent(operator, attrSetter, evData, logger)
            if ev:
               builtEvents.append(ev)
         if builtEvents:
            motion.SetEventsAfter(builtEvents)

      return motion

   # ================================================================
   # Position builder
   # ================================================================

   def _buildPosition(self, operator, posData, logger):
      position = operator.CreateEmptyPosition()
      self._createdObjects.append(position)
      position.SetName(posData.get("name", ""))

      # Process type
      ptName = posData.get("process_type", "Auxiliary")
      position.SetProcessType(_enum_lookup(ProcessType, ptName, ProcessType.Auxiliary))

      # Target type
      ttName = posData.get("target_type", "Cartesian")
      # CartesianAndJoint or unknown → default to Cartesian
      position.SetTargetType(_enum_lookup(TargetType, ttName, TargetType.Cartesian))

      # Cartesian coordinates (meters, degrees)
      xyz = posData.get("xyz_m", [0.0, 0.0, 0.0])
      if xyz and len(xyz) >= 3:
         position.SetXYZ((float(xyz[0]), float(xyz[1]), float(xyz[2])))

      ori = posData.get("orientation_deg", [0.0, 0.0, 0.0])
      if ori and len(ori) >= 3:
         position.SetOrientation((float(ori[0]), float(ori[1]), float(ori[2])))

      # Config and turn
      config = posData.get("config")
      if config:
         position.SetConfig(str(config))

      turn = posData.get("turn")
      if turn:
         position.SetTurn(str(turn))

      # Main joints
      mainJoints = posData.get("main_joints", [])
      if mainJoints:
         jointValues = []
         for jd in mainJoints:
            jname = jd.get("name", "")
            jval = jd.get("value", 0.0)
            if jname in self._jointsByName:
               jointValues.append((self._jointsByName[jname], float(jval)))
         if jointValues:
            position.SetExplicitMainJointValues(jointValues)

      # External joints
      extJoints = posData.get("external_joints", [])
      if extJoints:
         jointValues = []
         for jd in extJoints:
            jname = jd.get("name", "")
            jval = jd.get("value", 0.0)
            if jname in self._jointsByName:
               jointValues.append((self._jointsByName[jname], float(jval)))
         if jointValues:
            position.SetExplicitExternalJointValues(jointValues)

      return position

   # ================================================================
   # Event builder
   # ================================================================

   def _buildEvent(self, operator, attrSetter, evData, logger):
      event = operator.CreateEmptyEvent()
      self._createdObjects.append(event)
      event.SetName(evData.get("name", ""))

      # Insert position
      ipName = evData.get("insert_position", "InsertNone")
      event.SetInsertPosition(_enum_lookup(InsertPosition, ipName, InsertPosition.InsertNone))

      # Event attributes
      attrs = evData.get("attributes", [])
      if attrs:
         for attrData in attrs:
            attr = self._buildAttribute(attrSetter, attrData)
            if attr:
               event.AddAttribute(attr)

      # Nested motions (approach/retract events contain motions)
      nestedMotions = evData.get("motions", [])
      if nestedMotions:
         for mData in nestedMotions:
            nestedMotion = self._buildNestedMotion(operator, mData, logger)
            if nestedMotion:
               event.AddMotion(nestedMotion)

      return event

   # ================================================================
   # Nested motion builder (for approach/retract events)
   # ================================================================

   def _buildNestedMotion(self, operator, mData, logger):
      motion = operator.CreateEmptyMotion()
      self._createdObjects.append(motion)
      motion.SetName(mData.get("name", ""))

      mtName = mData.get("motion_type", "Linear")
      motion.SetMotionType(_enum_lookup(MotionType, mtName, MotionType.Linear))

      posData = mData.get("position")
      if posData and isinstance(posData, dict):
         pos = self._buildPosition(operator, posData, logger)
         if pos:
            motion.SetPosition(pos)

      return motion

   # ================================================================
   # Attribute builder
   # ================================================================

   def _buildAttribute(self, attrSetter, attrData):
      if not attrData or not isinstance(attrData, dict):
         return None

      attrType = attrData.get("type", "")
      name = attrData.get("name", "")

      attr = None

      if attrType == "Bool":
         attr = attrSetter.CreateWritingBoolAttributesObject()
         val = attrData.get("value")
         if val is not None:
            attr.SetValue(bool(val))

      elif attrType == "Int":
         attr = attrSetter.CreateWritingIntAttributesObject()
         val = attrData.get("value")
         if val is not None:
            attr.SetValue(int(val))
         minv = attrData.get("min")
         if minv is not None:
            attr.SetMinimum(int(minv))
         maxv = attrData.get("max")
         if maxv is not None:
            attr.SetMaximum(int(maxv))
         step = attrData.get("step_size")
         if step is not None:
            attr.SetStepSize(int(step))

      elif attrType == "Double":
         attr = attrSetter.CreateWritingDoubleAttributesObject()
         val = attrData.get("value")
         if val is not None:
            attr.SetValue(float(val))
         minv = attrData.get("min")
         if minv is not None:
            attr.SetMinimum(float(minv))
         maxv = attrData.get("max")
         if maxv is not None:
            attr.SetMaximum(float(maxv))
         step = attrData.get("step_size")
         if step is not None:
            attr.SetStepSize(float(step))

      elif attrType == "String":
         attr = attrSetter.CreateWritingStringAttributesObject()
         val = attrData.get("value")
         if val is not None:
            attr.SetValue(str(val))

      elif attrType == "Literal":
         attr = attrSetter.CreateWritingLiteralAttributesObject()
         values = attrData.get("values")
         if values:
            attr.SetValues([str(v) for v in values])
         val = attrData.get("value")
         if val is not None:
            attr.SetValue(str(val))

      elif attrType == "IntArray":
         attr = attrSetter.CreateWritingIntArrayAttributesObject()
         values = attrData.get("values")
         if values:
            attr.SetValues([int(v) for v in values])

      elif attrType == "DoubleArray":
         attr = attrSetter.CreateWritingDoubleArrayAttributesObject()
         values = attrData.get("values")
         if values:
            attr.SetValues([float(v) for v in values])

      elif attrType == "StringArray":
         attr = attrSetter.CreateWritingStringArrayAttributesObject()
         values = attrData.get("values")
         if values:
            attr.SetValues([str(v) for v in values])

      if attr is None:
         return None

      # Common properties
      if name:
         attr.SetName(name)

      groupName = attrData.get("group_name")
      if groupName is not None:
         attr.SetGroupName(str(groupName))

      readOnly = attrData.get("read_only")
      if readOnly is not None:
         attr.SetReadOnly(bool(readOnly))

      # OLP property flags → bitwise OR
      olpProps = attrData.get("olp_property", [])
      if olpProps:
         bitwise = 0
         for flag in olpProps:
            bitwise |= _OLP_PROPERTY_MAP.get(str(flag), 0)
         if bitwise:
            attr.SetOlpProperty(bitwise)

      # Value unit type
      unitType = attrData.get("value_unit_type")
      if unitType:
         attr.SetValueUnitType(_enum_lookup(AttributeValueUnitType, str(unitType), AttributeValueUnitType.Standard))

      return attr


# OLP property flag name → bit value
_OLP_PROPERTY_MAP = {
   "UserAttribute": 1 << 0,
   "ProcessAttribute": 1 << 1,
   "OperationAttribute": 1 << 2,
   "OperationGroupAttribute": 1 << 3,
   "GlobalAttribute": 1 << 4,
   "ReadOnlyAttribute": 1 << 5,
   "ControllerAttribute": 1 << 6,
}
