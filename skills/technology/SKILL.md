---
name: technology
description: Guide for customizing FASTSUITE E2 Technology UI — attributes, tabs, events, workmethods. Use when working on files under Technologies/.
applyTo: Technologies/**/*.py
---

# E2 Technology Customization Skill

## Required references

Read the focused reference that matches the task before editing implementation files:

- Attribute creation, `Settings.xml`, dynamic visibility, or NLS: [`references/attributes-ui-localization.md`](references/attributes-ui-localization.md)
- Event registration, rule binding, event attributes, or `PostCompute`: [`references/events-rules-compute.md`](references/events-rules-compute.md)
- Process-geometry importer, workmethod sync, or AutoExecute: [`references/process-geometry-import.md`](references/process-geometry-import.md)

Use [`docs/technology/`](../../docs/technology/) for the explanatory guides and [`examples/technology/`](../../examples/technology/) for focused overlays. The examples do not replace the selected R2026.1 technology template.

## What is a Technology?

A Technology in FASTSUITE E2 defines the process-specific behavior for a robot application (Arc Welding, Spray Painting, Handling, etc.). Technology customization scripts control:
- **Attributes**: Custom fields shown in the E2 UI (process parameters, settings)
- **Tabs**: UI tab layout in the technology editor
- **Events**: Technology-specific motion events (ArcOn/Off, GunOn/Off, etc.)
- **Workmethods**: Processing strategies and parameter sets

## Start Here: Ownership First

Before editing downloader or uploader code, decide whether the behavior is actually owned by the technology layer.

Use the technology layer when the behavior involves:

- Workmethod-selected process behavior
- Generated approach or retract motions
- Virtual or computed process points
- Technology event registration and event rules
- Upload-time or compute-time regeneration of helper motions

Practical rule:

- If the tree dump shows the event or helper motions only after technology compute, the technology layer owns them.
- If an uploader creates the expected event structure but E2 strips or regenerates it on re-download, the technology layer usually owns the final shape.

## API Authority

- Use `typings/` as the authority when the needed API surface actually exists there.
- Use the Obsidian vault as the primary authority for Technology and Workmethod operator APIs, callback lifecycle, and behavioral semantics, because technology stubs are still incomplete.
- If both sources mention the same concept, prefer `typings/` for signatures and Obsidian for timing or behavior.
- When they still conflict, prefer real script behavior and tree-dump or round-trip evidence over either document.

Short rule: for Technology work, Obsidian often has higher authority than `typings/` unless the exact operator surface is stubbed locally.

## Arc Welding Ownership Guide

For Arc Welding, many behaviors that look like normal motion or event data are actually technology-managed.

Typical owners:

- `DefaultUploadMethod.py`: registers Python technology events and binds them to event rules for upload-side reconstruction
- `TouchSensingWorkMethod.py` / `StitchWeldingWorkMethod.py`: workmethod attributes, event availability, and operation-level process behavior
- `TouchSensingEvent.py`: compute-time generation of sensing helper motions and speed or accuracy events
- `ApproachArcWelding*.py` / `RetractArcWelding*.py`: approach and retract event behavior

Session-derived guidance:

- Seam welding can round-trip with correct Cartesian targets and user events even when E2 regenerates approach or retract technology events.
- Touch sensing is frequently technology-managed end-to-end: the visible reference motion may survive while `TouchSensingEvent`, helper motions, or insert-side built-ins are recomputed or stripped.
- If re-downloaded touch operations lose nested sensing motions, do not assume uploader failure first; inspect the technology event and workmethod scripts.

## Folder Structure

Technology scripts follow this layout:
```
Technologies/<TechName>/<Vendor>/Standard/Scripts/
```

Common callback scripts:
- `PostTechInitAttributes.py` — called once when technology is initialized; set up custom attributes
- `PostWmSyncPgAttributes.py` — called when workmethod syncs to program; sync attribute values

Arc Welding scripts you will often need together:

- `ArcWeldingTechnology.py` — technology-wide attributes and initialization
- `DefaultUploadMethod.py` — upload registration, event rules, active event selection
- `TouchSensingWorkMethod.py` / `StitchWeldingWorkMethod.py` — workmethod attributes and event availability
- `TouchSensingEvent.py` — compute-time generation of helper motions and events

## API Reference

- **Primary context**: Obsidian vault `10_API_Reference/Technology/` (via `obsidian-e2` MCP)
- **Core objects**: Obsidian vault `10_API_Reference/OlpCore/` (via `obsidian-e2` MCP)

## Investigation Workflow

