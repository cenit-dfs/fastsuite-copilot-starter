---
name: downloader
description: Guide for creating and modifying FASTSUITE E2 OLP downloaders (robot program generators). Use when working on files under OLPTranslators/.
applyTo: OLPTranslators/**/*.py
---

# E2 OLP Downloader Skill

## What is a Downloader?

A downloader converts the FASTSUITE E2 OLP object tree (programs, operations, motions, events) into vendor-specific robot code (KRL for KUKA, RAPID for ABB, LS for FANUC, etc.). It is a Python class that inherits from `Downloader` and implements lifecycle callbacks.

## Start Here: Tree Dumper First

Before changing vendor syntax emission, first inspect what E2 is actually giving you.

Default workflow:

1. Run `community/OLPTranslators/Simple_Python_Translator.py` to dump the active OLP tree as a `.txt` reference.
2. Use that dump to identify the exact program / operation / motion / event / attribute path that controls the behavior.
3. Only after the dump confirms the data exists should you edit the vendor downloader.
4. If the dump does not contain the expected data, stop looking in the downloader and move one layer closer to the real owner: technology callbacks, uploader reconstruction, controller/resource mapping, or E2-generated virtual data.

Use the tree dumper as the source of truth for:

- Exact callback-visible structure and ordering
- Event names, event types, insert positions, and repeated attribute groups
- Motion context such as `IsReferenceMotion()`, `ProcessType`, target type, config, and turn
- Technology-managed artifacts that may appear in the OLP tree even when they do not exist in robot native code

Do not start by guessing from generated robot code alone. Start from the tree dump, then verify the nearest reference implementation, then make the smallest downloader change.

## API Authority

- Use `typings/cenpydownload`, `typings/cenpyolpcore`, `typings/cenpymath`, and related repo stubs as the authority for method names, signatures, enum members, and return types.
- Use the Obsidian vault as the authority for lifecycle order, callback semantics, patterns, and gotchas.
- If a stubbed API disagrees with the vault text, trust `typings/` first and verify against real downloader code or runtime output.

Short rule: signatures from `typings/`, behavior from Obsidian.

## Reference Files

| File | Purpose |
|------|---------|
| `community/OLPTranslators/Simple_Python_Translator.py` | **OLP tree dumper** — downloads the complete object tree as `.txt` for analysis. Trigger a download in E2 to get one. |
| `OLPTranslators/TreeDumper.py` | **Structured YAML tree dumper** — use when you need deterministic diffs, round-trip experiments, or to compare original vs re-downloaded OLP trees. |
| `community/OLPTranslators/KUKA/KUKA_KRC5.py` | **Canonical base downloader** — motion FOLDs, position data, event handling |
| `community/OLPTranslators/ABB/ABB_IRC5.py` | **Advanced multi-plugin** downloader with technology plugins |
| `community/OLPTranslators/KAWASAKI/KAWASAKI_AS.py` | **Kawasaki AS reference** — read [`references/kawasaki.md`](references/kawasaki.md) before changing it |
| Obsidian vault `10_API_Reference/Download/` | Full Download API documentation (via `obsidian-e2` MCP) |
| Obsidian vault `10_API_Reference/OlpCore/` | Core object model — attributes, resources, technologies (via `obsidian-e2` MCP) |
| `skills/downloader/templates/base_downloader.py` | Minimal starter template |

## Finished Downloader Lifecycle

Use `OLPTranslators/<VENDOR>/` in the starter as the development workspace. Once a general-purpose downloader is tested, documented, and accepted into the community repository, make `community/OLPTranslators/<VENDOR>/` its canonical source and remove the duplicate starter copy. Keep cross-vendor agent guidance in this skill and vendor-specific behavior under `docs/ctrl-specific/<VENDOR>/` or a focused skill reference. Product-release promotion is a separate qualification decision; do not maintain independent community and starter implementations.

## Investigation Workflow

### When to use `Simple_Python_Translator.py`

Use the simple text dumper first for most downloader work:

- New vendor downloader development
- Missing event handling
- Position / frame / config / turn questions
- Signal extraction and resource-port debugging
- Callback order and ownership questions

It is the fastest way to answer: "Does E2 expose this data to the downloader at all?"

### When to use `TreeDumper.py`

Use the YAML tree dumper when the work needs structure-preserving comparison rather than quick inspection:

- Original vs modified OLP tree diffing
- Download -> upload -> re-download round-trip analysis
- Comparing event-owned nested motions
- Inspecting large programs where text dumps are noisy
- Building generic parsers or uploaders from a stable schema

