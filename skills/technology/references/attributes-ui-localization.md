# Attribute, UI, and localization decision table

Read [`docs/technology/attributes-ui-localization.md`](../../../docs/technology/attributes-ui-localization.md) for the full guide.

| Question | Decision |
|---|---|
| Shared technology/program state? | `PostTechInitAttributes` |
| Selected process-method/operation state? | `PostWmInitAttributes` |
| Parameter belongs only to an event? | Event `PostInitAttributes` with `CENPyOlpEvent_AttribInitOperator` |
| Imported geometry metadata needed downstream? | Create operation attributes, then copy in `PostWmSyncPgAttributes` |
| UI and process/output access needed? | Start from `USER_ATTRIBUTE | PROCESS_ATTRIBUTE`, then add only the owning-level flag required by the reference template |
| Need runtime visibility changes? | Use the matching `*OnAttribChanged` callback and `GetAttributeByName(...).SetVisibility(...)` |
| Label missing? | Check `Add*` NLS key = XAML `x:Key`, resource filename/path, locale, then restart E2 |

Required checks:

1. Select the nearest R2026.1 template before creating files.
2. Verify the exact `Add*` signature against available authority.
3. Match Python name, `Settings.xml` name, and NLS key exactly.
4. Keep visibility logic idempotent and test every controlling state.
5. Confirm type, flags, units, read-only state, value, and owner in a tree dump.
