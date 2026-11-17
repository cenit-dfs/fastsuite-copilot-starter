# KUKA Arc Welding OLP Programmer Guide

This guide is for FASTSUITE E2 application engineers who create and validate KUKA Arc Welding programs. It assumes the cell, tools, bases, welding technology, controller family, and required KUKA option packages have already been configured by an administrator.

For deployment and project configuration, use the [E2 Administrator Guide](e2-admin-guide.md). For exact field definitions, use the [Configuration Reference](configuration-reference.md).

## Before programming

Confirm the following before creating operations:

- The active controller is the intended KUKA KRC5/KSS target.
- Welding TCP, line-laser frame, bases, and sensor datasets match the target controller.
- The selected calibration method matches the intended workflow.
- The WPS and process-table rows are approved for the project.
- Search and tracking limits are appropriate for the expected part variation.
- The complete robot program can be simulated without collision, singularity, limit, or reachability errors.

Use only tool, base, coordinate, sensor, correction, and process values approved for the target project.

## Correction model

TouchSense and SeamTech Finding both establish a correction before welding, but they do not use the same measurement algorithm.

E2 derives a local seam frame from the first weld motion:

- **X** follows the seam tangent.
- **Z** points opposite the welding tool's Z direction.
- **Y** is calculated as `Z cross X`.
- X is recalculated as `Y cross Z` to keep the frame orthogonal.

TouchSense routes physical touch directions against this frame. SeamTech Finding uses the selected recipe and sensor profile to assign measured channels to X, Y, and Z. This distinction matters when diagnosing a correction on the wrong axis.

Both methods use the same six correction slots and bucket cardinalities:

| Bucket | Slots | Legal filled-slot counts |
| --- | --- | --- |
| X | X1 | 0 or 1 |
| Y | Y1, Y2 | 0, 1, or 2 |
| Z | Z1, Z2, Z3 | 0, 1, or 3 |

Two filled Z slots are invalid. The executable order is always `Z1, Z2, Z3, Y1, Y2, X1`; unused TouchSense slots use `TSg_CD0`, while unused Finding slots use `BFg_PColl0_CD`.

For both methods:

1. Place sensing where the feature is visible and reachable.
2. Make every sensing motion collision-free, including overtravel.
3. Simulate sensing, welding, and exit motions as one complete program.
4. Verify the generated correction fold and executable call before controller use.

## Program TouchSense