### Diffing scenario files across sessions

`community/scenarios/**/*.cendoc` files are Git LFS-tracked (`community/.gitattributes`).
`git diff`/`git status` on a `.cendoc` only shows the LFS pointer's hash and size changing, never
the actual attribute/geometry content — it is easy to conclude "nothing changed in the scenario"
when something did. To see what actually changed, diff the corresponding `reference/*.yaml` or
`.xml` dump for the same program instead; that text projection of the tree is what shows, e.g., an
attribute value flipping between captures.

### Ownership Check: Downloader vs Technology vs Uploader

If the tree dump shows the data already missing or transformed before vendor emission, the downloader is not the controlling layer.

Typical ownership split:

- Downloader: vendor syntax emission, output ordering, formatting, controller mapping
- Technology: workmethods, technology-specific events, virtual approach/retract behavior, generated helper motions
- Uploader: reconstruction of OLP structure from external files or intermediate formats

Practical rule from round-trip experiments:

- If a seam motion keeps Cartesian targets and user events but loses approach/retract technology events, that usually indicates technology-managed regeneration, not a downloader defect.
- If a touch-sensing reference motion loses `TouchSensingEvent` or nested sensing motions on re-import, that is typically technology-managed behavior and cannot be fixed by downloader emission alone.

---

## Download Lifecycle (Callback Order)

The E2 download starter calls these methods in this exact order:

```
1. __init__()              — class construction, initialize arrays/variables
2. Initialize(operator)    — called ONCE per download, even with sub-programs
3. OutputHeader(operator, controller) — header info (controller name, date, etc.)
4. CreateOutputFile(operator)  — define output file paths
5. ProgramStart(operator, program)
   ├─ OperationGroupStart(operator, operationGroup)
   │  ├─ OperationStart(operator, operation)
   │  │  ├─ HandleMotion(operator, motion)
   │  │  │  ├─ eventsBefore → HandleEvent(operator, event, motion)
   │  │  │  ├─ [read ahead eventsAfter for tech events like ArcOn/Off]
   │  │  │  ├─ OutputPositionData(operator, position)
   │  │  │  ├─ OutputMotionData(operator, motion, ...)
   │  │  │  └─ eventsAfter → HandleEvent(operator, event, motion)
   │  │  └─ ... (more motions)
   │  ├─ OperationEnd(operator, operation)
   │  └─ ... (more operations)
   ├─ OperationGroupEnd(operator, operationGroup)
   └─ ... (more groups)
6. ProgramEnd(operator, program)
7. WriteOutputFile(operator)  — write all buffered content to files
8. CloseOutputFile(operator)  — register output files with E2
```

### Key Callback Signatures

```python
def __init__(self) -> None:
def Initialize(self, operator: DULPythonDownloadOperator):
def OutputHeader(self, operator: DULPythonDownloadOperator, controller: DULPythonController):
def ProgramStart(self, operator: DULPythonDownloadOperator, program: DULPythonProgram):
def ProgramEnd(self, operator: DULPythonDownloadOperator, program: DULPythonProgram):
def OperationGroupStart(self, operator: DULPythonDownloadOperator, operationGroup: DULPythonOperationGroup):
def OperationGroupEnd(self, operator: DULPythonDownloadOperator, operationGroup: DULPythonOperationGroup):
def OperationStart(self, operator: DULPythonDownloadOperator, operation: DULPythonOperation):
def OperationEnd(self, operator: DULPythonDownloadOperator, operation: DULPythonOperation):
def HandleMotion(self, operator: DULPythonDownloadOperator, motion: DULPythonMotion):
def HandleEvent(self, operator: DULPythonDownloadOperator, event: DULPythonEvent, motion: DULPythonMotion):
def SubprogramStart(self, operator: DULPythonDownloadOperator, subprogram: DULPythonSubprogram):
def SubProgramEnd(self, operator: DULPythonDownloadOperator, subprogram: DULPythonSubprogram):
def CreateOutputFile(self, operator: DULPythonDownloadOperator):
def WriteOutputFile(self, operator: DULPythonDownloadOperator):
def CloseOutputFile(self, operator: DULPythonDownloadOperator):
```

---

## Essential API Reference

### DULPythonDownloadOperator

```python
operator.GetLogOperator()          # → logger with .LogDebug(), .LogInfo(), .LogWarn(), .LogError()
operator.GetController()           # → DULPythonController
operator.AddOutputFilePath(path)   # Register output file with E2
operator.GetCurrentLanguage()      # → str (e.g., "en-US")
operator.GetWindowsEnvironmentVariable(name)  # → str
```

