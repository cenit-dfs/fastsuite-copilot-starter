# KUKA Arc Welding Configuration Reference

This reference describes the current KUKA Arc Welding customization surface. Labels can vary with localization; technical attribute names are stable identifiers used by the technology and downloader.

## Units and value flow

- E2 stores length attributes in SI metres.
- The E2 UI normally displays those values in millimetres.
- KUKA output converts the applicable values to millimetres.
- Angular values are degrees unless the controlling KUKA option-package field states otherwise.
- Enum values in this reference are implementation literals; the UI may display localized text.

When diagnosing a factor-of-1000 error, compare the typed E2 value with both the displayed UI value and generated KRL.

## Shared programming defaults

| Attribute | Purpose | Current default/example |
| --- | --- | --- |
| `WeldContour` | Enables weld-contour programming | `true` |
| `SeamCalibrationMethod` | Chooses sensing/tracking workflow | `TouchSensByPoint` |
| `TSOperationsSorted` | Controls sensing-operation sorting | `false` |
| `TSConnectionType` | Connects sensing and weld correction | `OperationConnect` |
| `WPSAutomatic` | Selects automatic CAD matching or named WPS | `false` |
| `WPSAutomaticNames` | Named process-table WPS | Project-specific |
| `LaserFovX/Y/Z` | Laser field-of-view translation | `0 / 0 / 10 mm` |
| `LaserFovA/B/C` | Laser field-of-view rotation | `0 / 20 / 0 deg` |

For Multilayer, `WPSAutomatic=false` plus a named WPS is the implemented resolution path. `WPSAutomatic=true` with CAD match attributes reports `ML018`.

## Seam frame and correction slots

The downloader constructs the local seam frame from the first ArcOn motion:

| Axis | Construction |
| --- | --- |
| X | Normalized seam tangent |
| Z | Negative welding tool Z |
| Y | Normalized `Z cross X` |
| Rebuilt X | Normalized `Y cross Z` |

TouchSense direction routing uses sign-independent alignment with these axes. The final KUKA slot order is:

```text
[Z1, Z2, Z3, Y1, Y2, X1]
```

Empty slots are filled with `TSg_CD0`.

## TouchSense attributes

| Attribute | UI meaning | Default/example | Notes |
| --- | --- | --- | --- |
| `SensorToolType` | Sensor tool type | `Touch Sensor` | Selects touch, point-laser, or line-laser sensor ID |
| `SensorIdTouch` | Touch sensor ID | `1` | Used for touch-sensor selection |
| `SensorIdPoint` | Point-laser sensor ID | `2` | Used when point laser is selected |
| `SensorIdLine` | Line-laser sensor ID | Configured ID | Used by Finding and Tracking |
| `CalibrationFrameSelection` | Vision/calibration frame | Project-specific | Must match controller calibration |
| `TSTouchMethod` | Detection method | `Wire` | Wire/nozzle behavior is controller-dependent |
| `TouchDifferenceAngleNozzle` | Touch-angle adjustment | `45 deg` | Visible nozzle-angle setting |
| `SensingLength` | Start offset from touch | `30 mm` | Available search approach |
| `TSWireDiam` | Wire diameter | `1 mm` | Used for geometric compensation |
| `SeamCalibCadMastered` | CAD mastered | `true` | Project validation required |
| `TouchSensMotionTypeFirstTpe` | Motion to touch start | `PTP` | Initial approach type |
| `TSSpeedFromCyclePtp` | PTP approach speed | `50%` | UI percent |
| `TSSpeedFromCycleLin` | LIN approach speed | `0.5` | Used when linear approach is selected |
| `SensingSpeed` | Search speed | Project-specific | Keep within KUKA commissioning limits |
| `TouchId` | Touch connect ID | Project-specific | Associates touch with a correction set |
| `FramePt` | Frame point | Project-specific | Hidden or visible by context |
| `TSLinkedTouch` | Linked Touch | `false` | Enables linked correction routing |
| `OtherSideTouch` | Other-side alignment | `false` | Expert alignment control |

### Shared correction buckets

The active implementation gives linked sequence numbers 1 through 3 fixed initial hints:

| Sequence | Axis hint |
| ---: | --- |
| 1 | Z |
| 2 | Y |
| 3 | X |

TouchSense routing and resolved Seam Finding recipes use the same legal bucket counts:

