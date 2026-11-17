# KUKA Arc Welding Troubleshooting and Validation

Use this guide when E2 simulation, generated SRC/DAT, OfficeLite loading, or real-cell behavior differs from the intended KUKA Arc Welding workflow.

## Preserve evidence first

Before changing an operation or generated file, capture:

- E2, KSS, and all relevant KUKA option-package versions.
- The selected controller, tool, base, WPS, sensor IDs, task/set IDs, and correction IDs.
- E2 log messages, including complete `ML0xx` messages.
- The generated SRC and DAT pair.
- Screenshots of Programming defaults and the affected operation attributes.
- Whether the result came from E2 simulation, OfficeLite load, OfficeLite execution, or a real controller.
- The exact operation and physical feature where behavior diverged.

Do not diagnose SRC without its DAT. Many apparent motion or inline-form problems originate in declarations, data types, or values.

## Fast triage

| Symptom | First check |
| --- | --- |
| Required controls are missing | Active calibration method, controller family, selected WPS, installed AML flag, and E2 restart after deployment |
| Expected sensing event is absent from output | Confirm the event exists on the operation/tree before changing the downloader |
| Controller rejects an inline form | Option-package version, inline-form provider, fold metadata, executable call, and DAT type |
| Correction occurs on the wrong axis | Seam frame, physical search direction, Finding recipe, and sensor profile |
| Correction sign is wrong | Tool/frame calibration and controller dataset sign before changing E2 mappings |
| Tracking starts at the wrong location | Tracking offset, Search Start dataset, path direction, and on-distance |
| AML was selected but native paths were generated | Find the first `ML0xx` fallback warning |
| SRC looks correct but loading fails | Check paired DAT declarations, variable-name length, duplicate symbols, and option-package availability |

## Controls or literals do not appear

### Likely causes

- The wrong calibration method is active.
- The selected sensor tool type hides unrelated fields.
- The WPS is not a multi-row data-valid process-table WPS.
- AML is not marked installed or its version is unsupported.
- JSON or language resources were changed without restarting E2.
- Technology and downloader files came from different baselines.

### Actions

1. Reopen the exact Programming defaults or operation tab shown in the relevant guide screenshot.
2. Verify the technical attributes in the [Configuration Reference](configuration-reference.md).
3. Restart E2 after script, JSON, Settings.xml, or language-resource changes.
4. Create one new controlled operation. Existing operation state can hide whether defaults loaded correctly.
5. Review E2 initialization errors before editing UI configuration.

## TouchSense

### Correction uses the wrong axis

1. Identify the first weld motion used to construct the seam frame.
2. Confirm local X follows the seam, local Z is opposite tool Z, and local Y completes the frame.
3. Check the physical direction of each touch against that frame.
4. For linked touches, verify the current initial mapping `1 -> Z`, `2 -> Y`, `3 -> X`.
5. Compare the visual correction fields with the executable `TS_BC6DCalc(Z1,Z2,Z3,Y1,Y2,X1)` call.

Do not reorder the KRL arguments to match the visual X/Y/Z field order. They are different representations by design.

### Six-dimensional correction is not generated

Check that:

- All touches share the intended connection ID and linked state.
- The search directions produce a legal routing bucket count.
- Additional observations provide at least two Y or at least two Z measurements for rotational compensation.
- No expected touch operation was omitted or reordered in the E2 tree.

Inspect the generated SRC/DAT to verify touch order, correction routing, and declarations.

### Search motion is unsafe or misses the surface

- Verify start offset, sensing length, overtravel, search speed, and approach type.
- Inspect wire/nozzle geometry and the selected sensor method.
- Simulate both approach and return paths.
- Reduce controller search limits and speed for the first physical test.
- Correct geometry or calibration before compensating with larger search lengths.

### Correction sign is reversed

Test one axis at a time with a known positive part displacement. Record the measured vector and resulting robot correction. If E2's search direction and seam frame are correct, investigate tool/base calibration and controller TouchSense data before changing routing logic.

## SeamTech Finding

### Wrong correction axis or channel

1. Confirm the selected recipe name.
2. Confirm `scan_ops` matches the programmed scan count and order.
3. Trace the recipe axis to `<ALONG>`, `<LATERAL>`, or `<HEIGHT>`.
4. Resolve that placeholder through the selected sensor profile.
5. Compare the result with the generated `BF_BC6DCalc` arguments.