### DULPythonController

```python
controller.GetName()               # → str
controller.GetManufacturer()       # → str
controller.GetSeries()             # → str
controller.GetModel()              # → str
controller.GetControllerType()     # → enum (.name for string)
controller.GetOutputDirectory()    # → str (output path)
controller.GetActiveProgram()      # → DULPythonProgram
controller.GetConnectedJoints()    # → list[DULPythonJoint]
controller.GetToolProfiles()       # → list[DULPythonToolProfile]
controller.GetBaseProfiles()       # → list[DULPythonBaseProfile]
controller.GetAccuracyProfiles()   # → list[DULPythonAccuracyProfile]
controller.GetMotionProfiles()     # → list[DULPythonMotionProfile]
controller.GetAttributes()         # → list[attribute]
controller.GetResources()          # → list[OlpCorePythonResource]
controller.GetString(name, flag)   # → str (controller string attribute)
```

### DULPythonProgram

```python
program.GetName()                  # → str
program.IsMainProgram()            # → bool
program.GetUsedBaseProfile()       # → DULPythonBaseProfile | None
program.GetUsedToolProfile()       # → DULPythonToolProfile | None
program.GetAttributes()            # → list[attribute]
```

### DULPythonOperation / DULPythonOperationGroup

```python
operation.GetName()                # → str
operation.GetOperationType()       # → enum (.name = "Normal", "Auxiliary", etc.)
operation.GetUsedBaseProfile()     # → DULPythonBaseProfile
operation.GetUsedToolProfile()     # → DULPythonToolProfile
operation.GetAttributes()          # → list[attribute]
operationGroup.GetName()           # → str
operationGroup.GetTechnology()     # → OlpCorePythonTechnology | None
operationGroup.GetUsedBaseProfile()
operationGroup.GetUsedToolProfile()
```

### DULPythonMotion

```python
motion.GetName()                   # → str (e.g., "P001")
motion.GetMotionType()             # → enum
motion.GetPosition()               # → DULPythonPosition (target)
motion.GetViaPosition()            # → DULPythonPosition (circular via point)
motion.IsLinearMotion()            # → bool
motion.IsCircularMotion()          # → bool
motion.IsReferenceMotion()         # → bool
motion.GetEventsBefore()           # → list[DULPythonEvent]
motion.GetEventsAfter()            # → list[DULPythonEvent]
```

### DULPythonPosition

```python
position.GetName()                 # → str (e.g., "P001")
position.GetXYZ()                  # → tuple[float,float,float] — in METERS
position.GetOrientation()          # → tuple[float,float,float] — in DEGREES (Rx,Ry,Rz)
position.GetMainJointValues()      # → list[tuple[DULPythonJoint, float]] — joint angle in DEGREES
position.GetExternalJointValues()  # → list[tuple[DULPythonJoint, float]] — ext axis values
position.GetTargetType()           # → TargetType enum (.Joint or .Cartesian)
position.GetConfig()               # → str (e.g., "S2")
position.GetTurn()                 # → str (e.g., "T10")
position.GetProcessType()          # → enum (.name = "Auxiliary", "Approach", "ProcessCurve", etc.)
```

### DULPythonEvent

```python
event.GetName()                    # → str (e.g., "Speed", "LogicPort", "SetResourcePort")
event.GetEventType()               # → EventType enum
event.GetGroupName()               # → str
event.GetInsertPosition()          # → str ("InsertBefore" or "InsertAfter")
event.GetAttributes()              # → list[attribute] — generic loop (RECOMMENDED)
event.GetMotions()                 # → list[DULPythonMotion] — event-owned motions
# Typed attribute getters (use for specific LogicPort subtypes only):
event.GetBoolAttribute(name, flag)     # → OlpCorePythonBoolAttribute
event.GetIntegerAttribute(name, flag)  # → OlpCorePythonIntegerAttribute
event.GetDoubleAttribute(name, flag)   # → OlpCorePythonDoubleAttribute
event.GetStringAttribute(name, flag)   # → OlpCorePythonStringAttribute
```

### DULPythonJoint

```python
joint.GetName()                    # → str (e.g., "A1")
joint.GetJointIndex()              # → int
joint.GetJointGroupIndex()         # → int
joint.GetDofNumber()               # → int
joint.GetPortName()                # → str
joint.GetJointRole()               # → str ("Main", "Rail", "Peripheral")
joint.GetUnit()                    # → str ("deg", "m")
joint.IsExternal()                 # → bool
joint.GetJointType()               # → JointKinematicType enum (.Prismatic or .Revolute)
```