Use TouchSense when the welding wire or nozzle searches physical surfaces before welding. See the KUKA manual sections on measurement directions, base correction, and inline forms in the [KUKA.TouchSense 3.2.2 manual](https://xpert.kuka.com/service-express/portal/project1_p/document/kuka-project1_p-common_PB12250_en?context=%7B%22filter%22%3A%7B%7D%2C%22text%22%3A%22KUKA.TouchSense%203.2.2%20manual%22%2C%22page%22%3A32%7D).

### 1. Set programming defaults

1. Open **Programming defaults** for Arc Welding.
2. Set **Calibration** to **Touch by point indication**.
3. Select the required connection type.
4. Open the TouchSense defaults.
5. Select the sensor tool type, sensor ID/TCP, calibration frame, detection method, start offset, wire diameter, approach motion, and sensing speed.

The sensor tool type determines which controller sensor ID is used:

- Touch sensor uses `SensorIdTouch`.
- Point laser uses `SensorIdPoint`.
- Line laser uses `SensorIdLine`.

### 2. Indicate the touch position

1. Select the weld seam geometry in 3D.
2. Indicate the touch position on the physical feature to be measured.
3. Create the operation group.
4. Inspect the generated approach, search direction, touch point, and return motion.

### 3. Adjust operation attributes

1. Set **Vision Frame** to the weld TCP.
2. Deselect CAD Mastered. This almost never works in real life due to inaccuracies of setup. Live mastering is required during 1st run.
3. Set each touch so that the search ray intersects the intended feature with enough clear approach and overtravel. Use **Touch connect ID** to associate related touches and **Linked Touch** when the touches form one correction set.

For a six-point correction, the intended physical model is:

- The first three or fewer measurements establish translational correction.
- Optional measurements four through six provide the additional observations needed for rotational compensation.

The current E2 linked-touch implementation has a specific initial progression:

| Linked sequence | Routed seam-frame axis |
| ---: | --- |
| 1 | Z |
| 2 | Y |
| 3 | X |

Additional observations are clustered by their measured direction in the seam frame. The final KUKA calculation slots are always assembled as:

```text
TS_BC6DCalc(Z1, Z2, Z3, Y1, Y2, X1)
```

Unused slots receive the neutral correction record `TSg_CD0`. Rotational compensation is selected when the routed set contains at least two Y observations or at least two Z observations.

### 4. Simulate and verify TouchSense

Simulate the whole program, not only the touch group. Confirm:

- The correct physical surface is crossed by every search.
- Search direction and available overtravel are safe.
- The wire/nozzle clears the part during approach and return.
- The correction remains active for the intended seam and is cleared at the correct boundary.

After download, inspect the TouchSense folds. The inline-form presentation lists correction fields in X/Y/Z order, while the executable macro uses KUKA's Z/Z/Z/Y/Y/X argument order.

Inspect the generated SRC/DAT to confirm that the search folds, correction calculation, and declarations match the configured operations.

## Program SeamTech Finding

Use SeamTech Finding when a line laser scans one or more features before welding. See the KUKA manual sections on measurement, correction calculation, and correction data in the  [KUKA.SeamTech Finding 4.0.3 manual](https://xpert.kuka.com/service-express/portal/project1_p/document/kuka-project1_p-common_PB22249_en?context=%7B%22filter%22%3A%7B%7D%2C%22text%22%3A%22KUKA.SeamTech%20Finding%204.0.3%20manual%22%2C%22page%22%3A39%7D).

### 1. Select profile and recipe

1. Set **Calibration** to **Touch by point indication**.
2. Set **SensorToolType** to **Line Laser**.
3. Select the controller sensor ID and calibrated vision frame.
4. Deselect CAD Mastered. This almost never works in real life due to inaccuracies of setup. Live mastering is required during 1st run.
5. Select the sensor mount profile (mechanical mounting position and correction naming rule).
6. Select the Seam Finding recipe (define how many scans total and how many corrections per scan).
7. Set the controller task (e.g. edge, fillet etc. as defined in CTRL) and correction IDs.

The sensor profile maps the abstract channels `ALONG`, `LATERAL`, and `HEIGHT` to controller CD fields. The recipe maps ordered scans (`ATTR1`, `ATTR2`, and `ATTR3`) to correction axes. Scan order therefore comes from the recipe; it is not inferred from the operation name or spatial order.

The optional text after the sensor number in the generated init fold is the WorkVisual display name. If no E2 mapping exists, the label is omitted rather than guessed.

### 2. Indicate and program scan geometry

1. Select the process geometry.
2. Indicate the Finding position on the part surface.
3. Create the operation group.
4. Adjust the scan position and orientation so the laser plane sees the intended joint feature.

### 3. Tune each scan

Set sensor ID, frame, mount profile, recipe, task, correction ID, approach motion, approach speed, sensing speed, and search offset. Ensure the selected recipe expects exactly the number and order of scans being programmed.

Typical recipes resolve one scan into Z only, Z plus Y, or Z plus X. Multiple scans add independent observations. A three-scan recipe can provide six correction inputs for a free six-dimensional correction.

### 4. Simulate and verify Finding

Confirm that the laser plane crosses the intended feature over the complete search motion. After download, verify:

- `BF_Init` is present before measurement.
- Each scan writes the expected `BFATTR1`, `BFATTR2`, or `BFATTR3` record.
- `BF_SetCorrData` follows the corresponding search.
- The correction fold references the recipe-selected CD channels.
- `BF_CorrSave` uses the configured correction ID.
- `BF_ClearSensor()` appears once after correction calculation to close the sensor session.
- `BF_CorrOff()` appears after the last motion that needs the corrected workspace. Clearing the sensor does not switch correction off.

Inspect the generated SRC/DAT to verify measurement order, correction channels, save ID, and declarations. For profile/recipe substitution rules, see the [Configuration Reference](configuration-reference.md#seam-finding-json).

## Program SeamTech Tracking

Use SeamTech Tracking when the line laser continuously corrects the path during welding. See the KUKA manual sections on sensor datasets, Search Start, tracking activation, and error behavior in the [KUKA.SeamTech Tracking 4.0.3 manual](https://xpert.kuka.com/service-express/portal/project1_p/document/kuka-project1_p-common_PB21432_en?context=%7B%22filter%22%3A%7B%7D%2C%22text%22%3A%22KUKA.SeamTech%20Finding%204.0.3%20manual%22%2C%22page%22%3A39%7D).

### 1. Set tracking defaults

1. Open Arc Welding programming defaults.
2. Set **Calibration** to **Seam Tracking Line Laser**.
3. Set the seam tracking offset between sensor observation and welding point.
4. Verify the selected WPS.
5. Set the laser FOV translation and rotation to the calibrated sensor geometry.

Do not use FOV values to compensate for an uncalibrated or incorrectly mounted sensor. They must describe the validated sensor-to-tool geometry used by the project.

### 2. Program and tune the weld operation

Select the 3D process geometry and create the operation group. On each tracking operation, verify:

- Seam tracking offset.
- Tracking-on and tracking-off path distances.
- Tracking set ID and seam/task number.
- Search length, maximum linear correction, and correction elimination distance.
- Continue-after-error behavior.
- Whether the offset is kept when tracking switches off.
- Search Start enablement, speed, set ID, task number, mode, offsets, and limits.

Search Start uses a separate controller dataset from normal tracking. Configure both datasets for the target controller and project.

### 3. Simulate and verify

Simulation must cover the complete sensor lead, Search Start path, weld path, and tracking-off distance. Confirm that the sensor field of view remains on the feature and that the robot can execute the offset path without collision.

For SeamTech Tracking 4.0.3 output, verify:

- `SensorIdLine` reaches `STTg_SensorInit(<id>)`.
- The tracking seam pattern reaches `iTaskNr` in the tracking dataset.
- Search Start has its own `STTg_SensorSet_T` declaration.
- `STTg_SearchSeamStart` appears in the expected motion order when Search Start is enabled.
- Tracking switches on through `STTg_SensorOn` and switches off through the version-appropriate `STTg_SensorOff` call.
- Legacy `STT_PrepareWeave` and `STT_SensorWeave` calls are not emitted for 4.0.3.

OfficeLite can validate syntax and declarations but does not emulate the physical line laser. Final offset direction, search behavior, and correction retention require a real-cell reduced-speed test.

## Program Multilayer welding

The process table is the source of pass count, layer/bead identity, process values, and pass geometry. The deprecated `TechTabs/Multilayer.csv` is not used.

See the KUKA manual sections on block structure, root position recording, filler offsets, and layer execution in the [KUKA.ArcTech Multilayer 3.7.1 manual](https://xpert.kuka.com/service-express/portal/project1_p/document/kuka-project1_p-common_PB22944_en?context=%7B%22filter%22%3A%7B%7D%2C%22text%22%3A%22KUKA.ArcTech%20Multilayer%203.7.1%20manual%22%2C%22page%22%3A35%7D).

### 1. Maintain and select the WPS

1. In ControllerBuilder, maintain all rows of the Multilayer WPS in the Arc Welding process table.
2. Give every pass a valid layer and bead number and mark the row data-valid.
3. Return to the Arc Welding programming defaults.
4. Turn **WPS Automatic** off.
5. Select the named Multilayer WPS (or predefined Single-layer WPS) from **WPS**.

Automatic CAD-driven WPS matching is not implemented for Multilayer resolution. A geometry carrying CAD match attributes while **WPS Automatic** is enabled produces `ML018` and does not enter the named-WPS Multilayer path.

### 2. Select the output mode

Choose one of these modes:

| Mode | Use when | Generated structure |
| --- | --- | --- |
| `E2NativePaths` | Every pass must remain explicit and independently simulated/generated | Complete seam geometry, points, WDAT, and WS variables are repeated for every pass |
| `KukaArcTechMultilayer` | The installed KUKA AML option pack should derive filler paths from a recorded root | Root geometry is stored once; filler cases use controller offsets and root positions |

For AML, enable **ArcTech Multilayer installed** and set the installed version. Keep **CompleteSeam** sequencing unless a separately validated project requirement says otherwise.

### 3. Simulate and adjust

Simulate every E2 pass and inspect work angle, travel angle, normal offset, contour offset, and start offset. Changing recipe-derived geometry detaches that operation from its original snapshot; review the entire seam after any manual adjustment.

E2 simulation is authoritative for native paths. AML filler geometry is generated by the controller from `LayerOffsetN`; E2 simulation is therefore an approximation and must be followed by an OfficeLite/controller dry run.

### 4. Verify native output

- Finding runs before the root pass.
- Each pass contains its own `ARCON`, interior weld motions, and `ARCOFF`.
- Each pass has independent point, WDAT, and WS declarations.
- No `AmlBlockBegin`, `AmlGetPos`, or `AmlSetPos` is present.

### 5. Verify AML output

- `AmlBlockBegin` opens the seam block.
- `SWITCH gAmlActLayer` selects `CASE 0` for the root and `CASE 1..N` for fillers.
- Finding remains in root `CASE 0` and is not repeated in filler cases.
- Root weld points are recorded through `AmlSetPos`.
- Fillers call `MLARCON`, `MLARCSWI`, or `MLARCOFF` and derive positions through `AmlGetPos(..., LayerOffsetN, ...)`.
- `AmlBlockCaseEnd`, `DEFAULT`, `ENDSWITCH`, and `AmlBlockEnd` close the structure.

If one seam uses an unsupported AML construct, the downloader issues an `ML0xx` warning and falls that seam back to native output. Do not remove the fallback warning from the validation record.

## Final download review

Before releasing any generated program:

1. Review the E2 log for warnings, especially `ML0xx` diagnostics.
2. Compare the selected tool, base, sensor IDs, correction IDs, WPS, and option-pack versions with the target controller.
3. Inspect the generated sensing/tracking initialization, calculation, save/load, clear, and off calls.
4. Load both SRC and DAT in OfficeLite or the target controller and resolve every declaration or inline-form error.
5. Dry-run without arc and sensor correction where the KUKA commissioning procedure requires it.
6. Validate sensing and correction at reduced speed with conservative search limits.
7. Validate the complete welded sequence, including correction lifetime between Multilayer passes.

Use [Troubleshooting and Validation](troubleshooting-validation.md) when any check fails.
