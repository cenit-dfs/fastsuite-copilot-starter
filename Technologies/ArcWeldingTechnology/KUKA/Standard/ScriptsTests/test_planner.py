"""Pure unit tests for MultiLayerPlanner (spec section 17.1, items 6-13, 15)."""
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Scripts"))

import MultiLayerPlanner as planner


def make_pass(seam_uuid, layer, bead, ordinal, main_id=100, sub_id=1, override=planner.DirectionOverride.INHERIT_PROGRAM):
    return planner.PassInput(
        seam_uuid=seam_uuid,
        wps_main_id=main_id,
        wps_sub_id=sub_id,
        wps_name="WPS_A",
        layer=layer,
        bead=bead,
        source_operation=object(),
        source_operation_ordinal=ordinal,
        recipe_fingerprint="fp-%s-%d-%d" % (seam_uuid, layer, bead),
        direction_override=override,
    )


class Test_SortAndFlatten(unittest.TestCase):
    def test_sorts_by_layer_bead_ordinal(self):
        entries = [
            make_pass("seam-1", layer=1, bead=2, ordinal=5),
            make_pass("seam-1", layer=0, bead=1, ordinal=1),
            make_pass("seam-1", layer=1, bead=1, ordinal=3),
        ]
        ordered = planner.sort_seam_passes(entries)
        self.assertEqual([(p.layer, p.bead) for p in ordered], [(0, 1), (1, 1), (1, 2)])

    def test_flattens_wps_layer_bead_to_0_n(self):
        entries = [
            make_pass("seam-1", layer=0, bead=1, ordinal=1),
            make_pass("seam-1", layer=1, bead=1, ordinal=2),
            make_pass("seam-1", layer=1, bead=2, ordinal=3),
        ]
        plan = planner.build_multilayer_plan(
            entries, "E2NativePaths", planner.SequenceMode.COMPLETE_SEAM, planner.DirectionMode.SAME_DIRECTION,
        )
        flat_indices = [p.flat_index_in_seam for p in plan.seams[0].passes]
        self.assertEqual(flat_indices, [0, 1, 2])

    def test_detects_duplicate_layer_bead(self):
        entries = [
            make_pass("seam-1", layer=1, bead=1, ordinal=1),
            make_pass("seam-1", layer=1, bead=1, ordinal=2),
        ]
        duplicates = planner.find_duplicate_layer_bead(entries)
        self.assertEqual(duplicates, [(1, 1)])


class Test_SeamOrderAndExecution(unittest.TestCase):
    def test_preserves_original_seam_order(self):
        entries = [
            make_pass("seam-B", layer=0, bead=1, ordinal=1),
            make_pass("seam-A", layer=0, bead=1, ordinal=2),
        ]
        grouped = planner.group_by_seam(entries)
        self.assertEqual([uuid for uuid, _ in grouped], ["seam-B", "seam-A"])

    def test_complete_seam_execution_order(self):
        entries = [
            make_pass("seam-A", layer=0, bead=1, ordinal=1),
            make_pass("seam-A", layer=1, bead=1, ordinal=2),
            make_pass("seam-B", layer=0, bead=1, ordinal=3),
        ]
        plan = planner.build_multilayer_plan(
            entries, "E2NativePaths", planner.SequenceMode.COMPLETE_SEAM, planner.DirectionMode.SAME_DIRECTION,
        )
        self.assertEqual([p.seam_uuid for p in plan.execution], ["seam-A", "seam-A", "seam-B"])

    def test_layer_bead_across_seams_skips_missing_coordinates(self):
        entries = [
            make_pass("seam-A", layer=0, bead=1, ordinal=1),
            make_pass("seam-A", layer=1, bead=1, ordinal=2),
            make_pass("seam-B", layer=0, bead=1, ordinal=3),
            # seam-B has no (1, 1) pass - must be skipped, not renumbered.
        ]
        plan = planner.build_multilayer_plan(
            entries, "E2NativePaths", planner.SequenceMode.LAYER_BEAD_ACROSS_SEAMS, planner.DirectionMode.SAME_DIRECTION,
        )
        execution_keys = [(p.seam_uuid, p.layer, p.bead) for p in plan.execution]
        self.assertEqual(execution_keys, [("seam-A", 0, 1), ("seam-B", 0, 1), ("seam-A", 1, 1)])