- Z count: 0, 1, or 3.
- Y count: 0, 1, or 2.
- X count: 0 or 1.

The six-input calls are `TS_BC6DCalc(Z1,Z2,Z3,Y1,Y2,X1)` and `BF_BC6DCalc(Z1,Z2,Z3,Y1,Y2,X1)`. Empty slots use `TSg_CD0` and `BFg_PColl0_CD`, respectively. The inline-form correction display uses X, Y, then Z presentation fields and must not be read as executable argument order.

## Seam Finding attributes

| Attribute | UI meaning | Default/example | Notes |
| --- | --- | --- | --- |
| `SensorToolType` | Sensor tool type | `Line Laser` | Makes line-laser settings relevant |
| `SensorIdLine` | Sensor ID line | Configured ID | Passed to current `BF_Init(<id>)` output |
| `CalibrationFrameSelection` | Vision frame | Configured frame | Must match calibrated controller frame |
| `KukaSeamFindingMountType` | Sensor mount position/profile | Configured profile | Selects JSON profile |
| `KukaSeamFindingRecipe` | Seam Finding recipe | Configured recipe | Selects JSON recipe |
| `SeamFindingJointType` | Sensor task/joint selection | Project-specific | Displayed as sensor task in current UI |
| `SeamFindingId` | SF correction ID | Configured ID | Used by correction save/load |
| `SensingLength` | Start offset | Configured length | Search setup |
| `SensingSpeed` | Sensing speed | Configured speed | Project/controller limit applies |

## Seam Finding JSON

The files are loaded at technology initialization:

- `Technologies/ArcWeldingTechnology/KUKA/Standard/TechTabs/SeamFind_Sensor_Profiles.json`
- `Technologies/ArcWeldingTechnology/KUKA/Standard/TechTabs/SeamFind_Recipes.json`

### Sensor profile schema

```json
{
  "sensors": [
    {
      "id": 1,
      "display_name": "LineLaser"
    }
  ],
  "profiles": [
    {
      "name": "Example_Top",
      "ALONG": "CDh",
      "LATERAL": "CDh",
      "HEIGHT": "CDv"
    }
  ]
}
```

`sensors` is an optional ID-to-WorkVisual-display-name mapping. It affects only the init-fold label; `SensorIdLine` still supplies `SeamFind.SensorNo` and `BF_Init`. Missing IDs omit the label. IDs must be unique positive integers, and display names must be non-empty and contain no line break, semicolon, percent sign, or brace.

`ALONG`, `LATERAL`, and `HEIGHT` are geometric roles. Their values are KUKA result fields from the commissioned sensor/task configuration. Sensor identity and mount/CD mapping remain independent despite sharing one physical JSON file.

### Recipe schema

```json
{
  "name": "Scan 1: Z+Y Scan 2: Z+X (across + along)",
  "scan_ops": ["ATTR1", "ATTR2"],
  "header": "X:(1:ATTR2.<ALONG>) Y-A:(1:ATTR1.<LATERAL>) Z-BC:(1:ATTR1.<HEIGHT> 2:ATTR2.<HEIGHT> 3: . )",
  "ilf_params": {
    "XCorre": "ATTR2",
    "XcdParam": "<ALONG>",
    "YCorr": "ATTR1",
    "YcdParam": "<LATERAL>",
    "ZCorr": "ATTR1",
    "ZcdParam": "<HEIGHT>",
    "Y2Corr": "EMPTY",
    "Y2cdParam": "EMPTY",
    "Z2Corr": "ATTR2",
    "Z2cdParam": "<HEIGHT>",
    "Z3Corr": "EMPTY",
    "Z3cdParam": "EMPTY"
  }
}
```

Rules:

- `scan_ops` defines required measurement order and count.
- Correction references must name an entry in `scan_ops` or use `EMPTY`.
- CD parameters use `<ALONG>`, `<LATERAL>`, `<HEIGHT>`, or `EMPTY`.
- Every populated slot must contain both an ATTR reference and CD parameter.
- Legal populated counts are X `0/1`, Y `0/1/2`, and Z `0/1/3`; two populated Z slots are invalid.
- Profile substitution occurs after recipe selection.
- `header` is presentation metadata; executable parameters remain authoritative.
- Names must be unique because they are UI literals.
- Restart/reload the technology after changing either file.

