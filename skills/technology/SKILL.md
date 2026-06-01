---
description: Guide for customizing FASTSUITE E2 Technology UI — attributes, tabs, events, workmethods. Use when working on files under Technologies/.
applyTo: Technologies/**/*.py
---

# E2 Technology Customization Skill

## What is a Technology?

A Technology in FASTSUITE E2 defines the process-specific behavior for a robot application (Arc Welding, Spray Painting, Handling, etc.). Technology customization scripts control:
- **Attributes**: Custom fields shown in the E2 UI (process parameters, settings)
- **Tabs**: UI tab layout in the technology editor
- **Events**: Technology-specific motion events (ArcOn/Off, GunOn/Off, etc.)
- **Workmethods**: Processing strategies and parameter sets

## Folder Structure

Technology scripts follow this layout:
```
Technologies/<TechName>/<Vendor>/Standard/Scripts/
```

Common callback scripts:
- `PostTechInitAttributes.py` — called once when technology is initialized; set up custom attributes
- `PostWmSyncPgAttributes.py` — called when workmethod syncs to program; sync attribute values

## API Reference

- **Primary context**: Obsidian vault `10_API_Reference/Technology/` (via `obsidian-e2` MCP)
- **Core objects**: Obsidian vault `10_API_Reference/OlpCore/` (via `obsidian-e2` MCP)

## Key Rules
- Logger is always a local variable: `logger = operator.GetLogOperator()`
- For enums, use `GetLiteralAttribute(name, True).GetValue()` — NOT `GetStringAttribute()`
- Use `GetAttributeByName()` when you need `SetVisibility()` — never create with `SetVisibility(False)`
- Never modify E2 core technology definitions

## Common Patterns

### Creating Attributes
```python
def PostTechInitAttributes(operator):
   # Add a string attribute
   operator.SetAttributeString("MyParam", "default_value")
   # Add a double attribute
   operator.SetAttributeDouble("Speed", 1.5)
   # Add a bool attribute
   operator.SetAttributeBool("EnableFeature", False)
```

### Reading Attributes
```python
# Generic loop (recommended)
for attr in operator.GetAttributes():
   name = attr.GetName()
   value = attr.GetValue()

# Typed getters
value = operator.GetStringAttribute("MyParam", True).GetValue()
value = operator.GetDoubleAttribute("Speed", True).GetValue()
value = operator.GetBoolAttribute("EnableFeature", True).GetValue()
```

*This skill will be expanded with more patterns and examples. Use the `obsidian-e2` MCP server to look up `Technology Callback Lifecycle` and `Workmethod Callback Lifecycle` for the full API reference.*