The profile is sensor-mount-specific. Copying `Example_Top`, `Example_Left45`, or `Example_Right45` to a differently mounted sensor can produce a syntactically valid but physically wrong correction.

### Missing or repeated measurement

- Confirm every expected scan operation exists in the tree.
- Confirm the recipe references only `ATTR1` through the last required scan.
- Verify each scan emits `BF_InitMovement`, `BF_Search`, and `BF_SetCorrData` for its own attribute record.
- Check for duplicate or missing operation ordering before changing JSON.

### Sensor ID or correction ID is wrong

- `SensorIdLine` should reach `BF_Init(<id>)` in current output.
- `SeamFindingId` should reach `BF_CorrSave(<id>, ...)` and any later load call.
- The fold text and executable call must agree; inspect both.

### Sensor display name is missing or wrong

The optional fold label comes from `sensors` in `SeamFind_Sensor_Profiles.json`, keyed by exact integer ID. Compare it with the WorkVisual sensor name. A missing mapping intentionally emits `SeamFind Init Sensor <id>` without inventing a label; it does not change `SensorNo` or `BF_Init`.

### Finding generation rejects a correction bucket

Inspect the resolved recipe rather than padding the generated KRL. X accepts 0 or 1 populated slots, Y accepts 0, 1, or 2, and Z accepts 0, 1, or 3. Two populated Z slots, half-empty ATTR/CD pairs, unknown CD fields, and ATTR references absent from `scan_ops` are configuration errors.

For Finding 4.0.3, a valid lower-dimensional recipe emits `1D`, `2D`, or `3D`; `FREE` is reserved for more than three active correction pairs.

### Correction remains active after sensor clear

This is expected until the explicit correction-off boundary. `BF_ClearSensor()` closes the sensor session; it does not switch off workpiece correction. Verify one clear after correction calculation and one final `BF_CorrOff()` after the last motion that needs correction. Do not move `BF_CorrOff()` earlier merely to silence the state: KUKA warns against switching correction off before the robot leaves the corrected workspace.

### OfficeLite loads but the scan cannot be validated

OfficeLite proves syntax, declarations, and available option-package calls. It does not prove laser visibility, measured channel signs, scan result quality, or correction behavior. Complete those checks on a real cell at reduced speed.

## SeamTech Tracking

### Search Start moves or searches in the wrong direction

- Confirm Search Start is enabled on the intended operation only.
- Verify Search Start set ID and task number independently of the normal tracking set.
- Check track mode (`Both`, `Side`, or `Height`) and all three Search Start offsets.
- Verify weld-path direction and the line-laser frame/FOV.
- Confirm the generated `STTg_SearchSeamStart` uses the expected target and increment frames.

### Tracking starts too early or too late

Check the relationship between:

- Seam tracking offset.
- `KukaTrackingOnDistance`.
- Sensor-to-TCP physical distance.
- Motion direction and any path trigger delay.

A numerically correct trigger can still be physically wrong when the calibrated sensor offset or path direction is wrong.

### Correction exceeds limits or is removed unexpectedly

- Review maximum linear correction and correction elimination distance.
- Check continue-after-error behavior.
- Check tracking-off distance and **Keep offset**.
- For Multilayer native paths, confirm intermediate passes retain the intended correction and only the final pass clears the sensor.

### Controller reports missing tracking calls

1. Confirm the generated code branch matches the installed Tracking version.
2. For 4.0.3, verify `STTg_SensorInit`, `STTg_SensorOn`, `STTg_SearchSeamStart`, and `STTg_SensorOff` are available.
3. Confirm legacy `STT_PrepareWeave` or `STT_SensorWeave` calls were not emitted for 4.0.3.
4. Compare the DAT `STTg_SensorSet_T` fields with a controller-taught sample from the same option-package version.

### OfficeLite limitation

OfficeLite cannot emulate the physical line laser. A successful load is not evidence that Search Start finds the seam or that tracking correction is stable. Record real-controller evidence separately.

## Multilayer

### Controls are hidden