### Frame Profiles

```python
# DULPythonToolProfile
toolProfile.GetName()              # → str
toolProfile.GetIndex()             # → int (frame number on controller)
toolProfile.GetXYZ()               # → tuple[float,float,float]
toolProfile.GetOrientation()       # → tuple[float,float,float]
toolProfile.GetToolType()          # → str ("OnRobot", etc.)

# DULPythonBaseProfile
baseProfile.GetName()              # → str
baseProfile.GetIndex()             # → int
baseProfile.GetXYZ()               # → tuple[float,float,float]
baseProfile.GetOrientation()       # → tuple[float,float,float]
baseProfile.GetReferenceProfile()  # → DULPythonBaseProfile | None
```

### Generic Attribute (from `GetAttributes()` loop)

```python
attribute.GetName()                # → str (e.g., "SignalName", "Value", "EventType")
attribute.GetValue()               # → any (bool, int, float, str — type depends on attribute)
```

---

## Enums

### EventType (from `event.GetEventType()`)

Values observed in debugger (name: int):

| Name | Value | Used For |
|------|-------|----------|
| `Approach` | 2 | Approach/retract motions |
| `Process` | 6 | Process start/stop |
| `LeadIn` | 7 | Lead-in motions |
| `LeadOut` | 8 | Lead-out motions |
| `GapBegin` | 9 | Gap detection start |
| `GapEnd` | 10 | Gap detection end |
| `BoolActor` | 11 | Boolean actor signals |
| `Speed` | 12 | Speed change |
| `Accuracy` | 13 | Accuracy change |
| `Dwell` | 16 | Wait/dwell time |
| `Acceleration` | 17 | Acceleration change |
| `Optimization` | 18 | Path optimization |
| `SetResourcePort` | 20 | Set resource port signal |
| `WaitForResourcePort` | ? | Wait for resource port signal |
| `LogicPort` | 22 | Controller logic port (has subtypes) |

### TargetType (from `position.GetTargetType()`)

| Name | Description |
|------|-------------|
| `Joint` | Joint-space target |
| `Cartesian` | Cartesian (world-space) target |

### JointKinematicType (from `joint.GetJointType()`)

| Name | Description |
|------|-------------|
| `Prismatic` | Linear axis (translational) — values in meters |
| `Revolute` | Rotational axis — values in degrees |

---

## Event Handling Patterns

### Event Dispatch (from `HandleBuildInEvents`)

Events are dispatched by `event.GetName()`:

```python
def HandleBuildInEvents(self, operator, event):
   if event.GetName() == 'Speed':
      self.SetSpeed(operator, event)
   elif event.GetName() == 'Accuracy':
      self.SetAccuracy(operator, event)
   elif event.GetName() == 'Acceleration':
      self.SetAcceleration(operator, event)
   elif event.GetName() == 'TextEvent':
      self.TextEvent(operator, event)
   elif event.GetName() == 'Dwell':
      self.DwellEvent(operator, event)
   elif event.GetName() == 'LogicPort':
      self.LogicPortEvent(operator, event)
   elif event.GetName() == 'SetResourcePort':
      self.LogicPortEvent(operator, event)
   elif event.GetName() == 'WaitForResourcePort':
      self.LogicPortEvent(operator, event)
```

### Signal Events — Two-Level Dispatch

Signal events require a **two-level dispatch**:

1. **Level 1 — EventType enum** (`event.GetEventType()`): Determines the high-level category
2. **Level 2 — eventSubType string** (from `EventType` attribute inside `LogicPort` events only): Determines the signal data type

```
EventType enum
├── SetResourcePort      → MULTI-SIGNAL container (loop to collect all signals)
├── WaitForResourcePort  → MULTI-SIGNAL container (loop to collect all signals)
└── LogicPort            → SINGLE signal, read eventSubType from 'EventType' attribute, then:
    ├── "CENE2SetSignal"         → bool set (GetBoolAttribute for SignalValue)
    ├── "CENE2SetSignalInt"      → int set (GetIntegerAttribute for SignalValue)
    ├── "CENE2SetSignalShortInt" → short int set (GetStringAttribute for SignalValue)
    ├── "CENE2SetSignalFloat"    → float set (GetDoubleAttribute for SignalValue)
    ├── "CENPyOlpSetBoolSignalEvent" → bool set (legacy, from generic loop)
    ├── "CENE2WaitForSignal"     → bool wait
    └── others...
```

#### CRITICAL: SetResourcePort / WaitForResourcePort are Multi-Signal Containers

