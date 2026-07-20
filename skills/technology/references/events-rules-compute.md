# Event, rule, and compute decision table

Read [`docs/technology/events-rules-compute.md`](../../../docs/technology/events-rules-compute.md) for the full guide.

| Question | Decision |
|---|---|
| Event applies across the technology? | Register/bind in `PostTechInitEvents` and `PostTechInitRules` |
| Event applies only to one method? | Register/bind in `PostWmInitEvents` and `PostWmInitRules` |
| Event replaces a template event? | Inspect the active R2026.1 rule, then remove/add/set active in the owning callback |
| Event generates helper motions? | Event `PostCompute` owns the final generated subtree |
| Event has parameters? | Create them in event `PostInitAttributes` using `CENPyOlpEvent_AttribInitOperator` |
| Uploader-created helpers disappear? | Compare before/after compute; move behavior to the technology event if E2 regenerates it |

Required checks:

1. Keep filename, `GetEventName()`, rule event name, UUID, and nested `AddEvent()` UUID consistent.
2. Install exactly one ownership variant.
3. Validate every generated motion has a position/matrix.
4. Validate before/after insertion semantics for nested events.
5. Capture before/after-compute tree dumps and a re-download comparison.