class Test_Direction(unittest.TestCase):
    def test_zigzag_alternates_continuously_across_seam_boundary(self):
        entries = [
            make_pass("seam-A", layer=0, bead=1, ordinal=1),
            make_pass("seam-A", layer=1, bead=1, ordinal=2),
            make_pass("seam-B", layer=0, bead=1, ordinal=3),
            make_pass("seam-B", layer=1, bead=1, ordinal=4),
        ]
        plan = planner.build_multilayer_plan(
            entries, "E2NativePaths", planner.SequenceMode.COMPLETE_SEAM, planner.DirectionMode.ZIGZAG,
        )
        directions = [p.direction for p in plan.execution]
        self.assertEqual(directions, [
            planner.Direction.FORWARD, planner.Direction.REVERSE,
            planner.Direction.FORWARD, planner.Direction.REVERSE,
        ])

    def test_alternating_flips_once_per_layer_not_per_pass(self):
        # Layer 1 has two beads (both must share Forward); layer 2 flips to Reverse.
        entries = [
            make_pass("seam-A", layer=1, bead=1, ordinal=1),
            make_pass("seam-A", layer=1, bead=2, ordinal=2),
            make_pass("seam-A", layer=2, bead=1, ordinal=3),
        ]
        plan = planner.build_multilayer_plan(
            entries, "E2NativePaths", planner.SequenceMode.COMPLETE_SEAM, planner.DirectionMode.ALTERNATING,
        )
        directions = [p.direction for p in plan.execution]
        self.assertEqual(directions, [
            planner.Direction.FORWARD, planner.Direction.FORWARD, planner.Direction.REVERSE,
        ])

    def test_alternating_is_scoped_per_seam_not_by_flat_position(self):
        # LayerBeadAcrossSeams interleaves seam-A/seam-B at each (layer,bead); Alternating must
        # still key off each seam's OWN layer rank, not the interleaved flat position (the bug
        # this test guards against: two seams sharing identical layer/bead sets must not end up
        # with one seam entirely Forward and the other entirely Reverse).
        entries = [
            make_pass("seam-A", layer=1, bead=1, ordinal=1),
            make_pass("seam-A", layer=2, bead=1, ordinal=2),
            make_pass("seam-B", layer=1, bead=1, ordinal=3),
            make_pass("seam-B", layer=2, bead=1, ordinal=4),
        ]
        plan = planner.build_multilayer_plan(
            entries, "E2NativePaths", planner.SequenceMode.LAYER_BEAD_ACROSS_SEAMS, planner.DirectionMode.ALTERNATING,
        )
        by_seam = {"seam-A": [], "seam-B": []}
        for p in plan.execution:
            by_seam[p.seam_uuid].append(p.direction)
        self.assertEqual(by_seam["seam-A"], [planner.Direction.FORWARD, planner.Direction.REVERSE])
        self.assertEqual(by_seam["seam-B"], [planner.Direction.FORWARD, planner.Direction.REVERSE])

    def test_same_direction_mode_is_always_forward(self):
        entries = [
            make_pass("seam-A", layer=0, bead=1, ordinal=1),
            make_pass("seam-A", layer=1, bead=1, ordinal=2),
        ]
        plan = planner.build_multilayer_plan(
            entries, "E2NativePaths", planner.SequenceMode.COMPLETE_SEAM, planner.DirectionMode.SAME_DIRECTION,
        )
        self.assertTrue(all(p.direction == planner.Direction.FORWARD for p in plan.execution))

    def test_zigzag_override_does_not_shift_later_parity(self):
        entries = [
            make_pass("seam-A", layer=0, bead=1, ordinal=1),
            make_pass("seam-A", layer=1, bead=1, ordinal=2, override=planner.DirectionOverride.FORWARD),
            make_pass("seam-A", layer=2, bead=1, ordinal=3),
            make_pass("seam-A", layer=3, bead=1, ordinal=4),
        ]
        plan = planner.build_multilayer_plan(
            entries, "E2NativePaths", planner.SequenceMode.COMPLETE_SEAM, planner.DirectionMode.ZIGZAG,
        )
        directions = [p.direction for p in plan.execution]
        # ordinal 1 forced Forward (was already Reverse->overridden); ordinals 2,3 keep
        # their computed parity as if the override never happened.
        self.assertEqual(directions, [
            planner.Direction.FORWARD, planner.Direction.FORWARD,
            planner.Direction.FORWARD, planner.Direction.REVERSE,
        ])

    def test_alternating_override_does_not_shift_later_layers(self):
        entries = [
            make_pass("seam-A", layer=0, bead=1, ordinal=1),
            make_pass("seam-A", layer=1, bead=1, ordinal=2, override=planner.DirectionOverride.FORWARD),
            make_pass("seam-A", layer=2, bead=1, ordinal=3),
            make_pass("seam-A", layer=3, bead=1, ordinal=4),
        ]
        plan = planner.build_multilayer_plan(
            entries, "E2NativePaths", planner.SequenceMode.COMPLETE_SEAM, planner.DirectionMode.ALTERNATING,
        )
        directions = [p.direction for p in plan.execution]
        # layer 1 forced Forward (was already Reverse->overridden); layers 2,3 keep their
        # computed layer-rank parity as if the override never happened.
        self.assertEqual(directions, [
            planner.Direction.FORWARD, planner.Direction.FORWARD,
            planner.Direction.FORWARD, planner.Direction.REVERSE,
        ])


class Test_PerSeamFallbackScoping(unittest.TestCase):
    def test_duplicate_diagnostic_scoped_to_offending_seam_only(self):
        import MultiLayerDiagnostics as diag

        entries = [
            make_pass("seam-A", layer=1, bead=1, ordinal=1),
            make_pass("seam-A", layer=1, bead=1, ordinal=2),  # duplicate within seam-A
            make_pass("seam-B", layer=0, bead=1, ordinal=3),
        ]
        plan = planner.build_multilayer_plan(
            entries, "E2NativePaths", planner.SequenceMode.COMPLETE_SEAM, planner.DirectionMode.SAME_DIRECTION,
        )
        affected = diag.seams_with_code(plan.diagnostics, "ML005")
        self.assertEqual(affected, {"seam-A"})
        # seam-B's passes remain untouched.
        seam_b = next(s for s in plan.seams if s.seam_uuid == "seam-B")
        self.assertEqual(len(seam_b.passes), 1)


def suite():
    loader = unittest.TestLoader()
    result = unittest.TestSuite()
    result.addTests(loader.loadTestsFromTestCase(Test_SortAndFlatten))
    result.addTests(loader.loadTestsFromTestCase(Test_SeamOrderAndExecution))
    result.addTests(loader.loadTestsFromTestCase(Test_Direction))
    result.addTests(loader.loadTestsFromTestCase(Test_PerSeamFallbackScoping))
    return result


if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