A single `SetResourcePort` or `WaitForResourcePort` event can contain **multiple signals**.
The `SignalName`, `SignalAddress`, `SignalNumber`, `SignalValue` attributes repeat in groups:

```
SetResourcePort event attributes (example from tree dump):
  ResourceName = "Rampf_MSC+Halter_neu"
  ExactStop = False
  TriggerRelatedToStart = True
  TriggerDistance = 0.0
  TriggerTime = 0.0
  SignalName = "Frei"              ← Signal 1
  SignalAddress = "$OUT3113"
  SignalNumber = 3113
  SignalValue = True (Bool)
  SignalName = "GunNumberForState1" ← Signal 2
  SignalAddress = "$OUT2857"
  SignalNumber = 2857
  SignalValue = 2 (Int)            ← Mixed types within same event!
```

**Collecting multiple signals:**

```python
signals = []
currentSignal = {}
for attr in event.GetAttributes():
   name = attr.GetName()
   if name == 'SignalName':
      # Start of a new signal group — save previous if exists
      if currentSignal.get('SignalName'):
         signals.append(currentSignal)
      currentSignal = {'SignalName': attr.GetValue(), 'SignalAddress': '', 'SignalNumber': '', 'SignalValue': ''}
   elif name == 'SignalAddress':
      currentSignal['SignalAddress'] = attr.GetValue()
   elif name == 'SignalNumber':
      currentSignal['SignalNumber'] = str(attr.GetValue())
   elif name == 'SignalValue':
      currentSignal['SignalValue'] = str(attr.GetValue())
# Don't forget the last signal
if currentSignal.get('SignalName'):
   signals.append(currentSignal)
# Output one command per signal
for sig in signals:
   ...  # vendor-specific output per signal
```

#### Reading LogicPort Attributes — Single Signal

LogicPort events always contain a single signal. The simple scalar loop works:

```python
# For LogicPort only — single signal per event
for attribute in event.GetAttributes():
   name = attribute.GetName()
   if name == 'EventType':
      eventSubType = attribute.GetValue()
   elif name == 'SignalName':
      signalName = attribute.GetValue()
   elif name == 'SignalNumber':
      signalNumber = str(attribute.GetValue())
   elif name == 'SignalValue':
      signalValue = str(attribute.GetValue())
```

Typed getters (`event.GetBoolAttribute("SignalValue", True)`) are only needed inside LogicPort subtypes where the `SignalValue` data type varies (bool/int/float).

#### Event Name vs EventType Enum

Note: `event.GetName()` returns the UI event name (e.g., `"SetResourcePort"`, `"BuiltInEvent"`, `"LogicPort"`).
`event.GetEventType()` returns the `EventType` enum which is the reliable dispatch key.
Events with `GetName()` = `"BuiltInEvent"` can have `GetEventType()` = `EventType.SetResourcePort`.
Always dispatch on `GetEventType()`, not `GetName()`.

### Common Event Attribute Names

| Event Name | Attributes |
|------------|------------|
| `Speed` | `Value` (float), `PathType` ("Contour" or "PointToPoint") |
| `Accuracy` | `Value` (float), `PathType`, `Criteria` ("On"/"Off"/"Distance"/"JointDistance") |
| `Acceleration` | `Value` (float), `PathType` |
| `TextEvent` | `Text` (str), `IsComment` (bool) |
| `Dwell` | `Value` (float — seconds) |
| `LogicPort` | `EventType` (str — subtype), `SignalName`, `SignalAddress`, `SignalNumber` (int), `SignalValue` (varies) — **single signal** |
| `SetResourcePort` | `ResourceName`, `ExactStop` (bool), `TriggerRelatedToStart` (bool), `TriggerDistance` (float), `TriggerTime` (float), then **repeating groups** of: `SignalName`, `SignalAddress`, `SignalNumber` (int), `SignalValue` (bool/int/double) |
| `WaitForResourcePort` | `ResourceName`, then **repeating groups** of: `SignalName`, `SignalAddress`, `SignalNumber` (int), `SignalValue` (bool) |
| `SyncRobots` | `SyncMode` ("Handshake"), `SyncText` (str) |

---

## Position Output Pattern

### Unit Conversions

E2 provides positions in **meters** and **degrees**. Most robot controllers expect **millimeters**:

```python
xyz = position.GetXYZ()        # meters
angles = position.GetOrientation()  # degrees (Rx, Ry, Rz)

# Convert to mm for output:
x_mm = xyz[0] * 1000
y_mm = xyz[1] * 1000
z_mm = xyz[2] * 1000
```