- Turn **WPS Automatic** off.
- Select a named process-table WPS.
- Confirm more than one matching row is data-valid.
- Confirm rows have stable IDs and layer/bead values.
- Recompute or recreate an operation after process-table changes.

Do not set or infer a Multilayer flag in process-table column 36. The resolver uses matching data-valid pass count.

### AML selection falls back to native output

Find the diagnostic code and respond to that cause:

| Codes | Category |
| --- | --- |
| `ML001`-`ML006` | WPS or stable operation metadata cannot form a valid Multilayer seam |
| `ML007`-`ML008` | AML installation/version/controller configuration is not eligible |
| `ML009`-`ML012` | Geometry or motion cannot be represented safely in AML |
| `ML013`-`ML014` | Recipe snapshot changed or source disappeared |
| `ML015`-`ML018` | Requested sequencing, simulation, direction, or automatic matching is unsupported/unverified |

Use the full code table in the [Configuration Reference](configuration-reference.md#multilayer-diagnostics). Fallback is normally seam-scoped; inspect each seam independently.

### Finding or TouchSense repeats in filler layers

This is invalid AML ownership. Sensing and correction calculation belong before or inside root `CASE 0`; filler cases derive geometry from the corrected root and must not repeat physical measurements.

### Filler positions do not follow the root

Verify:

- Every welded root point has its own AML weld-point state.
- Root motions record positions through `AmlSetPos`.
- Fillers use `AmlGetPos` with the intended `LayerOffsetN`.
- The root/filler command ordinal identifiers correspond.
- Translational offsets were converted from E2 metres to KRL millimetres.
- Work/travel-angle and normal/contour offset signs match the validated project convention.

### Native output unexpectedly shares data

Native passes must remain independent. Each pass should have complete geometry and its own point, WDAT, and WS declarations.

### Recipe changes are not reflected

Existing operations hold an applied snapshot. Check `MultiLayerRecipeState`:

| State | Meaning |
| --- | --- |
| `CurrentSnapshot` | Operation matches the applied recipe snapshot |
| `UpdateAvailable` | Source WPS differs; review before reapply |
| `Detached` | Effective operation geometry was changed locally |
| `MissingSource` | Original WPS row can no longer be resolved |
| `NotApplicable` | Operation is not using the Multilayer process-table path |

Do not silently overwrite reviewed operation changes. Reapply/regenerate through the approved project workflow after previewing all changed passes.

## SRC/DAT load errors

Review in this order:

1. First compiler message, not the cascade that follows it.
2. Installed option packages and exact versions.
3. SRC call name and argument count.
4. DAT type name and field names.
5. Missing or duplicate declarations.
6. Variable names longer than KRL limits.
7. Inline-form provider and metadata version.
8. Whether SRC and DAT came from the same download.

Do not fix generated output manually and call the issue resolved. A manual edit is useful only as an experiment that identifies the required generator change.

## Validation evidence levels

| Level | Evidence | Proves | Does not prove |
| --- | --- | --- | --- |
| 1 | Static SRC/DAT inspection or golden comparison | Deterministic structure and expected tokens | KRL validity or runtime behavior |
| 2 | E2 simulation | Reachability, E2 path geometry, and modeled collision behavior | Controller syntax or sensor physics |
| 3 | OfficeLite load | KRL syntax, declarations, and installed API availability | Physical sensing/tracking or process safety |
| 4 | OfficeLite execution | Executable non-hardware controller flow | Real sensor, I/O, correction sign, or weld process |
| 5 | Real controller dry run | Robot motion, I/O, sensor interaction, and correction behavior under test conditions | Production weld quality |
| 6 | Controlled production validation | Approved process result for the tested configuration | Untested versions, tools, recipes, or cells |

This repository does not include cell-specific validation results. Record evidence for each target configuration using the validation levels above.

## Record a validation result

For every accepted fixture, record:

```text
Date:
E2 version:
Controller/KSS:
Option-package versions:
Program and SRC/DAT checksum:
Selected tool/base/WPS/sensor datasets:
Validation level:
Observed warnings:
Expected result:
Actual result:
Reviewer:
Open limitations:
```

A result applies only to the recorded combination. Re-run the relevant checks after changing controller versions, option packages, sensor calibration, WPS data, JSON mappings, technology scripts, or downloader code.
