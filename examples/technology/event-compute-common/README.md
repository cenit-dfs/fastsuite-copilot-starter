# Shared Ultrasonic NDT event implementation

This overlay contains the event scripts shared by the two ownership examples. Copy both scripts into the selected `UltrasonicNdtTechnology/Standard/Scripts/` directory, then install exactly one owner:

- [`events-technology-owned`](../events-technology-owned/), or
- [`events-workmethod-owned`](../events-workmethod-owned/).

`FourPointApproach` creates five approach motions. It adds speed and accuracy before the first motion, inserts `SkipEvent(Skip=True)` before the camera motion, and inserts `SkipEvent(Skip=False)` after the final motion. Resource attributes `CAMERA_X`, `CAMERA_Y`, `SPRAY_X`, and `SPRAY_Y` are required.

The curated version corrects the source event name from `SKipEvent` to `SkipEvent` and types event attribute callbacks with `CENPyOlpEvent_AttribInitOperator`.