### Cartesian vs Joint Target

```python
targetType = position.GetTargetType()
if targetType == TargetType.Joint:
   joints = position.GetMainJointValues()
   for joint_obj, value in joints:
      # value is in degrees for revolute, meters for prismatic
else:
   xyz = position.GetXYZ()      # meters
   angles = position.GetOrientation()  # degrees
   config = position.GetConfig()  # e.g., "S2"
   turn = position.GetTurn()      # e.g., "T10"
```

### External Axes

```python
externals = position.GetExternalJointValues()
externals.sort(key=lambda ext: ext[0].GetJointIndex())
for joint_obj, value in externals:
   if joint_obj.GetJointType() == JointKinematicType.Prismatic:
      value_mm = value * 1000  # convert m → mm
   else:
      value_deg = value  # already degrees
```

---

## File Output Pattern

### Buffer-Then-Write

Downloaders buffer all output into arrays, then write everything at the end:

```python
def __init__(self):
   self.Header = []
   self.Source = []
   self.Data = []
   self.Footer = []

def WriteOutputFile(self, operator):
   fileUtil = FileUtility()
   fileUtil.AppendTextArrayToFile(self.outputPath, self.Header)
   fileUtil.AppendTextArrayToFile(self.outputPath, self.Source)
   fileUtil.AppendTextArrayToFile(self.outputPath, self.Footer)

def CloseOutputFile(self, operator):
   operator.AddOutputFilePath(self.outputPath)  # REQUIRED — registers file with E2
```

### Required Imports

```python
import sys, inspect, os
sys.dont_write_bytecode = True
sys.path.append(str(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

from cenpylib import FileUtility
from cenpydownload import *
from cenpyolpcore import *
from centypes import *
```

### Class Registration

Every downloader must define `DOWNLOAD_CLASS_NAME` at module level:

```python
DOWNLOAD_CLASS_NAME = "MyDownloader"
class MyDownloader(Downloader):
   ...
```

---

## Common Mistakes

1. **Not handling multiple signals in SetResourcePort/WaitForResourcePort** — These events are MULTI-SIGNAL containers. Attributes repeat in groups of (`SignalName`, `SignalAddress`, `SignalNumber`, `SignalValue`). A simple scalar loop only captures the last signal. Collect into a list by detecting each new `SignalName`.

2. **Using typed getters instead of generic loop** — `event.GetBoolAttribute("SignalValue", True)` can crash if the attribute type is wrong. Use `GetAttributes()` loop first, then typed getters only for LogicPort subtypes where you know the exact type.

3. **Forgetting `operator.AddOutputFilePath()`** — Output files won't appear in E2 unless registered in `CloseOutputFile`.

4. **Wrong unit conversion** — E2 positions are in meters. Multiply by 1000 for millimeters. External prismatic axes are also in meters.

5. **Modifying E2 installation files** — Never touch `downloadStarter.py`, `downloader.py`, or anything in E2's `Lib/site-packages/`.

6. **Logger in wrong scope** — Logger must be a local variable: `logger = operator.GetLogOperator()`. It is NOT available in utility functions or class-level methods that don't receive `operator`.

7. **BoolAttribute.GetValue() returns Python `bool`, NOT a string** — `True == 'True'` evaluates to `False` in Python. Always use `str(attr.GetValue()) == 'True'` when comparing bool attribute values. This is the #1 silent bug in downloaders — no error, just wrong output.

8. **Emitting motion settings inline instead of buffered** — Most controllers need SPEED/ACCURACY/CP emitted as separate lines BEFORE the motion. Use a buffered pattern: store pending values from events, flush before each motion, only emit when value changes (deduplicate via `last*` tracking).

9. **Not read-ahead scanning eventsAfter** — Technology events (ArcOn, ArcOff, Accuracy Off) attached to a motion via `eventsAfter` affect how that motion should be output. Scan `motion.GetEventsAfter()` BEFORE outputting the motion to detect LWS/LWE/mode changes.

10. **`GetIndex()` returning large values** — Tool/Base profile indices > 128 mean "not mapped". Check and log an error.

11. **Debugging generated code before checking the OLP tree** — If you do not confirm the structure with `Simple_Python_Translator.py` or `TreeDumper.py`, you can spend hours fixing the wrong layer.

---

## Advanced Patterns (Lessons from Production Downloaders)

### Pattern: Buffered Motion Data (Pending → Flush)

Instead of emitting SPEED/ACCURACY inline with motions, buffer them and flush once before each motion:

