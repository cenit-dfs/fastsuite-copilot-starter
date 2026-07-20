# Process-geometry import and synchronization

Process-geometry import spans three owners. Keep their responsibilities separate:

1. The importer parses source data, creates geometry, assigns targets, and attaches source metadata.
2. The workmethod optionally copies geometry metadata into operation attributes during `PostWmSyncPgAttributes`.
3. An AutoExecute auxiliary command may consume operation attributes after programming and add program events.

## Register the importer

`InitPkg.py` returns a `ProcessGeometryPackage` and registers a named import type:

```python
def InitializeWorkpiecePackage():
    package = Customization.ProcessGeometryPackage()
    package.ProcessGeometryImportTypes.Add("AtolPointImport", AtolPointImport)
    return package
```

Keep the import type name stable once users or configuration refer to it.

## Parse command rows as state

The teaching CSV format uses semicolon-separated rows:

```text
1;Speed;0.3
2;Wait;1.5
3;Move;100;200;300;0;0;90
```

`Speed` and `Wait` are pending modifiers for the next `Move`. Consume and clear them after the move so they cannot leak into later geometry. Validate field counts and numeric values before creating geometry. Convert source millimetres to E2 metres explicitly.

Orientation conversion is a source-format contract, not a generic E2 rule. The example assumes `R = Rx * Ry * Rz`, derives tangent and normal vectors, normalizes them, and rejects zero-length vectors. Change this only with a source-format specification and a known reference pose.

## Attach optional metadata

The importer stores `Has_Speed`/`Speed` and `Has_Wait`/`Wait` on each point. The `Has_*` flags distinguish an absent modifier from a valid numeric default such as zero.

Do not use broad exception handling to hide required API failures. If optional typed metadata is not supported by the target R2026.1 API, log the limitation and keep the basic point import deterministic.

## Synchronize into the workmethod only when needed

Create matching read-only operation attributes in `PostWmInitAttributes`, then copy values from the current geometry in `PostWmSyncPgAttributes`:

```python
def PostWmSyncPgAttributes(Operator: CENPyOlpWM_SyncPgAttribOperator):
    setter = Operator.GetAttribSetter()
    geometry = Operator.GetCurrentProcessGeometryOperator()

    has_speed = geometry.GetBool("Has_Speed")
    setter.SetBool("Has_Speed", has_speed, False)
    if has_speed:
        setter.SetDouble("Speed", geometry.GetDouble("Speed"), False)
```

Synchronization is optional. Add it only when downstream UI, download logic, or auxiliary processing consumes operation attributes. Guard optional values with `Has_*` before reading them.

## AutoExecute insertion

An auxiliary command under:

```text
Technologies/TechnologyCommon/Standard/AuxiliaryCommands/AutoExecute/
```

can inspect the active program after process-geometry programming and insert built-in speed or dwell events. This is a separate mutation phase, so make it idempotent or define how repeated execution avoids duplicate events. Do not assume the command is active merely because the file exists; confirm the selected template's AutoExecute integration and controller setting.

## Verification

- Import one point with both modifiers, one with neither, and one with zero values.
- Verify target position, normal, tangent, unit conversion, and row-to-point association.
- Confirm `Has_*` flags and optional values on the process geometry.
- Program the geometry and confirm synchronized operation attributes.
- Run AutoExecute twice and check the expected duplicate-handling policy.
- Use `OLPTranslators/TreeDumper.py` to compare the process geometry, operations, motions, and inserted events.
