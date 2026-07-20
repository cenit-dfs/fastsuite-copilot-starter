# Kawasaki AS downloader reference

Use this reference for `community/OLPTranslators/KAWASAKI/KAWASAKI_AS.py` and for any temporary Kawasaki development copy in the starter.

## Authority and evidence

- Canonical implementation: `community/OLPTranslators/KAWASAKI/KAWASAKI_AS.py`
- Controller behavior: `docs/ctrl-specific/KAWASAKI/spec/`
- Golden output: `community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/golden/`
- OLP evidence: `community/scenarios/ArcWeldingTechnology/KAWASAKI/Standard/reference/`

Read `docs/ctrl-specific/KAWASAKI/spec/downloader-patterns.md` before changing output behavior. Update the matching specification/current note and golden coverage when behavior changes.

## Required invariants

- Convert E2 `Euler_XYZs` orientation to Kawasaki `Euler_ZYZr` OAT.
- Convert positions, contour speed, accuracy, weave width, and LT bias from metres to millimetres; leave PTP percentages and revolute joint degrees unchanged.
- Treat boolean attribute values as Python `bool`, not string values.
- Buffer SPEED, ACCEL, CP, and ACCURACY and flush them before motion output.
- Preserve the documented ArcOn and ArcWeldCondition ordering; they are intentionally different.
- Enable TRSUB only for `ROT_BASE` profiles and do not wrap joint or explicit targets.
- Emit a nonzero program `GroupNumber` immediately after `.PROGRAM`; omit zero.
- Reset all per-program state in `ProgramStart` and emit shared touch-sensing helpers only in the main file.
- Keep `.TRANS` and `.JOINTS` deterministic and omit empty sections.

## Ownership

The community file is the maintained downloader. The starter retains skills and documentation only. Promotion into an E2 release is handled through product qualification; do not create another long-lived source copy here.
