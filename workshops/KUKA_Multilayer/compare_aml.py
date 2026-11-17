"""Compare AML downloader output against the hand-authored AML golden.

Unlike the native goldens, these were written by hand before any emitter existed (spec
section 16 phase D, anti-circularity rule). A failure here means the emitter disagrees with
expected structure from the hand-authored synthetic fixtures -- fix the
emitter, or add a reconciliation row justifying a change to the golden. Never regenerate the
golden from the emitter. Run from the repository root:

    python workshops/KUKA_Multilayer/compare_aml.py
"""
import os
import sys

import compare_native

HERE = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    sys.exit(compare_native.main(
        goldenDir=os.path.join(HERE, "golden_aml"),
        outputDir=os.path.join(HERE, "output_aml"),
    ))
