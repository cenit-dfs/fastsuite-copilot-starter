"""Compare native downloader output against the Phase C golden capture.

Spec section 17.3 permits normalizing only known-nondeterministic values. The KRL header
CREATE/MODIFIED timestamps are the sole such value observed; everything else must match
byte for byte. Run from the repository root:

    python workshops/KUKA_Multilayer/compare_native.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GOLDEN_DIR = os.path.join(HERE, "golden")
OUTPUT_DIR = os.path.join(HERE, "output")

TIMESTAMP_LINE = re.compile(r"^\s*;\s*(CREATE|MODIFIED)\s*=\s*DATE\b.*$")


def normalize(path):
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return [
            "; <normalized timestamp>" if TIMESTAMP_LINE.match(line) else line.rstrip("\r\n")
            for line in handle
        ]


def main(goldenDir=GOLDEN_DIR, outputDir=OUTPUT_DIR):
    goldens = sorted(f for f in os.listdir(goldenDir) if os.path.splitext(f)[1].lower() in (".src", ".dat"))
    if not goldens:
        print("No golden files found in " + goldenDir)
        return 1

    failures = 0
    for name in goldens:
        outputPath = os.path.join(outputDir, name)
        if not os.path.exists(outputPath):
            print("MISSING  %s (not downloaded)" % name)
            failures += 1
            continue

        expected = normalize(os.path.join(goldenDir, name))
        actual = normalize(outputPath)
        if expected == actual:
            print("OK       %s" % name)
            continue

        failures += 1
        print("DIFF     %s" % name)
        for index in range(max(len(expected), len(actual))):
            exp = expected[index] if index < len(expected) else "<eof>"
            act = actual[index] if index < len(actual) else "<eof>"
            if exp != act:
                print("    line %d\n      golden: %s\n      output: %s" % (index + 1, exp, act))

    print("\n%d file(s) compared, %d differing." % (len(goldens), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
