# Attribute creation overlay

This example separates a global technology attribute from operation-level workmethod attributes and binds the latter into a `DrillingMethod` UI tab.

Merge `DrillingTechnology.py` and `DrillingMethod.py` into the corresponding callbacks of a clean R2026.1 Drilling template. Merge `Settings.fragment.xml` into the template's existing `Technology/TechTabs` node; it is not a complete `Settings.xml`. Merge both locale files into the matching language-resource dictionaries.

Expected behavior:

- `MyIntAttribute` is a technology-created process/global integer.
- `ProcGeoName`, `Has_Speed`, `Speed`, `Has_Wait`, and `Wait` are read-only operation attributes owned by the workmethod.
- `PostWmSyncPgAttributes` copies optional metadata from the current process geometry and resets missing numeric values to zero.
- English and German UI labels are resolved by exact NLS keys after restarting E2.

Static source: curated from `examples/Attribute/E2Plugin` at source commit `584ce04`. Runtime status is recorded in `spec.json`.