```python
def __init__(self):
   self.pendingSpeed = None
   self.pendingAccel = None
   self.pendingAccuracy = None
   self.lastSpeed = None
   self.lastAccuracy = None

# Events set pending values:
def _handleSpeed(self, event):
   self.pendingSpeed = ...  # extract from event attributes

# Before each motion, flush:
def _flushPendingMotionData(self):
   if self.pendingSpeed is not None:
      if self.pendingSpeed != self.lastSpeed:
         self.Source.append('SPEED ' + self.pendingSpeed)
         self.lastSpeed = self.pendingSpeed
      self.pendingSpeed = None
   # Same for accuracy, acceleration, CP, etc.
```

**Benefits**: Deduplicates redundant output, enables conditional suppression (e.g., suppress SPEED during welding), maintains correct output order regardless of event arrival order.

### Pattern: Read-Ahead for Technology Events

Technology events (ArcOn, ArcOff) are attached as `eventsAfter` on a motion. You often need to know about them BEFORE outputting the motion (e.g., to decide motion type, suppress settings, or format the motion line differently):

```python
def HandleMotion(self, operator, motion):
   # Read-ahead: check what comes AFTER this motion
   hasArcOn = False
   hasArcOff = False
   for evt in motion.GetEventsAfter():
      if evt.GetName() == 'ArcOnEvent':
         hasArcOn = True
      elif evt.GetName() == 'ArcOffEvent':
         hasArcOff = True

   # Now output motion with full knowledge of context
   self._flushPendingMotionData()
   motionLine = self._buildMotionLine(motion, hasArcOn, hasArcOff)
   self.Source.append(motionLine)

   # THEN let HandleEvent fire for eventsAfter (lifecycle handles this)
```

### Pattern: Weld Section State Machine

For arc welding downloaders, track weld state to suppress/modify output:

```python
# State transitions:
# ArcOnEvent fires  → arcOnActive=True, arcOnIsFirstMotion=True
# Next HandleMotion → use arcOnIsFirstMotion for LWS line, then set False
# HandleMotion (after output, before eventsAfter) → if motion has ArcOff in eventsAfter: arcOnActive=False
# ArcOffEvent fires → arcOnActive already False, emit LWE line

# Suppression rules (vary by vendor):
# - SPEED: often suppressed during welding (welder controls speed)
# - ACCURACY: often suppressed during welding (continuous path assumed)
# - CP: may be forced ON during welding, OFF otherwise
```

### Pattern: Euler Conversion

E2 stores orientations in `Euler_XYZs` (static XYZ). Convert to vendor convention:

```python
from cenpymath.Euler.Converter import ConvertEuler
from centypes import Euler_XYZs, Euler_ZYZr  # or vendor's convention

rx, ry, rz = position.GetOrientation()  # degrees, Euler_XYZs
a, b, c = ConvertEuler(rx, ry, rz, Euler_XYZs, Euler_ZYZr)
```

Common vendor conventions:
- KUKA: `Euler_ZYZr` (A, B, C)
- ABB: Quaternion (convert separately)
- FANUC: `Euler_XYZr` (W, P, R)
- Kawasaki: `Euler_ZYZr` (O, A, T)

### Pattern: Numeric Formatting Without Trailing Zeros

Many controllers require clean numeric output (no `.0` on integers):

```python
def _fmtRound1(self, value):
   """Round to 1 decimal, strip trailing .0"""
   r = round(value, 1)
   return str(int(r)) if r == int(r) else str(r)
   # 0.0 → "0", 4.6 → "4.6", 100.0 → "100"
```

### Pattern: Main/Subprogram Handling

The E2 download starter supports three subprogram strategies controlled by two overridable methods on your `Downloader` subclass:

| `OutputSubprogramInSeparateFiles()` | `HandleSubprogramInLoop()` | Behavior |
|-------------------------------------|---------------------------|----------|
| `True` (base default) | — | Each subprogram gets its own `HandleProgram()` call → separate output file |
| `False` | `False` | After main program loop, subprograms are appended via `LoopProgram()` in the same file |
| `False` | `True` | Subprograms are traversed inline during `GetGroupsAndSubprograms()` iteration |

**Framework traversal flow** (from `downloadStarter.py`):