1. Capture the OLP structure with `community/OLPTranslators/Simple_Python_Translator.py` and, if needed, `OLPTranslators/TreeDumper.py`.
2. Identify whether the missing or regenerated structure belongs to a technology event, a workmethod, or a downloader/uploader callback.
3. Read the nearest technology script that owns the behavior.
4. Make the smallest change in that owner.
5. Re-run the same download or upload round-trip check.

For Arc Welding touch-sensing issues, inspect in this order:

1. `DefaultUploadMethod.py` for event registration and rule binding
2. `TouchSensingWorkMethod.py` for workmethod-owned attributes and process behavior
3. `TouchSensingEvent.py` for `PostCompute` logic that creates helper motions and speed or accuracy events
4. Only then return to downloader or uploader code if the tree shows technology is not the owner

## Key Rules

- Use the callback's established logger accessor; Technology scripts in this repository normally use `logger = Operator.GetLoggerOperator()`.
- For enums/literals, use the R2026.1 literal or enum getter established by `typings/`, Obsidian, and the nearest production script; do not treat a literal as a string.
- Use `GetAttributeByName()` when changing an existing attribute's visibility. During initialization, calling `SetVisibility()` on the object returned by `Add*` is valid when the reference template uses that pattern.
- Attribute use levels are bitmasks. Compose intentional flags with `|` and verify the resulting scope in a tree dump.
- Keep Python attribute names, `Settings.xml` `Attribute/@Name` values, and XAML NLS keys exact and case-sensitive.
- Never modify E2 core technology definitions

## Common Ownership Patterns

### Workmethod scripts own process semantics

Use `PostWmInitAttributes`, `PostWmInitEvents`, `PostWmInitRules`, and `PostWmSyncPgAttributes` when the behavior is selected by process method rather than by generic motion output.

### Event scripts own computed helper geometry

When an event script has `PostCompute`, treat it as the owner of generated motions, derived points, and technology-inserted speed or accuracy events.

### Upload method scripts own event registration

If an event is missing from a rule or the wrong event is active for a given rule, check the upload or workmethod registration script before editing parser logic.

## Arc Welding Touch-Sensing Pattern

`DefaultUploadMethod.py` typically does three important things:

1. registers technology event Python files
2. removes or replaces default rule bindings
3. activates the technology event for the relevant rule such as `ProcessPointRule`

`TouchSensingEvent.py` then computes the real helper motions in `PostCompute`, typically by:

1. reading workmethod attributes such as sensing length, overtravel, and motion type
2. asking the touch-sensing operator for reference, start, collision, and end points
3. generating helper motions like approach, collision, and retract moves
4. adding technology events like speed and accuracy around those generated points

This means a generic uploader can often reconstruct the visible event shell but still not control the final helper-motion structure. That final shape belongs to technology compute.

## Common Patterns

### Creating Attributes
```python
def PostTechInitAttributes(Operator: CENPyOlpTech_AttribInitOperator):
   creator = Operator.GetAttribCreator()
   use_level = USER_ATTRIBUTE | PROCESS_ATTRIBUTE | GLOBAL_ATTRIBUTE
   creator.AddInteger("MyIntAttribute", 0, -100, 100,
                      use_level, "MyIntAttribute")
```

### Reading Attributes
```python
getter = Operator.GetAttribGetter()
enabled = getter.GetBool("EnableFeature")
speed = getter.GetDouble("Speed")

# Retrieve the attribute object when object-level behavior is needed.
speed_attribute = getter.GetAttributeByName("Speed")
speed_attribute.SetVisibility(enabled)
```

## Common Mistakes

1. **Patching downloader or uploader code when the behavior is technology-owned** — decide ownership first.
2. **Ignoring `PostCompute` in event scripts** — generated helper motions often come from event compute, not from the imported structure.
3. **Changing event parsing without checking registration rules** — the wrong active event on a rule can make a correct parser look broken.
4. **Treating hidden operation attributes as user-authored state** — some flags are technology-computed and may disappear on round-trip.
5. **Using the wrong attribute getter for enums** — enum-like attributes are often literals, not strings.
6. **Installing both ownership variants of the same event** — choose technology-level or workmethod-level registration, never both for the same deployment.
7. **Assuming an AutoExecute filename is enough** — confirm the selected template's integration and make repeated execution behavior explicit.
8. **Promoting static review to runtime fact** — callback timing, visibility, generated motions, and inserted events require R2026.1 runtime/tree-dump evidence.

Use the `obsidian-e2` MCP server to look up `Technology Callback Lifecycle` and `Workmethod Callback Lifecycle` for the full API reference.
