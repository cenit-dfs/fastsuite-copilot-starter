# E2 Technology Integration Decision Record

This completed questionnaire records how content from `X:\E2Git\E2CustomizingAI` was selected and integrated into this repository.

## Discovery Summary

Source inspected: `X:\E2Git\E2CustomizingAI` at commit `584ce04` (2026-06-22).

- The source repository has no `AGENTS.md`, Copilot instruction file, prompt, or `SKILL.md`. Its reusable agent knowledge must be synthesized from documentation, examples, schemas, and code.
- It contains six substantive general guides covering attribute use-levels, `Settings.xml`, NLS localization, workflow conventions, API-to-example mapping, and knowledge capture.
- It contains five machine-readable example packages: attribute creation, attribute-change visibility, technology-level events, workmethod-level event creation, and process-geometry import/attribute synchronization.
- All five JSON specifications currently pass the source repository's AJV validation.
- It contains 153 generated Markdown pages derived from C++ E2 interface headers.
- It contains 1,180 technology-baseline files. Compared with this repository's `community/Technologies`, 494 are identical, 26 differ, and 660 are absent here.
- The source repository does not identify its E2 release and has no license file. Some API extracts contain CENIT copyright notices. This repository also currently has no `LICENSE` file even though its README links to one.

## Recommended Integration Baseline

Unless you choose otherwise, the proposed integration is:

1. Translate and consolidate the durable German guidance into English under `docs/technology/`.
2. Expand `skills/technology/SKILL.md` with routing and checklists for attributes, UI configuration, localization, attribute-change callbacks, event creation, and process-geometry import.
3. Add a small curated `examples/technology/` collection with English READMEs and machine-readable specs.
4. Preserve E2 identifiers, callback names, paths, UUIDs, NLS keys, and code syntax exactly; translate explanatory prose and human-facing example text only.
5. Keep `community/Technologies` as the technology-baseline source of truth. Do not bulk-copy the source template corpus.
6. Do not import `node_modules`, generated `output/`, the C++ API-reference dump, or conflicting technology baselines until provenance, version, and ownership are confirmed.
7. Record the source commit and any intentional corrections in the imported documentation.

## Integration Decisions

### 1. Reuse and distribution permission

Do we have permission to copy, translate, modify, and redistribute the coworker's material, including CENIT-copyright API extracts and E2 technology baseline files?

- [x] Yes, all source content may be reused in this repository.
- [ ] Only the coworker's original documentation/specifications may be reused; exclude E2/CENIT source-derived files. **(Recommended until confirmed)**
- [ ] Internal use only; imported material must not be published.

Notes / owner who confirmed permission:

>

### 2. E2 version compatibility

Which E2 release was the source material and template corpus taken from?

Normalized target: FASTSUITE E2 R2026.1.

Target policy:

- [x] Normalize and validate everything against FASTSUITE E2 R2026.1. **(Recommended)**
- [ ] Preserve the source version and label version-specific content.
- [ ] Support multiple E2 releases; document differences explicitly.

### 3. Intended integration scope

- [x] Curated skill, English docs, and selected minimal examples only. **(Recommended)**
- [ ] Skill and docs only; do not import executable examples.
- [ ] Full framework migration, including schemas, validation tooling, API references, and technology templates.

Notes:

>

## Content and Architecture Questions

### 4. Technology skill organization

- [x] Expand the existing `skills/technology/SKILL.md` and keep detailed material in linked references. **(Recommended)**
- [ ] Split it into focused skills such as `technology-attributes`, `technology-events`, and `process-geometry-import`.
- [ ] Replace the existing technology skill with a translated version derived from the source repository.

Notes:

>

### 5. General documentation to import

Select the topics to translate and consolidate:

- [x] Attribute use-level flags and bitmasks. **(Recommended)**
- [x] `Settings.xml` UI hierarchy and attribute binding. **(Recommended)**
- [x] NLS localization and language-resource rules. **(Recommended)**
- [x] Attribute-change callbacks and dynamic visibility. **(Recommended)**
- [x] Event registration, rule binding, and `PostCompute` event injection. **(Recommended)**
- [x] Process-geometry importer, workmethod synchronization, and AutoExecute flow. **(Recommended)**
- [ ] PowerShell/npm workflow conventions.
- [ ] Knowledge-capture policy.

Additional topics: Explain Knowledge-capture policy - could it be useful? If not - should there be a better replacement?

>

### 6. Example packages

Which examples should become maintained English examples?

