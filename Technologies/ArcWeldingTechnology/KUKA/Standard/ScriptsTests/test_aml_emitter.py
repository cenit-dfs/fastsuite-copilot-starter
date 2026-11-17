"""Pure unit tests for MultiLayerAmlEmitter — reproduces the committed golden_aml text exactly.

These tests never regenerate the golden; they build neutral inputs and assert the emitter's output
matches the hand-authored file byte-for-byte.
"""
import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Scripts"))

import MultiLayerAmlEmitter as emitter
import MultiLayerProcessTable as process_table

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))))
GOLDEN_AML_DIR = os.path.join(REPO_ROOT, "workshops", "KUKA_Multilayer", "golden_aml")


def _read_golden(name):
    """Strip the 3-line "AML GOLDEN - hand-authored" marker: it is fixture provenance metadata,
    not KRL the emitter would ever produce (see golden_aml/README.md)."""
    with open(os.path.join(GOLDEN_AML_DIR, name), "r", encoding="utf-8") as f:
        text = f.read()
    marker = (";***************************************************\n"
              "; AML GOLDEN - hand-authored, not emitter output\n"
              "; status: synthesized-unvalidated\n")
    return text.replace(marker, "")


PROGRAM_META = {"create": "26-09-01", "create_time": "12:00:00",
                "modified": "26-09-01", "modified_time": "12:00:00", "user": "E2"}


class TestAml01S01(unittest.TestCase):
    """2-point seam, ARCON+ARCOFF only, 1 filler layer."""

    def test_reproduces_committed_golden(self):
        root = [
            emitter.WeldPoint(emitter.ARCON, "P001", "WP001",
                               "78007cee-bb13-5d94-b043-b37467b95f00"),
            emitter.WeldPoint(emitter.ARCOFF, "P002", "WP002",
                               "99b1ec54-f02c-5196-9ba4-36c4223a64e2"),
        ]
        fillers = [emitter.FillerLayer(1, "LayerOffset1")]
        text = emitter.build_seam_module(
            "AML01_S01", root, fillers, "Tool[1]:Torch Base[5]:Part",
            operation_labels=["Seam01_Layer1_Bead1", "Seam01_Layer2_Bead1"],
            program_meta=PROGRAM_META,
        )
        self.assertEqual(text, _read_golden("AML01_S01.src"))


class TestShapeGuard(unittest.TestCase):
    def test_rejects_root_not_starting_with_arcon(self):
        root = [emitter.WeldPoint(emitter.ARCOFF, "P001", "WP001", "x")]
        with self.assertRaises(emitter.SeamShapeError):
            emitter.build_seam_module("BAD", root, [], "Tool[1]:Torch Base[5]:Part")

    def test_extracts_weld_envelope_and_ignores_approach_retract(self):
        motions = [
            emitter.MotionObservation("P001", False),
            emitter.MotionObservation("P002", True, ("ArcOnEvent",), "0.5"),
            emitter.MotionObservation("P003", True),
            emitter.MotionObservation("P004", True, ("ArcOffEvent",), "0.034"),
            emitter.MotionObservation("P005", True),
        ]
        root = emitter.build_root_weld_points("The_Contour_Uuid_at_Start", motions)
        self.assertEqual([emitter.ARCON, emitter.ARCSWI, emitter.ARCOFF], [p.kind for p in root])
        self.assertEqual(["P002", "P003", "P004"], [p.point for p in root])
        self.assertEqual(["WP002", "WP003", "WP004"], [p.weld_point_var for p in root])
        self.assertEqual(root, emitter.build_root_weld_points("The_Contour_Uuid_at_Start", motions))
        self.assertEqual(3, len(set(p.ml_id for p in root)))

    def test_extracts_circular_switch_with_via_point(self):
        motions = [
            emitter.MotionObservation("P001", True, ("ArcOnEvent",)),
            emitter.MotionObservation("P003", False, via_point="P002"),
            emitter.MotionObservation("P003", True, ("ArcOffEvent",)),
        ]
        root = emitter.build_root_weld_points("S1", motions)
        self.assertEqual("P002", root[1].via_point)
        self.assertEqual("WP002", root[1].via_weld_point_var)

        lines = emitter.build_block_lines(
            root,
            [emitter.FillerLayer(1, "LayerOffset1")],
            "Tool[1]:Torch Base[5]:Part",
        )
        text = "\n".join(lines)
        self.assertIn("AmlSetPos(#ArcSwiMoveStd, WDAT02_01_050, WP003, WP002)", text)
        self.assertIn(
            "CIRC AmlGetPos(XP002, LayerOffset1, WP002, AmlInfo, ), "
            "AmlGetPos(XP003, LayerOffset1, WP003, AmlInfo, ) C_DIS C_DIS",
            text,
        )

    def test_rejects_non_linear_motion_without_via_point(self):
        motions = [
            emitter.MotionObservation("P001", True, ("ArcOnEvent",)),
            emitter.MotionObservation("P002", False),
            emitter.MotionObservation("P003", True, ("ArcOffEvent",)),
        ]
        with self.assertRaises(emitter.SeamShapeError):
            emitter.build_root_weld_points("S1", motions)

    def test_rejects_incomplete_or_ambiguous_envelope(self):
        cases = [
            [emitter.MotionObservation("P001", True, ("ArcOnEvent",))],
            [emitter.MotionObservation("P001", True, ("ArcOffEvent",))],
            [emitter.MotionObservation("P001", True, ("ArcOnEvent", "ArcOffEvent"))],
        ]
        for motions in cases:
            with self.subTest(motions=motions), self.assertRaises(emitter.SeamShapeError):
                emitter.build_root_weld_points("S1", motions)


