# Attributes, UI, and localization

## Choose the owning scope

Create an attribute in the narrowest scope that owns its meaning:

- Technology attribute: shared technology behavior or program/global state; create it in `PostTechInitAttributes`.
- Workmethod attribute: process-method semantics and operation values; create it in `PostWmInitAttributes`.
- Event attribute: parameters owned by one event; create it in the event's `PostInitAttributes`.
- Process-geometry metadata: values imported with geometry; optionally copy them to operation attributes in `PostWmSyncPgAttributes`.

Before adding a workmethod callback, confirm that the method exists in the selected R2026.1 template. A corresponding `TechTab` in `ControllerSettings/Settings.xml` is useful evidence, but inspect the actual template and runtime rather than assuming a name creates a method.

## Use-level flags are a bitmask

The use level passed to `AddBool`, `AddDouble`, `AddInteger`, `AddString`, `AddEnum`, and related creators is composed with bitwise OR.

| Flag | Value | Intended effect |
|---|---:|---|
| `OLP_NONE` | `0` | No OLP use-level flag. Rare in customization examples. |
| `USER_ATTRIBUTE` | `1 << 0` | User-facing attribute. |
| `PROCESS_ATTRIBUTE` | `1 << 1` | Available to process/output logic. |
| `OPERATION_ATTRIBUTE` | `1 << 2` | Operation-level availability. |
| `OPERATION_GROUP_ATTRIBUTE` | `1 << 3` | Operation-group-level availability. |
| `GLOBAL_ATTRIBUTE` | `1 << 4` | Program/global-level availability. |
| `READONLY_ATTRIBUTE` | `1 << 5` | Read-only use-level flag. Prefer the established template pattern if it instead calls `SetReadOnly(True)`. |
| `CONTROLLER_ATTRIBUTE` | `1 << 6` | Controller-only availability. |

Typical combinations are:

```python
USER_ATTRIBUTE | PROCESS_ATTRIBUTE
USER_ATTRIBUTE | PROCESS_ATTRIBUTE | OPERATION_ATTRIBUTE
USER_ATTRIBUTE | PROCESS_ATTRIBUTE | READONLY_ATTRIBUTE
```

Do not copy a bitmask without checking its intended scope. In particular, `PROCESS_ATTRIBUTE` does not by itself mean "visible in the UI," and `GLOBAL_ATTRIBUTE` changes where the value is exposed.

## Create attributes through the creator

The maintained pattern is to obtain the callback's creator and call the typed `Add*` method:

```python
def PostWmInitAttributes(Operator: CENPyOlpWM_AttribInitOperator):
    creator = Operator.GetAttribCreator()
    use_level = USER_ATTRIBUTE | PROCESS_ATTRIBUTE | OPERATION_ATTRIBUTE

    speed = creator.AddDouble(
        "Speed", 0.3, 0.0, 10.0, 0.01,
        use_level, ATTRIB_SPEED, "Speed"
    )
    speed.SetReadOnly(True)
```

The final string is the NLS key in this example. Verify exact signatures against `typings/`, the Obsidian API reference, and an R2026.1 reference script because overloads vary by attribute type.

## Bind attributes into `Settings.xml`

The usual UI hierarchy is:

```text
Technology
└── TechTabs
    └── TechTab
        └── Containers
            └── Container
                └── Groups
                    └── Group
                        └── Attributes
                            └── Attribute
```

The `Attribute/@Name` value must exactly match the name passed as the first argument to `Add*`:

```xml
<Attribute Name="Speed" Order="1" Visibility="true" Icon="Velocity" />
```

Prefer extending the selected R2026.1 template's existing tab/container/group. Add a new UI branch only when the functionality needs a distinct conceptual area. Keep sibling `Order` values deterministic, and update every reference if an identifier changes. For rule-bound controls, preserve matching `Rule` and `Event` names.

## Dynamic visibility

Use the attribute-changed callback owned by the same scope as the controlling attributes. Read values through the getter, then retrieve the attribute object with `GetAttributeByName()` before calling `SetVisibility()`:

```python
def PostTechOnAttribChanged(Operator: CENPyOlpTech_AttribChangedOperator):
    getter = Operator.GetAttribGetter()
    enabled = getter.GetBool("AdvancedOptions")
    getter.GetAttributeByName("AdvancedDelay").SetVisibility(enabled)
```

Initialize dependent attributes with the intended initial visibility and make the callback idempotent: the same input state should always produce the same visibility state. Use `Operator.GetChangedAttribute()` only when limiting work to a particular trigger; recomputing a small visibility group from current values is often safer than relying on change order.

For enum/literal controls, use the literal/enum getter established by the R2026.1 API and reference scripts. Do not silently treat a literal as a string.

## NLS resources

The NLS key passed to `Add*` must exactly match `x:Key` in each language resource:

```xml
<sys:String x:Key="Speed">Speed</sys:String>
```

Expected location and naming:

```text
Technologies/<Technology>/[<Vendor>/]Standard/Scripts/Resources/Languages/
└── <locale>/<Technology>.<locale>.xaml
```

Common locales include `en-US`, `de-DE`, `fr-FR`, `ja-JP`, and `zh-CN`. New or changed language resources require an E2 restart because they are loaded at startup. Diagnose missing labels by checking, in order, the `Add*` NLS key, XAML `x:Key`, filename, technology name, locale directory, and restart.

## Verification

- Inspect the selected template and confirm the callback is loaded.
- Confirm Python names, `Settings.xml` names, and NLS keys match exactly.
- Restart E2 after resource changes.
- Exercise every controlling value and record the visibility matrix.
- Dump the resulting OLP tree and confirm type, value, use-level flags, units, read-only state, and owning level.