### Finding lifecycle output

`BF_ClearSensor()` closes the sensor session after correction calculation. It does not deactivate the workpiece correction. `BF_CorrOff()` is emitted separately after all program motion that may depend on the corrected workspace. AML flow calls such as `AmlBlockCaseEnd()` and `AmlBlockEnd()` do not replace either Finding lifecycle call.

### Delivered recipe patterns

| Pattern | Correction observations |
| --- | --- |
| Z only | One HEIGHT observation |
| Z+Y | HEIGHT and LATERAL from one across scan |
| Z+X | HEIGHT and ALONG from one along scan |
| Z+Y plus Z+X | Across and along scans |
| Z+Y plus Z+Y | Two across observations |
| Three-scan free correction | One along plus two across scans, or the inverse order |

## Seam Tracking attributes

### Normal tracking

| Attribute | UI meaning | Default |
| --- | --- | ---: |
| `SeamTrackingDistance` | Seam tracking offset | `55 mm` in current defaults |
| `KukaTrackingOnDistance` | On distance | `0 mm` |
| `KukaTrackingSetId` | Seam tracking set | `S1` |
| `KukaTrackingSeamPatternNr` | Seam pattern/task | `2` |
| `KukaTrackingSearchLength` | Search length | `150 mm` |
| `KukaTrackingContAfterErr` | Continue after error | `Without offset` |
| `KukaTrackingMaxLinCorrection` | Maximum linear correction | `50 mm` |
| `KukaTrackingCorrElimDistance` | Correction elimination distance | `200 mm` |
| `KukaTrackingOffDistance` | Off distance | `0 mm` |
| `KukaTrackingOffKeepDistance` | Keep offset after switch-off | `true` |
| `SeamTrackSearchStart` | Search Start Point | `true` |
| `SeamTrackSearchSpeed` | Search velocity | `10 mm/s` in sample |

### Search Start 4.0.3

| Attribute | UI meaning | Default |
| --- | --- | ---: |
| `KukaSearchStartSetId` | Search Start set ID | `S4` |
| `KukaSearchStartTaskNr` | Task number | `1` |
| `KukaSearchStartSearchLength` | Search length | `100 mm` |
| `KukaSearchStartCorrElimDistance` | Correction elimination distance | `20 mm` |
| `KukaSearchStartMaxCorrection` | Maximum correction | `25 mm` |
| `KukaSearchStartErrorReaction` | Error reaction | `Without offset` |
| `KukaSearchStartTrackMode` | Track mode | `Both` |
| `KukaSearchStartSideOffset` | Side offset | `0 mm` |
| `KukaSearchStartHeightOffset` | Height offset | `0 mm` |
| `KukaSearchStartPathOffset` | Path offset | `0 mm` |

Track mode literals are `Both`, `Side`, and `Height`. Error behavior literals are `Without offset` and `With offset`.

For Tracking 4.0.3, `SensorIdLine` supplies the sensor initialization ID and `KukaTrackingSeamPatternNr` supplies `iTaskNr`. Search Start has an independent dataset declaration.

## Multilayer attributes

### User-facing controls

| Attribute | Literals/default | Behavior |
| --- | --- | --- |
| `MultiLayerOutputMode` | `E2NativePaths` (default), `KukaArcTechMultilayer` | Selects explicit E2 passes or AML projection |
| `MultiLayerSequenceMode` | `CompleteSeam` (default), `LayerBeadAcrossSeams` | Cross-seam mode currently falls back to CompleteSeam |
| `MultiLayerDirectionMode` | `SameDirection` (default), `Alternating`, `ZigZag` | Same, per-layer alternating, or per-pass alternating |
| `MultiLayerDirectionOverride` | `InheritProgram` (default), `Forward`, `Reverse` | Operation-level direction override |
| `KukaArcTechMultilayerInstalled` | `false` | Explicit option-pack availability setting |
| `KukaArcTechMultilayerVersion` | `3.7.1.4` | Configured option-pack version |

AML is forced back to native mode when the installed flag is false. `ZigZag` is a native-path capability; AML exposes direction per layer/case and cannot represent arbitrary per-pass zigzag inside a layer.

### Read-only operation metadata

