---
name: uploader
description: Guide for creating and modifying FASTSUITE E2 OLP uploaders (robot program importers). Use when working on uploader files under OLPTranslators/.
applyTo: OLPTranslators/**/*ul*.py
---

# E2 OLP Uploader Skill

## What is an Uploader?

An uploader imports vendor-specific robot programs back into the FASTSUITE E2 OLP environment. It parses robot code files and creates the corresponding E2 program structure (operations, motions, events, positions).

## Start Here: Tree Dumper First

Before changing uploader reconstruction logic, inspect the OLP structure you are trying to recreate.

Default workflow:

1. Download the source program with `community/OLPTranslators/Simple_Python_Translator.py` for a human-readable `.txt` tree dump.
2. If the work is round-trip sensitive, also download with `OLPTranslators/TreeDumper.py` to get a structured YAML baseline.
3. Upload your reconstructed program.
4. Re-download the uploaded result and compare it with the original dump.
5. Only patch the uploader after the diff shows which part of the structure was lost, normalized, or regenerated.

Use this to answer three different questions early:

- Did the parser fail to reconstruct the expected OLP object graph?
- Did E2 accept the graph but normalize part of it during upload validation?
- Is the missing behavior actually owned by technology callbacks rather than uploader code?

## API Authority

- Use `typings/cenpyupload`, `typings/cenpydownload`, and `typings/cenpyolpcore` as the authority for upload object creation methods, writable object methods, enum members, and signatures.
- Use the Obsidian vault as the authority for lifecycle order, upload semantics, normalization patterns, and behavior that is not obvious from types alone.
- If the vault text disagrees with stubbed class or method signatures, trust `typings/` first and then confirm with a round-trip experiment.

Short rule: signatures from `typings/`, behavior from Obsidian, round-trip diffs break ties.

## Reference Files

- `OLPTranslators/TreeDumper_ul.py` — structured YAML uploader used for round-trip experiments and generic OLP reconstruction
- `OLPTranslators/TreeDumper.py` — structured YAML downloader used as the matching baseline format
- `community/OLPTranslators/Simple_Python_Translator_ul.py` — minimal text-tree uploader reference
- `community/OLPTranslators/PRIMA/PRIMA_XML_ul.py` — reference uploader with technology-aware reference motion patterns
- `typings/cenpyupload/uploadStarter.py` — actual upload lifecycle entrypoint
- `typings/cenpyupload/stubs/ULPythonUploadOperator.pyi` — object creation surface and operator methods
- Obsidian vault `10_API_Reference/Upload/` — upload API reference
- Obsidian vault `10_API_Reference/OlpCore/` — shared core object model and attributes

## Upload Lifecycle

The upload starter is much simpler than the download traversal. It instantiates your uploader once, calls `Initialize`, parses each selected source file through `ParseFile`, then calls `Finalize`.

```python
def __init__(self) -> None:
def Initialize(self, operator: ULPythonUploadOperator):
def ParseFile(self, operator: ULPythonUploadOperator, fileObject):
def Finalize(self, operator: ULPythonUploadOperator):
```

Framework flow from `uploadStarter.py`:

```text
UploadProgramFromFile(operator)
1. instantiate globals()[UPLOAD_CLASS_NAME]
2. uploader.Initialize(operator)
3. for each source file:
	- open file
	- uploader.ParseFile(operator, fileObject)
4. uploader.Finalize(operator)
```

Practical consequence: all program creation, parsing, object wiring, and validation logging happen inside `ParseFile` and your helper methods.

## Core API Surface

- **Primary context**: Obsidian vault `10_API_Reference/Upload/` (via `obsidian-e2` MCP)
- **Core objects**: Obsidian vault `10_API_Reference/OlpCore/` (via `obsidian-e2` MCP)

### ULPythonUploadOperator

```python
operator.GetSourceFiles()                 # list[str]
operator.GetController()                  # ULPythonController
operator.GetLogOperator()                 # logger
operator.GetAttributeSetterOperator()     # attribute factory
operator.CreateEmptyProgram()
operator.CreateEmptySubprogram()
operator.CreateEmptyOperationGroup()
operator.CreateEmptyOperation()
operator.CreateEmptyMotion()
operator.CreateEmptyPosition()
operator.CreateEmptyEvent()
operator.CreateEmptyToolProfile()
operator.CreateEmptyBaseProfile()
```

### Common writable objects

```python
program.SetName(...)
program.SetIsMainProgram(...)
program.SetUsedBaseProfile(...)
program.SetUsedToolProfile(...)

group.SetName(...)
group.SetUsedBaseProfile(...)
group.SetUsedToolProfile(...)

operation.SetName(...)
operation.SetUsedBaseProfile(...)
operation.SetUsedToolProfile(...)

motion.SetName(...)
motion.SetMotionType(...)
motion.SetPosition(...)
motion.SetViaPosition(...)
motion.SetEventsBefore(...)
motion.SetEventsAfter(...)
motion.AddEventBefore(...)
motion.AddEventAfter(...)

position.SetName(...)
position.SetProcessType(...)
position.SetTargetType(...)
position.SetXYZ(...)
position.SetOrientation(...)
position.SetConfig(...)
position.SetTurn(...)
position.SetExplicitMainJointValues(...)
position.SetExplicitExternalJointValues(...)

event.SetName(...)
event.SetInsertPosition(...)
event.AddAttribute(...)
event.AddMotion(...)
```

## Reconstruction Pattern

Build the graph in the same containment order E2 expects:

1. program
2. operation group
3. operation
4. motion
5. position / via position
6. events before / after
7. event-owned nested motions