class TestLayerFrameMapping(unittest.TestCase):
    def make_geometry(self, contour_start_offset=0.0):
        return process_table.PassGeometryData(
            work_angle_offset=-5.0,
            absolute_travel_angle=2.5,
            normal_offset=0.003,
            contour_start_offset=contour_start_offset,
            contour_offset=0.0015,
        )

    def test_maps_neutral_geometry_to_provisional_tts_axes(self):
        frame = emitter.build_layer_frame(self.make_geometry())
        self.assertEqual(
            emitter.LayerFrame(0.0, 1.5, 3.0, 0.0, 2.5, -5.0, "provisional"),
            frame,
        )
        self.assertEqual(
            "DECL FRAME LayerOffset2={X 0.000000,Y 1.500000,Z 3.000000,A 0.000000,B 2.500000,C -5.000000}",
            emitter.format_layer_frame_declaration(2, frame),
        )

    def test_rejects_path_tangent_offset(self):
        with self.assertRaises(emitter.UnsupportedLayerGeometryError):
            emitter.build_layer_frame(self.make_geometry(contour_start_offset=0.25))


class TestDatProjection(unittest.TestCase):
    def setUp(self):
        self.native_wdat = (
            'DECL stArcDat_T WDAT02_01_050={WdatId[] "WDAT02_01_050",'
            'Strike {JobModeId[] "Jobmodus",ParamSetId[] "Set1"},'
            'Weld {Velocity 0.00833333},Weave {Pattern #None},Crater {CraterTime 0.00},'
            'Advanced {WeldErrorStrategy 1},Track {IsArcSenseEnabled TRUE}}'
        )
        self.native_ws = (
            'DECL stArcDat_T WS01_01_050={WdatId[] "WS01_01_050",Info {Version 307020112},'
            'Strike {SeamName[] " ",PartName[] " "},Advanced {BitCodedRobotMark 0}}'
        )

    def test_filler_wdat_reuses_process_data_but_drops_identity_and_tracking(self):
        declaration = emitter.build_filler_wdat_declaration(self.native_wdat, 1)
        self.assertEqual(
            'DECL stArcDat_T L1_WDAT02_01_050={Strike {JobModeId[] "Jobmodus",ParamSetId[] "Set1"},'
            'Weld {Velocity 0.00833333},Weave {Pattern #None},Crater {CraterTime 0.00},'
            'Advanced {WeldErrorStrategy 1}}',
            declaration,
        )
        self.assertNotIn("Track", declaration)
        self.assertNotIn("WdatId", declaration)

    def test_filler_wdat_rejects_oversized_identifier(self):
        declaration = self.native_wdat.replace("WDAT02_01_050", "WDAT_IDENTIFIER_TOO_LONG")
        with self.assertRaises(emitter.InvalidWdatError):
            emitter.build_filler_wdat_declaration(declaration, 10)

    def test_weld_points_reuse_root_seam_data_only_on_first_command(self):
        root = emitter.build_root_weld_points("S1", [
            emitter.MotionObservation("P002", True, ("ArcOnEvent",)),
            emitter.MotionObservation("P003", True, ("ArcOffEvent",)),
        ])
        declarations = emitter.build_weld_point_declarations(root, self.native_ws, "307020112")
        self.assertIn('WP002={WdatId[] "WP002",Info {Version 307020112},Strike', declarations[0])
        self.assertIn("MultiLayer {OP #ARC", declarations[0])
        self.assertNotIn("Strike", declarations[1])
        self.assertIn('WP003={WdatId[] "WP003",Info {Version 307020112},MultiLayer', declarations[1])

    def test_aml_info_uses_filler_count(self):
        self.assertEqual(
            'DECL stAmlInfo_T AmlInfo={Info[] " ",MaxLayer 5}',
            emitter.format_aml_info_declaration(5),
        )


def suite():
    result = unittest.TestSuite()
    for case in (TestAml01S01, TestAml02S01, TestShapeGuard, TestLayerFrameMapping,
                 TestDatProjection):
        result.addTests(unittest.TestLoader().loadTestsFromTestCase(case))
    return result


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    outcome = runner.run(suite())
    sys.exit(0 if outcome.wasSuccessful() else 1)