- [x] Attribute creation in technology and workmethod. **(Recommended)**
- [x] Attribute-change visibility in Arc Welding/KUKA. **(Recommended)**
- [x] Technology-level event registration and compute-time injection.
- [x] Workmethod-level event registration and compute-time injection. **(Recommended)**
- [x] Process-geometry CSV importer and optional attribute synchronization. **(Recommended)**
- [x] AutoExecute event insertion after process-geometry programming.

The source has two closely related Ultrasonic NDT event examples with different ownership: one registers rules at technology level and the other at workmethod level. Should both be retained?

- [x] Keep both as a deliberate ownership comparison. **(Recommended)**
- [ ] Keep only the workmethod-owned version.
- [ ] Keep only the technology-owned version.
- [ ] Merge them into one configurable example.

### 7. Known source anomalies

The source documents known inconsistencies such as `SKipEvent` capitalization, a mismatched `FILE_NAME`, and an event attribute callback typed with a workmethod operator.

- [x] Correct them in maintained examples and document each correction. **(Recommended)**
- [ ] Preserve examples byte-for-byte and describe the issues only.
- [ ] Exclude examples containing known anomalies.

Notes:

>

### 8. API-reference corpus

The 153 Markdown files reproduce C++ interface declarations and partially overlap with this repository's `typings/` and Obsidian MCP authority model.

- [x] Do not import them; map examples to `typings/` and Obsidian instead. **(Recommended)**
- [ ] Import only Technology/Workmethod interfaces that have no local stubs, after provenance and version review.
- [ ] Import the complete corpus as a versioned reference snapshot.

Notes:

>

### 9. Technology baseline templates

- [x] Keep `community/Technologies` authoritative and import no duplicate baseline files. **(Recommended)**
- [ ] Curate only missing technologies needed by selected examples.
- [ ] Import all 660 baselines not currently present in `community`.
- [ ] Replace or reconcile the 26 conflicting files.

If conflicts should be reconciled, who decides which runtime version is correct?

>

### 10. Machine-readable specifications and validation

- [x] Import the JSON specs/schemas, but defer the Node/AJV validator unless validation becomes a maintained workflow. **(Recommended)**
- [ ] Import the Node validator and add AJV as an approved development dependency.
- [ ] Port validation to the repository's existing Python environment without adding a package.
- [ ] Import prose documentation only; omit machine-readable specs.

Notes: Explain why a validator isn't needed

>

### 11. Destination layout

- [x] `docs/technology/` for guides, `examples/technology/` for teaching examples, and `skills/technology/references/` for agent-only decision tables. **(Recommended)**
- [ ] Keep all imported material under `Technologies/`.
- [ ] Mirror the source repository's `docs/`, `examples/`, `templates/`, and `input/` structure.

Notes:

>

### 12. English translation policy

- [x] English-only narrative; preserve German locale files as localization examples. **(Recommended)**
- [ ] English narrative plus the original German documents side-by-side.
- [ ] English skill only; retain German example READMEs.

Terminology preferences, if any:

>

### 13. Provenance and ongoing synchronization

- [x] One-time curated import with source path, commit, and translation notes recorded. **(Recommended)**
- [ ] Maintain a repeatable synchronization/conversion script.
- [ ] Add the source repository as a submodule or subtree.
- [ ] Omit source attribution from individual files and mention it only once centrally.

Notes:

>

### 14. Intended audience

- [ ] Project engineers who need guided, safe customization workflows. **(Recommended)**
- [ ] Experienced E2 framework developers who need comprehensive API detail.
- [x] Both; provide beginner guides plus deeper reference sections.

Notes:

>

### 15. Runtime validation and definition of done

Which validation environment is available after integration?

- [x] FASTSUITE E2 R2026.1 is available for UI and callback testing.
- [ ] Static review and schema validation only.
- [ ] A coworker will run the examples in E2 and return results.

For the first integration milestone, which outcomes are required?

- [x] English docs are reviewed for technical meaning.
- [x] Skills route agents to the correct owning layer and references.
- [x] Machine-readable specs validate.
- [ ] Selected examples run in E2.
- [x] Tree dumps confirm generated attributes/events/motions.

Additional acceptance criteria:

>

## Optional Priorities

Rank the first three areas (`1` = first):

- [1] Attribute creation, use-levels, and UI placement
- [2] Dynamic visibility and attribute-change callbacks
- [3] Event registration and rule binding
- [4] Compute-time motion/event generation
- [7] Process-geometry import and attribute synchronization
- [5] NLS localization
- [6] Technology template selection

Other requirements or concerns:

>
