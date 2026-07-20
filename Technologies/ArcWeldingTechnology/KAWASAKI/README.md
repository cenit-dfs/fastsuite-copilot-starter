# Kawasaki Arc Welding overlay

This directory contains only the project-owned files that extend the community Kawasaki Arc Welding technology for upload support and multiline text editing.

Use `community/Technologies/ArcWeldingTechnology/KAWASAKI/` as the baseline. Overlay these local files when deploying the customization:

- `ArcWeldingTechnology.py` — imports the upload utilities and declares upload header/footer attributes.
- `DefaultUploadMethod.py` — registers upload-side events and rule bindings.
- `TextEvent.py` — adds multiline text-event editing.
- `UploadFlags.py` — carries upload header/footer metadata.
- `UploadUtils.py` — shared multiline editor helpers.

Files that are byte-identical to the community baseline are deliberately not duplicated here.
