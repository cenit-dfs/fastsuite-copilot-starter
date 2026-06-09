# Plan: YAML Tree Dumper + Technology Customization

Status: **Draft**
Date: 2026-06-08

---

## Motivation

The `community/OLPTranslators/Simple_Python_Translator.py` generates text-based OLP tree dumps. These dumps are essential for:
- **Downloader development**: understanding what data E2 provides at each lifecycle level
- **Technology work**: seeing which attributes/events a technology defines per vendor
- **Agent-assisted coding**: parsing structured data to auto-generate downloader logic

Current limitations:
1. **~45 of ~140 API methods used** — misses resource ports, joint kinematic types, subprogram context, inherited attributes, technology version/UUID, motion/position attributes
2. **Text format is regex-dependent** — hard for agents to parse reliably
3. **No dedicated YAML output** — agents need structured data, not indentation-dependent text
4. **Reference baselines exist for only 3 of 13+ technology/vendor combos**

## Phase 1: YAML Tree Dumper Translator

### Goal
New translator `OLPTranslators/TreeDumper/TreeDumper.py` that outputs `.yaml` files with **complete** OLP tree data.

### Output Structure (target)

```yaml
meta:
  translator: TreeDumper
  translator_version: "1.0"
  language: en-US

controller:
  name: "E0x_with_TrafoUnit"
  model: "E0x_with_TrafoUnit"
  series: "E-Series"
  manufacturer: "Kawasaki"
  type: "Motion"  # ControllerTypes enum
  active_program: "PG06_BASIC"

  joints:
    - name: "D1"
      group_index: 0
      dof_number: 1
      joint_index: 1
      port_name: "D1"
      role: "Main"  # JointConstellationRole
      unit: "deg"
      kinematic_type: "Revolute"  # NEW: JointKinematicType
      is_external: false

  tool_profiles:
    - name: "TOOL1"
      index: ~  # null = notDefined
      tool_type: "OnRobot"
      is_vision_frame: false  # NEW
      xyz_m: [0.0022, 0.141714, 0.431714]
      orientation_deg: [-45.0, -0.000274, -0.000327]

  base_profiles:
    - name: "World"
      index: ~
      reference_profile: ~
      xyz_m: [0.0, 0.0, 0.0]
      orientation_deg: [0.0, 0.0, 0.0]

  accuracy_profiles:
    - name: "Default"
      criteria: "Distance"
      fly_by: "Off"
      value: 0.0
      unit: "m"

  motion_profiles:
    - name: "CP_SP_0.50_ACC100.00%"
      basis: "Absolute"
      type: "Contour"
      speed: { value: 0.5, unit: "" }
      acceleration: { value: 100.0, unit: "%" }

  attributes: []  # controller-level

  resources:
    - name: "BA06L"
      item_type: "Production"
      item_sub_type: "MachineRobot"
      manufacturer: "Kawasaki"
      model: "BA06L"
      series: "BA-Series"
      supported_configurations: [...]  # NEW
      supported_turns: [...]            # NEW
      ports:                            # NEW
        - name: "DO_1"
          comment: "Digital output 1"
          data_type: "Bool"
          direction: "Output"
      attributes:
        - { name: "CENOlpDataOutputStyle", value: "Implicit", type: "String", ... }

programs:
  - name: "PG06_BASIC"
    is_main: true
    base_profile: "B0"
    tool_profile: "TOOL1"
    attributes: [...]

    subprograms:              # NEW
      - name: "SUB1"
        calling_program: "PG06_BASIC"
        called_program: "SUB1_body"

    operation_groups:
      - name: "GRP001"
        technology:
          name: "ArcWeldingTechnology"
          version: 1          # NEW
          uuid: "..."         # NEW
        base_profile: "B0"
        tool_profile: "TOOL1"
        attributes: [...]

        operations:
          - name: "WG1_Seam1"
            type: "Normal"
            base_profile: "B0"
            tool_profile: "TOOL1"
            attributes: [...]

            motions:
              - name: "PG06_BASIC_P0001"
                motion_type: "PTP"
                is_ptp: true
                is_linear: false
                is_circular: false
                is_reference: false
                attributes: []       # NEW

                events_before: [...]
                events_after: [...]

                position:
                  name: "PG06_BASIC_P0001"
                  process_type: "Auxiliary"
                  target_type: "CartesianAndJoint"
                  attributes: []     # NEW
                  xyz_m: [x, y, z]
                  orientation_deg: [rx, ry, rz]
                  config: "..."
                  turn: "..."
                  main_joints:
                    - { name: "D1", value: 45.0 }
                  external_joints:
                    - { name: "JT7", value: 0.0 }

                # via_position only for circular
                via_position: ~

summary:                         # NEW — at bottom for streaming
  program_count: 1
  operation_group_count: 1
  operation_count: 2
  motion_count: 10
  event_count: 15
  event_types_found: ["Approach", "Retract", "ArcOn", "ArcOff", "Speed", "Accuracy", "Tool"]
  technologies_found: ["ArcWeldingTechnology"]
  attribute_count:
    controller: 0
    program: 15
    group: 3
    operation: 8
    event: 45
    motion: 0
    position: 0
    resource: 2
```