Minimal pattern:

```python
program = operator.CreateEmptyProgram()
group = operator.CreateEmptyOperationGroup()
operation = operator.CreateEmptyOperation()
motion = operator.CreateEmptyMotion()
position = operator.CreateEmptyPosition()

motion.SetPosition(position)
operation.AddMotion(motion)
group.AddOperation(operation)
program.AddOperationGroup(group)
```

Keep helpers narrow: one builder for each object kind, each returning a fully populated object or `None`.

## Critical Patterns

### Strong references to created objects

pybind11-backed E2 objects can be released on the Python side while E2 still holds raw or weak references. Keep strong references to every created object for the lifetime of the upload run.

```python
def __init__(self):
	self._createdObjects = []

motion = operator.CreateEmptyMotion()
self._createdObjects.append(motion)
```

If you see unexplained null behavior, disappearing children, or intermittent crashes, check object lifetime first.

### Every uploaded motion needs a position object

Do not create a motion without assigning a position. This includes reference motions. If the parsed source lacks full target data, create an empty position object and set at least the process type intentionally.

### Profile type split matters

In practice, `ULPythonProgram` and `ULPythonOperationGroup` often need UL profile wrappers created through the upload operator, while operations may accept the controller's plain cached profiles. If a profile assignment works at one level but fails at another, check whether that layer expects UL wrappers.

### Round-trip diff before deeper theory

When behavior is unclear, compare:

1. original tree dump
2. uploaded program in E2
3. re-downloaded tree dump

This separates parser defects from E2 normalization.

## Round-Trip Investigation Workflow

### Use `Simple_Python_Translator.py` when

- You need a quick human-readable tree dump
- You are confirming names, callback-visible order, or attribute presence
- You are checking whether the uploader recreated the basic object graph at all

### Use `TreeDumper.py` and `TreeDumper_ul.py` when

- You need structured original vs re-download comparison
- You are building a generic importer / exporter pair
- You need stable diffs for positions, event lists, and nested motions
- You are testing whether E2 keeps, strips, or regenerates technology-managed data

### Ownership check: uploader vs technology

If the uploader creates the object graph you expect but E2 strips or reshapes it during upload, the uploader may not be the controlling layer.

Typical ownership split:

- Uploader: parser logic, object creation, attribute mapping, profile assignment, target reconstruction
- Technology: workmethod-owned events, generated approach/retract motions, virtual sensing helpers, controller-specific validation of technology data

Session-derived rule of thumb:

- Seam operations can round-trip well even when E2 regenerates approach/retract technology events.
- Touch-sensing operations may lose `TouchSensingEvent`, `BuiltInEvent`, or nested sensing motions during upload because those are technology-managed, not generic uploader-owned.

## Positions and Motions

### Set process type and target type explicitly

Do not rely on defaults. Uploaded positions should always receive an explicit `ProcessType` and `TargetType`.

### Cartesian targets

E2 expects XYZ in meters and orientation in degrees:

```python
position.SetXYZ((x_m, y_m, z_m))
position.SetOrientation((rx_deg, ry_deg, rz_deg))
position.SetConfig(config_string)
position.SetTurn(turn_string)
```

### Joint targets and external axes

Resolve joints from the active controller and pass explicit `(jointObject, value)` pairs for main and external axes.

### Circular motions

If the motion is circular, create and assign the via position as a separate `ULPythonPosition`.

## Events and Attributes

### Insert position matters

Set `InsertBefore` or `InsertAfter` intentionally. Many downstream behaviors depend on whether the event is attached before or after the motion.

### Build attributes through the attribute setter operator

Use the attribute setter returned by `operator.GetAttributeSetterOperator()` to create typed writable attributes, then attach them to programs, operations, events, or positions.

### Nested motions are valid but may not survive round-trip

Approach/retract and sensing events can own motions. Uploading them literally is valid API usage, but E2 technology may strip and regenerate them.

## Common Mistakes

1. **Not keeping strong references** — created UL objects can disappear or become invalid if Python releases them too early.
2. **Creating motions without positions** — reference motions still need a position object.
3. **Assuming upload preserves all event structure** — technology-managed events may be stripped even when your uploader builds them correctly.
4. **Using the wrong profile object type at the wrong level** — program and operation-group profile assignment may require UL wrappers.
5. **Debugging parser text without comparing OLP trees** — always compare original and re-downloaded trees before rewriting reconstruction logic.
6. **Treating empty YAML / parsed blocks as empty lists automatically** — missing blocks often parse as `None`; normalize with `or []` before taking lengths or iterating.
7. **Forgetting circular via positions** — circular motions need both main position and via position.
8. **Adding fallback events without checking controller mapping** — some built-in events may upload but later be skipped by controller validation.

## Key Rules

- Never modify `uploadStarter.py`, `uploader.py` (E2 installation files)
- Never modify E2 site-packages (`cenpydownload`, `cenpyolpcore`, `cenpylib`, `cenpyupload`)
- Logger is always a local variable: `logger = operator.GetLogOperator()`
- Use round-trip comparison to identify the owning layer before patching
- Treat `TreeDumper.py` / `TreeDumper_ul.py` as the preferred structured harness for uploader experiments

## Debugging

- Log one level above the failure surface: file, program, operation, motion, event
- Count events before and after normalization when testing upload acceptance
- When E2 accepts the upload but the re-download differs, assume normalization first and parser bugs second
- Use the `obsidian-e2` MCP server to look up `Upload Callback Lifecycle` and the specific UL object types when method behavior is unclear
