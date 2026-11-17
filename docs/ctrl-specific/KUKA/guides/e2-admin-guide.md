# KUKA Arc Welding E2 Administrator Guide

This guide covers the E2-side setup required for KUKA TouchSense, SeamTech Finding, SeamTech Tracking, and ArcTech Multilayer workflows. It is for E2 administrators and project engineers who deploy the customization, align it with a controller project, and maintain project-specific mappings.

It does not replace KUKA installation, licensing, safety, sensor calibration, or option-package commissioning instructions.

## Configuration ownership

| Item | Owner | Source of truth |
| --- | --- | --- |
| KUKA option-package installation and license | KUKA/controller administrator | Controller and WorkVisual project |
| KSS and option-package version attributes | E2 administrator | E2 controller user-defined attributes, matched to the controller project |
| Sensor calibration, datasets, task numbers, correction IDs | Commissioning engineer | Validated controller project |
| E2 controller, tools, bases, and sensor frames | E2 administrator | Customer E2 cell/project |
| Finding recipe and sensor-channel mapping | Project engineer | E2 KUKA technology JSON files |
| Multilayer pass recipe | Welding/process engineer | ControllerBuilder process table |
| Generated KRL structure | KUKA downloader | `KUKA_KRC5_Arc_Welding.py` |
| Operation-specific values | OLP programmer | E2 program/operation attributes |

## Delivered components

The customization is split by responsibility:

| Path | Purpose |
| --- | --- |
| `OLPTranslators/KUKA/KUKA_KRC5_Arc_Welding.py` | KUKA SRC/DAT generation |
| `Technologies/ArcWeldingTechnology/KUKA/Standard/ControllerSettings/Settings.xml` | Technology tab layout and attribute exposure |
| `Technologies/ArcWeldingTechnology/KUKA/Standard/Scripts/` | Attribute creation, event generation, WPS resolution, planning, AML projection, and diagnostics |
| `Technologies/ArcWeldingTechnology/KUKA/Standard/TechTabs/SeamFind_Recipes.json` | Project-specific scan-to-correction recipes |
| `Technologies/ArcWeldingTechnology/KUKA/Standard/TechTabs/SeamFind_Sensor_Profiles.json` | Project-specific sensor CD-channel profiles |
| `Technologies/ArcWeldingTechnology/KUKA/Standard/Scripts/Resources/Languages/` | Multilayer labels and literals |

Do not deploy or modify E2 installation bootstrap files, core downloader/uploader files, or FASTSUITE site-packages. Keep customer changes in the vendor technology and translator folders.

## Establish the version baseline

Record the following before deployment:

- E2 release.
- KUKA controller family and KSS version.
- ArcTech, ArcTech Advanced, and ArcTechSense versions.
- TouchSense version.
- SeamTech Finding version.
- SeamTech Tracking version.
- ArcTech Multilayer version, when used.
- Controller-side sensor datasets, task numbers, and correction-data conventions.

### Configure controller version attributes

Store the installed KSS and KUKA option-package versions as **string** attributes on the E2 controller under **User defined attributes**. A non-empty controller attribute overrides the corresponding fallback embedded in the downloader. The effective values are written to the generated SRC header and are also used by version-dependent Finding and Tracking output branches.

Use the exact, case-sensitive attribute names:

| Controller attribute | Downloader fallback when missing or empty |
| --- | --- |
| `KssVersion` | `8.7` |
| `ArcTechVersion` | `3.4.5.6` |
| `ArcTechAdvVersion` | `3.4.5.6` |
| `ArcTechSenseVersion` | `3.5.1.21` | `3.7.1` |
| `TouchSenseVersion` | `3.8.1.0` | `3.8.1.0` |
| `SeamTechFindingVersion` | `3.8.1.0` | `4.0.3` |
| `SeamTechTrackingVersion` | `3.8.1.0` | `4.0.3` |

Enter option-package versions as three or four numeric components separated by periods, for example `4.0.3` or `3.7.2.112`. `KssVersion` must contain at least major and minor components; only those first two components are emitted. The screenshot is illustrative and does not show `TouchSenseVersion`; add it when TouchSense is installed and used.

After changing a version attribute:

1. Re-download a controlled fixture.
2. Confirm the effective versions in the generated SRC header.
3. Verify that Finding and Tracking output uses the syntax expected by the installed option-package versions.
4. Repeat the applicable OfficeLite or controller-load validation before releasing the configuration.

Do not use the embedded fallback as evidence of the installed controller option. The fallback only keeps generation possible when an attribute is absent; the E2 controller attributes should match the commissioned WorkVisual/controller project.