### API Coverage Additions (vs Simple_Python_Translator)

| Class | Method | Current | TreeDumper |
|---|---|---|---|
| DULPythonJoint | `GetJointType()` | - | Revolute / Prismatic |
| DULPythonToolProfile | `IsVisionFrame()` | - | bool |
| DULPythonSubprogram | `GetCallingProgram()` | - | program name |
| DULPythonSubprogram | `GetCalledProgram()` | - | program name |
| DULPythonMotion | `IsPtPMotion()` | - | bool |
| DULPythonMotion | `GetAttributes()` | - | attribute list |
| DULPythonPosition | `GetAttributes()` | - | attribute list |
| OlpCorePythonResource | `GetSupportedConfigurations()` | - | string list |
| OlpCorePythonResource | `GetSupportedTurns()` | - | string list |
| OlpCorePythonResource | `GetAllPorts()` | - | port list |
| OlpCorePythonTechnology | `GetVersion()` | - | int |
| OlpCorePythonTechnology | `GetUuid()` | - | string |
| OlpCorePythonProgramComponent | `GetInheritedAttributes()` | - | deferred (v2) |

### Attribute Output Format

All attribute types normalized to a consistent dict:

```yaml
- name: "WeldConditionMode"
  type: "Literal"         # Bool | Int | Double | String | IntArray | DoubleArray | StringArray | Literal
  value: "JobMode"
  values: ["JobMode", "ManualMode", "None"]  # Literal only
  index: 0                                    # Literal only
  min: ~                                      # Int/Double only
  max: ~
  step_size: ~
  group_name: ""
  read_only: false
  value_unit_type: "Standard"
  olp_property: ["UserAttribute", "ProcessAttribute", "GlobalAttribute"]
```

Key change: `olp_property` as a list instead of pipe-delimited string — much easier to parse.

### Implementation Notes

- Python `yaml` module is NOT available in E2's bundled Python. Use manual YAML emitter (string building) — no external dependencies.
- File extension: `.yaml`
- One file per program (follows E2 convention)
- Numbers: floats always with 6 decimal places for positions, raw for integers
- Units: keep meters/degrees as-is (consumers convert), annotate field names with `_m` and `_deg` suffixes
- `notDefined` ProfileIndex → YAML `null` (`~`)
- No timestamps by default (deterministic for golden files)

### Tasks

| # | Task | Effort |
|---|---|---|
| 1.1 | Scaffold `OLPTranslators/TreeDumper/TreeDumper.py` with all callbacks | S |
| 1.2 | Implement YAML string builder (indent-aware, type-safe) | M |
| 1.3 | Implement `OutputHeader` — controller, joints, profiles, resources, ports | M |
| 1.4 | Implement `ProgramStart/End` — program attributes, base/tool profiles | S |
| 1.5 | Implement `OperationGroupStart/End` — technology, attributes | S |
| 1.6 | Implement `OperationStart/End` — attributes | S |
| 1.7 | Implement `HandleMotion` — position data, motion/position attributes | M |
| 1.8 | Implement `HandleEvent` — event attributes, nested motions | M |
| 1.9 | Implement `SubprogramStart/End` — calling/called program context | S |
| 1.10 | Implement summary section (emitted in `CloseOutputFile`) | S |
| 1.11 | Test with Kawasaki ArcWelding scenario, validate YAML is parseable | M |

---

## Phase 2: Technology Baselines

### Goal
Generate reference `.yaml` dumps for every technology/vendor combination that has a scenario `.cendoc`.

### Current Baseline Coverage

