# R2026.1 runtime validation

Static review can establish naming consistency and callback intent, but Technology lifecycle behavior must be confirmed in FASTSUITE E2 R2026.1.

## Validation matrix

| Area | Exercise in E2 | Tree-dump evidence |
|---|---|---|
| Attribute creation | Load technology/workmethod and create an operation | Attribute name, type, value, unit, use-level flags, read-only state, owning level |
| Dynamic visibility | Change every controlling enum/bool combination | Attribute values plus screenshots or an explicit visibility matrix |
| Event registration | Open the relevant rule for technology-owned and workmethod-owned variants separately | Registered/active event identity and rule ownership |
| Event compute | Compute an operation containing `FourPointApproach` | Five generated motions, positions, speed/accuracy events, and `SkipEvent` insertion order |
| Localization | Start E2 in `en-US` and `de-DE` after a restart | Correct labels for matching NLS keys |
| PG import/sync | Import the fixture CSV and program it | Process points, metadata, operation attributes, and generated speed/dwell events |

## Procedure

1. Install one example overlay into a clean R2026.1 template copy. Do not install both event-ownership variants together.
2. Restart E2 when scripts or language resources require reload.
3. Use `community/OLPTranslators/Simple_Python_Translator.py` for the first full-tree inspection.
4. Use `OLPTranslators/TreeDumper.py` when a deterministic YAML comparison is needed.
5. Store the input fixture, resulting dump, and observed E2 build together.
6. Compare actual output with the example's `expected-tree.yaml`; update the expected file only after reviewing the semantic difference.

## Current status

The imported examples have been statically reviewed and normalized for the R2026.1 target. Their specs describe expected behavior, but runtime tree dumps must be captured in an E2 session before the examples are promoted from teaching overlays to validated production references.