The bundled KUKA manuals are older or equal reference documents, not proof that every later controller build has identical syntax:

- [KUKA.TouchSense 3.2.2 manual](https://xpert.kuka.com/service-express/portal/project1_p/document/kuka-project1_p-common_PB12250_en?context=%7B%22filter%22%3A%7B%7D%2C%22text%22%3A%22KUKA.TouchSense%203.2.2%20manual%22%2C%22page%22%3A32%7D)
- [KUKA.SeamTech Finding 4.0.3 manual](https://xpert.kuka.com/service-express/portal/project1_p/document/kuka-project1_p-common_PB22249_en?context=%7B%22filter%22%3A%7B%7D%2C%22text%22%3A%22KUKA.SeamTech%20Finding%204.0.3%20manual%22%2C%22page%22%3A39%7D)
- [KUKA.SeamTech Tracking 4.0.3 manual](https://xpert.kuka.com/service-express/portal/project1_p/document/kuka-project1_p-common_PB21432_en?context=%7B%22filter%22%3A%7B%7D%2C%22text%22%3A%22KUKA.SeamTech%20Finding%204.0.3%20manual%22%2C%22page%22%3A39%7D)
- [KUKA.ArcTech Multilayer 3.7.1 manual](https://xpert.kuka.com/service-express/portal/project1_p/document/kuka-project1_p-common_PB22944_en?context=%7B%22filter%22%3A%7B%7D%2C%22text%22%3A%22KUKA.ArcTech%20Multilayer%203.7.1%20manual%22%2C%22page%22%3A35%7D)

The manuals can also be obtained via KUKA WorkVisual controller backup incl. option packs (KOP files) in case no KUKA account is available.

## Deploy the customization

1. Back up the currently deployed KUKA Arc Welding technology and translator customization.
2. Record the active files and checksums so rollback can restore one coherent version.
3. Deploy the KUKA technology folder and KUKA downloader as one tested set.
4. Preserve project-specific JSON mappings unless the new release explicitly changes their schema.
5. Restart E2. Python sibling modules and language resources are cached and are not reliably refreshed by reopening a program.
6. Open a KUKA Arc Welding project and confirm that the technology initializes without errors.
7. Verify the expected controls in Programming defaults and operation attributes.
8. Download one approved fixture for each enabled capability and compare its SRC/DAT structure with the validated baseline.

Never mix a new technology script set with an older downloader during validation. The operation metadata and generated syntax form one contract.

## Configure shared Arc Welding defaults

In the customer template or project defaults:

1. Select the intended KUKA controller and Arc Welding technology.
2. Verify welding tools, bases, TCPs, and workpiece frames.
3. Configure the WPS behavior and approved default WPS.
4. Configure laser FOV translation and rotation from the validated sensor geometry.
5. Set conservative default sensing and tracking limits.
6. Save the template only after a representative generated program loads in the target validation environment.

Changing a global default does not prove existing operations were updated. Recompute or recreate a controlled operation and inspect its effective values.

## Configure TouchSense

Align the E2 sensor selector with the controller project:

| E2 setting | Controller-side dependency |
| --- | --- |
| `SensorIdTouch` | Touch sensor dataset/tool configuration |
| `SensorIdPoint` | Point-laser sensor dataset |
| `SensorIdLine` | Line-laser sensor dataset |
| `CalibrationFrameSelection` | Calibrated tool/sensor frame |
| `TSConnectionType` | Required KUKA correction connection strategy |

Validate at least a 1D correction and the project maximum correction dimensionality. For linked TouchSense, verify current output routing `1 -> Z`, `2 -> Y`, `3 -> X` and the final `TS_BC6DCalc(Z1,Z2,Z3,Y1,Y2,X1)` argument order.

## Configure SeamTech Finding

### Sensor names and profiles

Keep sensor display names and mount profiles in the same `SeamFind_Sensor_Profiles.json` file as separate top-level collections:

```json
{
  "sensors": [
    {"id": 1, "display_name": "LineLaser"}
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

`sensors` mirrors optional WorkVisual display text by integer sensor ID. It does not select the executable sensor; `SensorIdLine` remains authoritative for `SensorNo` and `BF_Init`. Missing mappings omit the label. Duplicate or invalid IDs and unsafe fold text stop generation. The delivered `Sample_*` profiles are templates; their names and CD mappings are not universal controller defaults.

### Finding recipes

Edit `SeamFind_Recipes.json` to define scan count/order and how each scan contributes to X, Y, and Z correction. Use only profile placeholders `<ALONG>`, `<LATERAL>`, and `<HEIGHT>` in CD parameters.

After editing either JSON file:

1. Parse the JSON with a standard JSON validator.
2. Confirm profile and recipe names are unique.
3. Confirm sensor IDs are unique and display names match WorkVisual.
4. Confirm every recipe `scan_ops` entry has matching correction references and legal X/Y/Z bucket counts: X `0/1`, Y `0/1/2`, Z `0/1/3`.
5. Restart E2 or reload the technology through the approved site procedure.
6. Reopen Programming defaults and verify the new literals.
7. Generate and inspect one program per changed recipe, including one `BF_ClearSensor()` after calculation and a final `BF_CorrOff()` after corrected motion.

The technology loads these files during initialization. Editing them while a technology instance is active does not reliably refresh its literals.

## Configure SeamTech Tracking

Align two separate controller datasets:

- The normal tracking set, identified by `KukaTrackingSetId` and the seam/task number.
- The Search Start set, identified by `KukaSearchStartSetId` and its own task number and limits.

For Tracking 4.0.3, verify that the controller project provides the structures and calls used by `STTg_SensorInit`, `STTg_SensorOn`, `STTg_SearchSeamStart`, and `STTg_SensorOff`. The 4.0.3 output intentionally omits legacy `STT_PrepareWeave` and `STT_SensorWeave` helpers.

OfficeLite validates declarations and syntax but does not emulate the physical laser sensor. Schedule a real-cell reduced-speed acceptance test for Search Start direction, offset sign, correction limits, error reaction, and offset retention.

## Configure Multilayer

### Maintain the process table

Use ControllerBuilder's Arc Welding process table. `TechTabs/Multilayer.csv` is deprecated and must not be maintained as a parallel recipe source.

For every named Multilayer WPS:

1. Use one stable WPS name and main ID.
2. Create one data-valid row per pass.
3. Assign layer and bead/pass numbers.
4. Maintain process values and geometric offsets for every row.
5. Avoid duplicate `(layer, bead)` pairs within one seam recipe.
6. Review the order in which E2 creates operations from the rows.

A WPS is classified as Multilayer when it has more than one matching data-valid row. Process-table column 36 is not a usable Multilayer flag.

### Configure E2 selection

- Set `WPSAutomatic` to false for the implemented named-WPS path.
- Select the recipe through `WPSAutomaticNames`/the **WPS** dropdown.
- Use `E2NativePaths` as the conservative default.
- Set `KukaArcTechMultilayerInstalled` only when the target controller project contains the option pack.
- Set `KukaArcTechMultilayerVersion` to the installed version.
- Enable `KukaArcTechMultilayer` only after an AML fixture loads successfully.

The installed flag is explicit configuration. E2 does not probe the physical controller for the option package.

### Understand current planning controls

| Control | Current behavior |
| --- | --- |
| `CompleteSeam` | Executes all ordered passes of one seam before the next seam |
| `LayerBeadAcrossSeams` | Not production-ready; downloader forces `CompleteSeam` and reports `ML015` |
| `SameDirection` | All passes follow the source direction |
| `Alternating` | Direction changes once per distinct layer number within each seam |
| `ZigZag` | Direction changes every pass; use native output because KUKA AML is layer-oriented |

Unsupported AML content falls back per seam to native output with an `ML0xx` diagnostic. A fallback is a controlled result, not permission to ignore the warning.

## Acceptance test

For every release or project-specific configuration change:

1. Generate TouchSense, Finding, Tracking, native Multilayer, and AML fixtures for the enabled features.
2. Confirm expected option-package version headers and inline-form providers.
3. Compare SRC and DAT together; declaration changes can invalidate unchanged-looking SRC.
4. Load the files in OfficeLite or the target controller environment.
5. Perform real-cell tests for physical sensing/tracking behavior where applicable.
6. Record the exact versions, fixture names, result, and validation tier.
7. Retain the accepted output as a project golden only after sensitive customer data is removed.

Use the [Troubleshooting and Validation](troubleshooting-validation.md) evidence matrix to describe what each test proves.

## Rollback

If initialization, UI, generation, or controller-load validation fails:

1. Stop using the changed technology for production downloads.
2. Capture the E2 log, generated SRC/DAT, active version matrix, and changed JSON/configuration files.
3. Restore the translator and technology from the same previous baseline.
4. Restore the previous project JSON files if their schema or literals changed.
5. Restart E2.
6. Regenerate a known fixture and compare it with the previous accepted output.

Do not roll back only one script from a coordinated technology/downloader change.
