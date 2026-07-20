# Technology teaching examples

These focused overlays demonstrate FASTSUITE E2 Technology customization patterns without duplicating complete technology templates.

| Example | Pattern |
|---|---|
| [`attribute-creation`](attribute-creation/) | Technology/workmethod attributes, use-levels, UI placement, and NLS |
| [`dynamic-visibility`](dynamic-visibility/) | Attribute-change callback and dependent visibility |
| [`events-technology-owned`](events-technology-owned/) | Technology-wide event registration and rule binding |
| [`events-workmethod-owned`](events-workmethod-owned/) | Method-scoped event registration and rule binding |
| [`event-compute-common`](event-compute-common/) | Shared event attributes, motions, and nested event injection |
| [`process-geometry-import`](process-geometry-import/) | CSV point import, workmethod sync, and AutoExecute insertion |

## How to use an overlay

1. Start from the nearest FASTSUITE E2 R2026.1 technology template.
2. Merge only the callback bodies and XML/resources required by the example.
3. For event examples, install one ownership variant plus `event-compute-common`; never install both ownership variants.
4. Resolve all identifiers against the target template and the authoritative API sources.
5. Follow [`docs/technology/runtime-validation.md`](../../docs/technology/runtime-validation.md) and retain the resulting tree dump.

The `expected-tree.yaml` files are assertions to check, not captured runtime evidence. Replace or accompany them with an actual R2026.1 dump after validation.

Machine-readable JSON specifications are retained as review contracts. Their schemas live under [`schemas/`](schemas/). No local AJV dependency is required until schema validation becomes a CI or regular authoring workflow.