| Technology | Vendor | Scenario exists | Reference dump exists |
|---|---|---|---|
| ArcWelding | KAWASAKI | `.cendoc` in `scenarios/` | text dumps for 7 programs |
| ArcWelding | ABB | `.cendoc` in `scenarios/` | text dumps for 4 programs |
| LaserCutting | TRUMPF | `.cendoc` in `scenarios/` | text dump for 1 program |
| ArcWelding | Standard | - | - |
| ArcWelding | CLOOS | - | - |
| ArcWelding | DAIHEN | - | - |
| ArcWelding | FANUC | - | - |
| ArcWelding | KUKA | - | - |
| ArcWelding | Motoman | - | - |
| ArcWelding | NEURA | - | - |
| ArcWelding | PANASONIC | - | - |
| LaserCutting | LASERDYNE | - | - |
| LaserCutting | PRIMA | - | - |

### What the baselines reveal

Each technology vendor script (e.g., `ArcWeldingTechnology/KAWASAKI/Standard/Scripts/ArcWeldingTechnology.py`) defines:
- **Custom attributes** (Kawasaki ArcWelding alone defines 50+ attributes: weld conditions, weave patterns, SPS, RTPM, etc.)
- **Custom events** (ArcOn, ArcOff, LTOn, LTOff, SeamFinding, TouchSensing, SPS, etc.)
- **Workmethods** (ArcWelding, StitchWelding, SeamFinding, TouchSensing)

Running the TreeDumper against a scenario with each technology/vendor shows:
1. Which attributes appear at which level (program / group / operation / event)
2. Which events fire and in what order relative to motions
3. What `olp_property` flags control attribute inheritance
4. Default values for all technology parameters

This is **the definitive catalog** of what a downloader must handle per vendor.

### Tasks

| # | Task | Effort |
|---|---|---|
| 2.1 | Run TreeDumper on existing 3 scenarios, commit YAML baselines | S |
| 2.2 | Create minimal `.cendoc` scenarios for remaining ArcWelding vendors | L (requires E2) |
| 2.3 | Create minimal `.cendoc` scenarios for LaserCutting vendors | L (requires E2) |
| 2.4 | Commit all YAML baselines to `community/scenarios/` | S |

---

## Phase 3: Technology Customization

### Goal
Build Technology plugins under `Technologies/` in the starter repo for customizations beyond the standard community scripts.

### Where the baselines help

With YAML baselines per vendor, we can:
1. **Diff two vendor technologies** — e.g., compare Kawasaki ArcWelding attributes vs KUKA ArcWelding to see vendor-specific vs common attributes
2. **Plan which attributes need custom UI** — identify attributes that need visibility rules, tab assignments, or value validation
3. **Generate PostTechInitAttributes scaffolds** — auto-generate attribute setup from the baseline dump
4. **Validate downloader coverage** — check that every attribute/event in the baseline is handled by the downloader

### Initial Technology targets

| Technology | Vendor | Priority | Rationale |
|---|---|---|---|
| ArcWelding | KAWASAKI | High | Active downloader development, 28 event scripts |
| ArcWelding | (next vendor) | Medium | Extend pattern to second vendor |
| LaserCutting | TRUMPF | Medium | Different technology type, validates generality |

### Tasks (Kawasaki ArcWelding first)

| # | Task | Effort |
|---|---|---|
| 3.1 | Analyze KAWASAKI YAML baseline → catalog all attributes by level and event | S |
| 3.2 | Create `Technologies/ArcWeldingTechnology/KAWASAKI/` folder structure | S |
| 3.3 | Scaffold `PostTechInitAttributes.py` — custom attributes beyond standard | M |
| 3.4 | Scaffold `PostWmSyncPgAttributes.py` — attribute sync rules | M |
| 3.5 | Document attribute catalog in `docs/ctrl-specific/KAWASAKI/spec/` | S |

---

## Dependencies

```mermaid
graph LR
    P1[Phase 1: TreeDumper translator] --> P2[Phase 2: Generate baselines]
    P2 --> P3[Phase 3: Technology customization]
    P1 --> P3
```

Phase 1 is the enabler. Phase 2 needs E2 access to run downloads. Phase 3 can start in parallel using existing text-based reference dumps while the YAML dumper is built.

---

## Open Questions

1. **TreeDumper name** — `TreeDumper` or something more descriptive like `OlpInspector`?
2. **Inherited attributes** — include `GetInheritedAttributes()` in v1, or defer to v2? (adds complexity: need to track what's inherited vs local)
3. **Scenario creation** — who creates the missing `.cendoc` files for vendors without scenarios? (requires E2 + vendor robot model)
4. **YAML library** — confirm E2 Python 3.12 does NOT have `pyyaml` in `site-packages`. If it does, use it; if not, manual emitter.
