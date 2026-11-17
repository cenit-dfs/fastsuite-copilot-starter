"""Aggregate test suite for the Multilayer pure domain model (Phase A evidence gate).

Run with: python TestSuite.py
"""
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test_process_table import suite as process_table_suite
from test_planner import suite as planner_suite
from test_recipe_state import suite as recipe_state_suite
from test_diagnostics import suite as diagnostics_suite
from test_metadata import suite as metadata_suite
from test_aml_capability import suite as aml_capability_suite
from test_aml_emitter import suite as aml_emitter_suite


def suite():
    result = unittest.TestSuite()
    result.addTests(process_table_suite())
    result.addTests(planner_suite())
    result.addTests(recipe_state_suite())
    result.addTests(diagnostics_suite())
    result.addTests(metadata_suite())
    result.addTests(aml_capability_suite())
    result.addTests(aml_emitter_suite())
    return result


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    outcome = runner.run(suite())
    sys.exit(0 if outcome.wasSuccessful() else 1)
