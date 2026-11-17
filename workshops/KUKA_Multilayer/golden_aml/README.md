# AML goldens — hand-authored synthetic fixtures

These files are independent expected-output fixtures for the AML emitter. They use neutral names
and synthetic data; they are not controller-captured or production programs.

| File | Role |
| --- | --- |
| `AML01.src` / `.dat` | Higher-level caller with approach/retract and individual layer selection |
| `AML01_S01.src` / `.dat` | AML seam module with a root case and one filler case |

`compare_aml.py` compares downloaded output in `output_aml/` against these fixtures. It does not
self-compare emitter output.
