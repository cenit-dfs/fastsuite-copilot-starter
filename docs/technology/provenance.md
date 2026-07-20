# Provenance and intentional corrections

## Source

- Repository: `X:\E2Git\E2CustomizingAI`
- Source commit: `584ce04`
- Source commit date: 2026-06-22
- Curated import date: 2026-07-20
- Reuse decision: authorized by the completed [integration decision record](integration-questionnaire.md)
- Target: FASTSUITE E2 R2026.1

This is a one-time curated import, not a subtree or synchronization pipeline. English guides were synthesized from the source documentation and selected example packages. Identifiers and API calls were retained where they form runtime contracts; prose was translated and consolidated.

## Deliberately excluded

- Generated C++ API Markdown corpus: local `typings/` plus the Obsidian E2 API vault remain authoritative.
- Technology baseline corpus: `community/Technologies/` remains authoritative.
- `node_modules`, generated output, npm/PowerShell workflow conventions, and the source validator.
- The generic knowledge-capture policy: replaced by the Technology-specific routing described in this documentation and the repository milestone debrief.

## Corrections made during curation

| Source anomaly | Maintained form | Reason |
|---|---|---|
| Event name `SKipEvent` | `SkipEvent` | Event names are case-sensitive and must match registration/spec references. |
| Ultrasonic script `FILE_NAME = "DrillingTechnology.py"` | Matching Ultrasonic/owner filename | Logging and diagnostics must identify the loaded script. |
| Event `PostInitAttributes` annotated with `CENPyOlpWM_AttribInitOperator` | `CENPyOlpEvent_AttribInitOperator` | The callback receives an event attribute-init operator. |
| Full technology `Settings.xml` copied into examples | Focused XML fragments | Avoids creating a second baseline and makes merge points explicit. |
| Required API calls hidden by broad `except` blocks | Explicit guards or documented optional behavior | Required import/event failures must remain diagnosable. |

## Machine-readable specifications

The JSON specs and schemas are retained as reviewable contracts. A local Node/AJV validator is intentionally not installed because:

- the source specs already passed AJV before curation;
- the first milestone treats them as static teaching contracts, not a frequently authored CI input;
- importing AJV would introduce a new maintained dependency and lockfile for little current value;
- JSON parsing, path checks, Python compilation, and XML parsing provide useful dependency-free static checks.

Add an automated schema validator when specs become a maintained authoring workflow or CI gate. At that point, pin the validator version and validate every example in CI rather than keeping an unused local dependency.

For this one-time import, all six curated specs were validated against the three imported schemas with the source checkout's existing AJV installation; no dependency was copied into this repository. The 11 example Python files also compile under the installed E2 Python 3.12.4, and all XML/XAML files parse successfully. These are static checks, not substitutes for the pending E2 callback and tree-dump validation.
