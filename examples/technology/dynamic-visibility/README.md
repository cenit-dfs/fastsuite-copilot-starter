# Dynamic visibility overlay

This is a reduced, vendor-neutral form of the Arc Welding/KUKA attribute-change example. It demonstrates the pattern without copying the full KUKA technology baseline.

Merge the callback and constants into the target `ArcWeldingTechnology.py`, and merge the XML group into the appropriate Arc Welding tab/container. The controlling and dependent attribute names must remain identical across Python and XML.

Visibility rules:

- `WeavePattern == "None"`: all weave details hidden.
- Any other pattern: deflection and angle visible; show length for `WeaveType == "Weave length"`, otherwise show frequency.
- `AdvancedOptions` controls the advanced delay.

The callback recomputes the complete visibility state on every change, so callback ordering cannot leave stale controls visible.