| Attribute | Meaning |
| --- | --- |
| `MultiLayerMetadataVersion` | Metadata schema version |
| `MultiLayerUsesProcessTable` | Operation resolved from process-table WPS |
| `MultiLayerWpsMainId` / `MultiLayerWpsSubId` | Stable process-table row identity |
| `MultiLayerWpsName` | Selected WPS display name |
| `MultiLayerLayerNumber` / `MultiLayerBeadNumber` | Pass coordinates |
| `MultiLayerFlatPassIndex` | Deterministic pass index; root is 0 |
| `MultiLayerSeamUuid` | Source process-geometry identifier |
| `MultiLayerRecipeFingerprint` | Applied recipe snapshot hash |
| `MultiLayerRecipeState` | `NotApplicable`, `CurrentSnapshot`, `UpdateAvailable`, `Detached`, or `MissingSource` |
| `MultiLayerWorkAngleOffset` | Effective work-angle offset |
| `MultiLayerAbsoluteTravelAngle` | Effective travel angle |
| `MultiLayerNormalOffset` | Effective normal offset |
| `MultiLayerContourStartOffset` | Effective along-contour start shift |
| `MultiLayerContourOffset` | Effective contour offset |

### Process-table identity

The resolver uses these process-table fields:

| Index | Meaning |
| ---: | --- |
| 0 / 1 / 2 | Main ID / sub ID / WPS name |
| 25 / 26 | Layer / bead number |
| 29 / 30 | Work-angle / absolute travel-angle offset |
| 31 / 32 / 33 | Normal / contour-start / contour offset |
| 35 | Transient creation-time used flag |
| 37 | Data-valid flag |

Index 36 must not be used to classify Multilayer. Classification is based on more than one matching data-valid row.

## Generated-output structures

| Capability | Expected SRC | Expected DAT |
| --- | --- | --- |
| TouchSense | Search folds, correction calculation/on, correction off/clear | Search parameter, position, motion, and correction records |
| Finding | `BF_Init`, measurement folds, `BF_SetCorrData`, correction calculation/save/load, clear | `BFg_PColl_T`, six CD records per measurement, positions and motion data |
| Tracking 4.0.3 | Sensor init/on/off, optional `STTg_SearchSeamStart` | Normal tracking and Search Start `STTg_SensorSet_T` records |
| Native Multilayer | Independent `ARCON`/weld motions/`ARCOFF` for every pass | Independent points, WDAT, and WS data per pass |
| AML | `AmlBlockBegin`, layer switch/cases, root `AmlSetPos`, filler `AmlGetPos`, `AmlBlockEnd` | Root/filler WDAT, per-point AML state, `AmlInfo`, and `LayerOffsetN` |

## Multilayer diagnostics

| Code | Meaning | Normal response |
| --- | --- | --- |
| `ML001` | WPS not from process table | Use native behavior or select a named process-table WPS |
| `ML002` | Selected WPS is not Multilayer | Use native output or fix WPS rows |
| `ML003` | Stable WPS row cannot be resolved | Repair row identity; do not infer from names |
| `ML004` | Duplicate WPS name/main-ID ambiguity | Make WPS identity unique |
| `ML005` | Duplicate layer/bead coordinate | Correct the process table |
| `ML006` | Seam UUID missing | Recreate/recompute process geometry |
| `ML007` | AML option pack not configured | Configure installed flag/version or use native output |
| `ML008` | Unsupported controller/KSS/AML version | Use a validated combination or native output |
| `ML009` | More than 99 AML fillers | Split the seam/recipe or use native output |
| `ML010` | Closed-contour start shift required | Use native output |
| `ML011` | Unsupported spline/motion construct | Simplify the weld path or use native output |
| `ML012` | Unsupported TTS X offset | Remove contour-start translation or use native output |
| `ML013` | Recipe snapshot changed | Review and explicitly reapply/regenerate |
| `ML014` | Recipe source missing | Restore the WPS or preserve reviewed detached output |
| `ML015` | Cross-seam sequencing not enabled | Use `CompleteSeam` |
| `ML016` | AML/E2 simulation may differ | Perform OfficeLite/controller dry run |
| `ML017` | Reverse correction mapping unverified | Use native output for affected seam |
| `ML018` | Automatic CAD-driven WPS matching unsupported | Turn off automatic matching and select named WPS |

AML fallback is scoped per seam where possible. Another eligible seam in the same program may still use AML.
