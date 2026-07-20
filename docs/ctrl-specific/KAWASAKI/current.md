# KAWASAKI Current Changes

## 2026-07-20

- Emit `GROUP {value}` immediately after `.PROGRAM {name}()` when the program-level `GroupNumber` attribute is nonzero.
- Preserve the existing header when `GroupNumber` is zero by omitting the `GROUP` line.
- Emit `BASE {profileName}` and the corresponding `.TRANS` frame for base-profile names beginning with `ROT_BASE`; retain `BASE NULL` without a frame entry for all other base profiles.
