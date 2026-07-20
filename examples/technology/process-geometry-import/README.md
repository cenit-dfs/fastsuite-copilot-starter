# Process-geometry CSV import overlay

This example demonstrates the complete data path selected in the questionnaire:

```text
CSV modifier/move rows
  -> process geometry and point metadata
  -> workmethod operation attributes
  -> AutoExecute speed/dwell events
```

## Files

- `config.xml`, `InitPkg.py`, and `PGImport.py` form the importer package. Install their containing directory as `ProcessGeometryImporter/GenericPoint/`, matching the module name used by `InitPkg.py`.
- `DrillingMethod.py` is the workmethod attribute/sync overlay.
- `PostProgramProcessGeometries.py` is the optional AutoExecute overlay.
- `fixture.csv` exercises a point with modifiers, a point without modifiers, and explicit zero values.

The source uses millimetres and degrees. The importer converts positions to metres and assumes `R = Rx * Ry * Rz`; local X becomes the tangent and local Y becomes the normal. `Speed` and `Wait` rows apply only to the following `Move` and are then cleared.

The AutoExecute example is deliberately one-shot: running it repeatedly can add duplicate built-in events. A production deployment must either guarantee a single execution phase or add duplicate detection using APIs verified for the target R2026.1 template.

Merge these files into a clean template and run the validation matrix in [`docs/technology/runtime-validation.md`](../../../docs/technology/runtime-validation.md). The importer API is CLR-hosted and cannot be meaningfully executed in normal CPython.