```
DownloadActiveProgram()
└─ HandleProgram(mainProgram)
   ├─ OutputHeader()
   ├─ LoopProgram(mainProgram)
   │  ├─ ProgramStart()
   │  ├─ for each in program.GetGroupsAndSubprograms():
   │  │  ├─ if OperationGroup → OperationGroupStart/Operations/OperationGroupEnd
   │  │  └─ if Subprogram → SubprogramStart() / [inline LoopProgram if HandleInLoop] / SubProgramEnd()
   │  └─ ProgramEnd()
   ├─ [if !SeparateFiles && !HandleInLoop: loop program.GetSubprograms() → LoopProgram(each)]
   ├─ CreateOutputFile → WriteOutputFile → CloseOutputFile
   └─ [if SeparateFiles: loop program.GetSubprograms() → HandleProgram(each)]
```

**Key APIs:**
- `program.IsMainProgram()` → `bool` — True for the top-level program
- `program.GetSubprograms()` → `list[DULPythonSubprogram]` — subprogram references
- `program.GetGroupsAndSubprograms()` → `list` — interleaved operation groups and subprogram calls (cast with `CastToOperationGroup` / `CastToSubprogram`)
- `program.GetOperationGroups()` → `list[DULPythonOperationGroup]` — operation groups only (no subprograms)
- `subprogram.GetCalledProgram()` → `DULPythonProgram` — the program being called
- `subprogram.GetName()` → `str` — name of the subprogram

**Detecting a "container" main program** (one that only holds CALL statements):

```python
def ProgramStart(self, operator, program):
   self.isContainerProgram = program.IsMainProgram() and len(program.GetSubprograms()) > 0
```

**Emitting CALL statements** in `SubprogramStart`:

```python
def SubprogramStart(self, operator, subprogram):
   self.Source.append('CALL ' + subprogram.GetName())
```

### Pattern: Per-Program State Reset

When `OutputSubprogramInSeparateFiles` is True, `ProgramStart` is called once per program (main + each sub). All per-program state must be reset there — NOT in `__init__` or `OutputHeader`:

```python
def ProgramStart(self, operator, program):
   self.programName = program.GetName()
   # Reset output buffers
   self.TransBlock = []
   self.JointsBlock = []
   self.Source = []  # or keep appending if single-file
   # Reset all flags
   self.headerEmitted = False
   self.arcOnActive = False
   self.pendingSpeed = None
   self.lastSpeed = None
   # ... reset all per-program state
```

`OutputHeader` should only read **controller-level** data (output directory, motion profiles, resource attributes) that stays constant across programs.

### Pattern: Subroutine Deduplication

Hard-coded subroutines (e.g., touch sensing helpers, utility programs) that are shared across subprograms should be emitted **once in the main program file**, not in every subprogram.

**Strategy:** Pre-scan the subprogram tree in `ProgramStart` of the main program, then emit subroutines in `ProgramEnd` only for the main:

```python
def ProgramStart(self, operator, program):
   self._treeNeedsSubroutines = False
   if self.isContainerProgram:
      self._treeNeedsSubroutines = self._scanTreeForFeature(program)

def ProgramEnd(self, operator, program):
   self.Source.append('.END')
   # Only in main program file
   if self.isContainerProgram:
      if self._treeNeedsSubroutines:
         self._emitHelperSubroutines()
   elif program.IsMainProgram() and self.hasFeatureAtRuntime:
      self._emitHelperSubroutines()  # standalone (no subs)

def _scanTreeForFeature(self, program):
   for sub in program.GetSubprograms():
      calledProg = sub.GetCalledProgram()
      for opGroup in calledProg.GetOperationGroups():
         for op in opGroup.GetOperations():
            if self._operationNeedsFeature(op):
               return True
   return False
```

---

## Debugging

### Automated download loops bypass AutoExecute

`controller.DownloadProgramByName()` does **not** run the `AuxiliaryCommands/AutoExecute`
pipeline that the UI Download button triggers. A dev-loop harness that calls it directly
therefore exercises a different code path from production, and a passing golden comparison
proves nothing about the real one.

If the technology does program-wide work before download (for example writing planner results
into the tree in `PrevProgramDownload.py`), the harness must import and invoke that hook
explicitly before each `DownloadProgramByName` call.

Symptom: attributes the technology should have written are still at their defaults after an
automated download, but correct after a manual UI download.

### Attaching Debugger
- VS Code: Use the `debugpy attach` launch config (port 5254) while E2 is running
- Set breakpoints in your downloader `.py` file
- Trigger download in E2 — debugger will catch

### Using Simple_Python_Translator
Trigger a download using the `Simple_Python_Translator.py` downloader to get a complete `.txt` dump of the OLP tree. This shows:
- All programs, operation groups, operations
- All motions with position data
- All events with their attributes and types
- All controller/resource configuration

This is the fastest way to understand what data is available for your downloader.
