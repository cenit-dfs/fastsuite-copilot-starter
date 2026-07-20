# Technologies

Place your technology customization scripts here.

## Structure

```
Technologies/
├── <TechName>/
│   └── <Vendor>/
│       └── Standard/
│           └── Scripts/
│               ├── PostTechInitAttributes.py
│               ├── PostWmSyncPgAttributes.py
│               └── ...
└── .instructions.md                   # Auto-applied coding rules
```

## Getting Started

1. Select the nearest FASTSUITE E2 R2026.1 template or `community/Technologies/` reference.
2. Read `skills/technology/SKILL.md` and its task-specific reference.
3. Use `docs/technology/` for maintained explanations and `examples/technology/` for focused overlays.
4. Use the `obsidian-e2` MCP server to look up `Technology Callback Lifecycle` or `Workmethod Callback Lifecycle` when local stubs are incomplete.
5. Validate the behavior in E2 and retain a before/after tree dump.

Do not copy an entire teaching overlay over a production technology. Merge the smallest callback, settings, and resource changes into the selected template.
