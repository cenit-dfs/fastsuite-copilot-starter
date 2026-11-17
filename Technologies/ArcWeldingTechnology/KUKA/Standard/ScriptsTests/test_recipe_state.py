"""Pure unit tests for MultiLayerRecipeState (spec section 17.1, item 16, and section 9.2)."""
import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Scripts"))

import MultiLayerProcessTable as process_table
import MultiLayerRecipeState as recipe_state
from _row_fixture import make_row


class Test_FingerprintDeterminism(unittest.TestCase):
    def test_same_records_produce_same_fingerprint(self):
        rows = [
            make_row({process_table.Row.LAYER_NUMBER: 0, process_table.Row.BEAD_NUMBER: 1}),
            make_row({process_table.Row.LAYER_NUMBER: 1, process_table.Row.BEAD_NUMBER: 1}),
        ]
        records = [process_table.parse_row(r) for r in rows]

        fp1 = recipe_state.compute_recipe_fingerprint(records)
        fp2 = recipe_state.compute_recipe_fingerprint(list(reversed(records)))
        self.assertEqual(fp1, fp2)

    def test_changed_process_value_changes_fingerprint(self):
        rows_a = [make_row({process_table.Row.LAYER_NUMBER: 0, process_table.Row.BEAD_NUMBER: 1})]
        rows_b = [make_row({
            process_table.Row.LAYER_NUMBER: 0, process_table.Row.BEAD_NUMBER: 1,
            process_table.Row.WELDING_SPEED: 0.02,
        })]
        records_a = [process_table.parse_row(r) for r in rows_a]
        records_b = [process_table.parse_row(r) for r in rows_b]

        self.assertNotEqual(
            recipe_state.compute_recipe_fingerprint(records_a),
            recipe_state.compute_recipe_fingerprint(records_b),
        )


class Test_RecipeStateTransitions(unittest.TestCase):
    def test_not_applicable_when_not_process_table(self):
        state = recipe_state.resolve_recipe_state(
            is_multilayer_process_table=False, source_exists=True,
            applied_fingerprint="a", current_fingerprint="a", locally_modified=False,
        )
        self.assertEqual(state, recipe_state.RecipeState.NOT_APPLICABLE)

    def test_missing_source(self):
        state = recipe_state.resolve_recipe_state(
            is_multilayer_process_table=True, source_exists=False,
            applied_fingerprint="a", current_fingerprint="a", locally_modified=False,
        )
        self.assertEqual(state, recipe_state.RecipeState.MISSING_SOURCE)

    def test_detached_when_locally_modified(self):
        state = recipe_state.resolve_recipe_state(
            is_multilayer_process_table=True, source_exists=True,
            applied_fingerprint="a", current_fingerprint="a", locally_modified=True,
        )
        self.assertEqual(state, recipe_state.RecipeState.DETACHED)

    def test_update_available_when_fingerprint_differs(self):
        state = recipe_state.resolve_recipe_state(
            is_multilayer_process_table=True, source_exists=True,
            applied_fingerprint="a", current_fingerprint="b", locally_modified=False,
        )
        self.assertEqual(state, recipe_state.RecipeState.UPDATE_AVAILABLE)

    def test_current_snapshot_when_unchanged(self):
        state = recipe_state.resolve_recipe_state(
            is_multilayer_process_table=True, source_exists=True,
            applied_fingerprint="a", current_fingerprint="a", locally_modified=False,
        )
        self.assertEqual(state, recipe_state.RecipeState.CURRENT_SNAPSHOT)


def suite():
    loader = unittest.TestLoader()
    result = unittest.TestSuite()
    result.addTests(loader.loadTestsFromTestCase(Test_FingerprintDeterminism))
    result.addTests(loader.loadTestsFromTestCase(Test_RecipeStateTransitions))
    return result


if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
