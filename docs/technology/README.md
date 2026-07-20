# E2 Technology Customization

This section documents maintained patterns for FASTSUITE E2 R2026.1 technology customization. It complements the agent workflow in [`skills/technology/SKILL.md`](../../skills/technology/SKILL.md) and the production references under [`community/Technologies/`](../../community/Technologies/).

## Start here

1. Decide which layer owns the behavior: technology, workmethod, event, importer, uploader, or downloader.
2. Select the nearest R2026.1 template or community implementation.
3. Read the focused guide for the behavior:
   - [Attributes, UI, and localization](attributes-ui-localization.md)
   - [Events, rules, and compute-time generation](events-rules-compute.md)
   - [Process-geometry import and synchronization](process-geometry-import.md)
4. Use the matching teaching example under [`examples/technology/`](../../examples/technology/).
5. Complete the [R2026.1 runtime validation](runtime-validation.md) before treating the behavior as proven.

## Source authority

Use sources in this order:

1. `typings/` for locally represented Python names, signatures, and enums.
2. The Obsidian E2 API vault for Technology, Workmethod, and OlpCore lifecycle semantics not represented by local stubs.
3. The nearest R2026.1 production/community script for an established implementation pattern.
4. Runtime behavior and before/after tree dumps to settle remaining uncertainty.

The examples here are focused overlays. They intentionally do not duplicate complete technology templates. `community/Technologies/` remains the baseline source of truth.

## Knowledge capture

A knowledge-capture policy is useful because verified E2 behavior otherwise disappears into chat history. The generic policy from the source repository was not imported as a separate policy: this repository already has a more actionable milestone debrief in `.github/copilot-instructions.md`.

For Technology work, capture discoveries at the narrowest durable level:

- Cross-technology lifecycle or API pattern: update `skills/technology/` or these guides.
- Example-specific contract: update the example README or JSON specification.
- Vendor-specific behavior: update `docs/ctrl-specific/<VENDOR>/`.
- E2 platform/API discovery not yet represented locally: add an Obsidian `90_Inbox_AI` note for review.
- Unverified observation: keep it in working notes and label it as unverified; do not promote it to a rule.

This is more useful than a second generic policy because it says where each kind of Technology knowledge belongs and requires runtime evidence for behavioral claims.

## Imported material

These guides and examples are a one-time English curation of `X:\E2Git\E2CustomizingAI` at commit `584ce04`. See [provenance and corrections](provenance.md).
