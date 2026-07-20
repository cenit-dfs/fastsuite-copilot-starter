# Events, rules, and compute-time generation

## Separate registration, binding, and computation

Python technology events have three distinct responsibilities:

1. Register the event script so E2 knows it exists.
2. Add the event to a rule and select the active event where appropriate.
3. Let the event script create attributes and generate motions/events in `PostCompute`.

Do not collapse these responsibilities into downloader or uploader parsing. If E2 regenerates helper motions after compute, the event script owns the final tree shape.

## Choose technology or workmethod ownership

Use technology-level registration when the event and rule selection apply across the technology:

```python
def PostTechInitEvents(Operator: CENPyOlpTech_EventInitOperator):
    Operator.RegisterPyTechnologyEvent("FourPointApproach.py")
    Operator.RegisterPyTechnologyEvent("SkipEvent.py")


def PostTechInitRules(Operator: CENPyOlpTech_RuleInitOperator):
    Operator.AddPyEvent("ApproachRule", "FourPointApproach")
    Operator.SetActivePyEvent("ApproachRule", "FourPointApproach")
```

Use workmethod-level registration when only a selected method should expose or activate the event:

```python
def PostWmInitEvents(Operator: CENPyOlpWM_EventInitOperator):
    Operator.RegisterPyTechnologyEvent("FourPointApproach.py")
    Operator.RegisterPyTechnologyEvent("SkipEvent.py")


def PostWmInitRules(Operator: CENPyOlpWM_RuleInitOperator):
    Operator.AddPyEvent("ApproachRule", "FourPointApproach")
    Operator.SetActivePyEvent("ApproachRule", "FourPointApproach")
```

The calls look similar; lifecycle and availability differ. Do not register the same ownership path at both levels. If replacing a default event, remove the existing binding only when the selected R2026.1 template requires it.

## Event identity is a contract

Keep these identifiers stable and mutually consistent:

- `GetEventName()` return value
- Python filename registered by the technology or workmethod
- event name added to the rule
- UUID returned by `GetEventUuId()`
- event UUID passed to `AddEvent()` for nested event injection
- `Rule`/`Event` references in `Settings.xml`

Names are case-sensitive. A typo such as `SKipEvent` creates a different identifier from `SkipEvent`.

## Event attributes

Event attributes belong to `CENPyOlpEvent_AttribInitOperator`, not the Technology or Workmethod attribute operator:

```python
def PostInitAttributes(Operator: CENPyOlpEvent_AttribInitOperator):
    creator = Operator.GetAttribCreator()
    skip = creator.AddBool(
        "Skip", True, USER_ATTRIBUTE | PROCESS_ATTRIBUTE, "Skip"
    )
    skip.SetReComputeEnterState(ENTERSTATE_NORECOMPUTE)
```

Verify recompute behavior deliberately. Use `ENTERSTATE_COMPLETE` only for values that must trigger a complete event recomputation.

## `PostCompute` owns generated structure

An event's `PostCompute` can:

- derive matrices from the reference toolpath element,
- insert PTP or linear motions,
- add speed and accuracy events around those motions,
- inject another event by UUID and set its parameters.

Insertion position is part of the contract. For example, a skip-on event before a generated move and a skip-off event after the final move produce different execution semantics from attaching both to the same side.

Defensive requirements:

- Validate resource lookup results before using offsets.
- Ensure each generated motion has a valid matrix/position.
- Keep UUIDs stable once deployed.
- Make units explicit; E2 geometry commonly uses metres while source formats may use millimetres.
- Avoid swallowing exceptions around required event or motion creation.

## Ownership comparison

The two Ultrasonic NDT teaching examples intentionally use the same event implementation with different owners:

- [`events-technology-owned`](../../examples/technology/events-technology-owned/): event availability is technology-wide.
- [`events-workmethod-owned`](../../examples/technology/events-workmethod-owned/): event availability is limited to the Point workmethod.

Use the comparison to choose an owner, not as a reason to install both variants together.

## Verification

Capture a tree dump before and after technology compute. Confirm:

- the event is registered once and is available on the intended rule,
- the intended event is active,
- event-level attributes have the expected types and values,
- generated motions appear in deterministic order and each has a position,
- speed/accuracy/nested events appear at the intended insertion side,
- re-download preserves or predictably regenerates the same semantic structure.
