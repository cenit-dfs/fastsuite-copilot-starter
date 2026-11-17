"""Pure unit tests for MultiLayerAmlCapability (spec sections 13.1, 13.6, 13.7)."""
import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Scripts"))

import MultiLayerMetadata
import MultiLayerAmlCapability as capability
import MultiLayerPlanner as planner


VALID_CONFIG = capability.AmlConfiguration(
    controller_family="KRC5", kss_version="8.7", aml_installed=True, aml_version="3.7.1.4",
)


def make_geometry(contour_start_offset=0.0):
    import MultiLayerProcessTable as process_table
    return process_table.PassGeometryData(
        work_angle_offset=0.0, absolute_travel_angle=0.0, normal_offset=3.0,
        contour_start_offset=contour_start_offset, contour_offset=1.5,
    )


def make_plan(seam_specs, output_mode=MultiLayerMetadata.OUTPUT_MODE_KUKA_AML,
              direction_mode=planner.DirectionMode.SAME_DIRECTION):
    """seam_specs: [(seam_uuid, pass_count), ...]."""
    inputs = []
    ordinal = 0
    for seam_uuid, pass_count in seam_specs:
        for layer in range(1, pass_count + 1):
            inputs.append(planner.PassInput(
                seam_uuid=seam_uuid, wps_main_id=1, wps_sub_id=layer, wps_name="WPS",
                layer=layer, bead=1, source_operation=None, source_operation_ordinal=ordinal,
                recipe_fingerprint="fp",
            ))
            ordinal += 1
    return planner.build_multilayer_plan(
        inputs, output_mode=output_mode,
        sequence_mode=planner.SequenceMode.COMPLETE_SEAM,
        direction_mode=direction_mode,
    )


def codes(diagnostics):
    return sorted(d.code for d in diagnostics)


class Test_ParseVersion(unittest.TestCase):
    def test_dotted_numeric(self):
        self.assertEqual(capability.parse_version("3.7.1.4"), (3, 7, 1, 4))

    def test_rejects_non_numeric_and_empty(self):
        for text in ("3.7.1.x", "", "  ", "V3.7", None, 3.7):
            self.assertIsNone(capability.parse_version(text), text)


class Test_ProgramConfiguration(unittest.TestCase):
    def test_valid_configuration_passes(self):
        allowed, diagnostics = capability.check_program_configuration(VALID_CONFIG)
        self.assertTrue(allowed)
        self.assertEqual(diagnostics, [])

    def test_kss_86_and_87_both_supported(self):
        for version in ("8.6", "8.7", "8.6.7"):
            config = capability.AmlConfiguration("KRC5", version, True, "3.7.1.4")
            self.assertTrue(capability.check_program_configuration(config)[0], version)

    def test_option_pack_not_installed_raises_ml007(self):
        config = capability.AmlConfiguration("KRC5", "8.7", False, "3.7.1.4")
        allowed, diagnostics = capability.check_program_configuration(config)
        self.assertFalse(allowed)
        self.assertEqual(codes(diagnostics), ["ML007"])

    def test_wrong_controller_family_raises_ml008(self):
        config = capability.AmlConfiguration("KRC4", "8.7", True, "3.7.1.4")
        self.assertEqual(codes(capability.check_program_configuration(config)[1]), ["ML008"])

    def test_controller_family_is_case_insensitive(self):
        config = capability.AmlConfiguration(" krc5 ", "8.7", True, "3.7.1.4")
        self.assertTrue(capability.check_program_configuration(config)[0])

    def test_unsupported_kss_raises_ml008(self):
        config = capability.AmlConfiguration("KRC5", "8.5", True, "3.7.1.4")
        self.assertEqual(codes(capability.check_program_configuration(config)[1]), ["ML008"])

    def test_incompatible_aml_version_raises_ml008(self):
        config = capability.AmlConfiguration("KRC5", "8.7", True, "3.3.1.11")
        self.assertEqual(codes(capability.check_program_configuration(config)[1]), ["ML008"])

    def test_unparseable_aml_version_raises_ml008(self):
        config = capability.AmlConfiguration("KRC5", "8.7", True, "unknown")
        self.assertEqual(codes(capability.check_program_configuration(config)[1]), ["ML008"])

    def test_every_failing_condition_is_reported(self):
        config = capability.AmlConfiguration("KRC4", "8.5", False, "3.3.1.11")
        allowed, diagnostics = capability.check_program_configuration(config)
        self.assertFalse(allowed)
        self.assertEqual(codes(diagnostics), ["ML007", "ML008", "ML008", "ML008"])

    def test_diagnostics_name_the_fallback_mode(self):
        config = capability.AmlConfiguration("KRC5", "8.7", False, "3.7.1.4")
        diagnostic = capability.check_program_configuration(config, program="P1")[1][0]
        self.assertEqual(diagnostic.program, "P1")
        self.assertEqual(diagnostic.selected_mode, MultiLayerMetadata.OUTPUT_MODE_KUKA_AML)
        self.assertEqual(diagnostic.fallback_mode, MultiLayerMetadata.OUTPUT_MODE_E2_NATIVE)


class Test_SeamRestrictions(unittest.TestCase):
    def test_ordinary_seam_passes(self):
        seam = make_plan([("S1", 3)]).seams[0]
        allowed, diagnostics = capability.check_seam(seam, geometry_for=lambda p: make_geometry())
        self.assertTrue(allowed)
        self.assertEqual(diagnostics, [])

    def test_exactly_99_fillers_allowed(self):
        seam = make_plan([("S1", 100)]).seams[0]
        self.assertTrue(capability.check_seam(seam)[0])

    def test_100_fillers_raises_ml009(self):
        seam = make_plan([("S1", 101)]).seams[0]
        allowed, diagnostics = capability.check_seam(seam)
        self.assertFalse(allowed)
        self.assertEqual(codes(diagnostics), ["ML009"])

    def test_missing_seam_uuid_raises_ml006(self):
        seam = make_plan([("", 2)]).seams[0]
        self.assertEqual(codes(capability.check_seam(seam)[1]), ["ML006"])

    def test_reverse_direction_raises_ml017_per_reconciliation_f15(self):
        plan = make_plan([("S1", 2)], direction_mode=planner.DirectionMode.ALTERNATING)
        allowed, diagnostics = capability.check_seam(plan.seams[0])
        self.assertFalse(allowed)
        self.assertEqual(codes(diagnostics), ["ML017"])

    def test_unresolved_geometry_raises_ml003(self):
        seam = make_plan([("S1", 2)]).seams[0]
        allowed, diagnostics = capability.check_seam(seam, geometry_for=lambda p: None)
        self.assertFalse(allowed)
        self.assertEqual(codes(diagnostics), ["ML003", "ML003"])

    def test_contour_start_offset_raises_ml012(self):
        seam = make_plan([("S1", 2)]).seams[0]
        geometry_for = lambda p: make_geometry(contour_start_offset=2.0 if p.layer == 2 else 0.0)
        allowed, diagnostics = capability.check_seam(seam, geometry_for=geometry_for)
        self.assertFalse(allowed)
        self.assertEqual(codes(diagnostics), ["ML012"])

    def test_seam_diagnostics_identify_the_pass(self):
        seam = make_plan([("S1", 2)]).seams[0]
        geometry_for = lambda p: make_geometry(contour_start_offset=2.0 if p.layer == 2 else 0.0)
        diagnostic = capability.check_seam(seam, geometry_for=geometry_for)[1][0]
        self.assertEqual(diagnostic.seam_uuid, "S1")
        self.assertEqual((diagnostic.layer, diagnostic.bead), (2, 1))
        self.assertEqual(diagnostic.wps_main_id, 1)


class Test_SelectAmlSeams(unittest.TestCase):
    def test_native_output_mode_is_not_a_fallback(self):
        plan = make_plan([("S1", 2)], output_mode=MultiLayerMetadata.OUTPUT_MODE_E2_NATIVE)
        result = capability.select_aml_seams(plan, VALID_CONFIG)
        self.assertFalse(result.program_allows_aml)
        self.assertEqual(result.aml_seam_uuids, frozenset())
        self.assertEqual(result.diagnostics, ())

    def test_bad_configuration_disables_every_seam(self):
        plan = make_plan([("S1", 2), ("S2", 2)])
        config = capability.AmlConfiguration("KRC5", "8.7", False, "3.7.1.4")
        result = capability.select_aml_seams(plan, config)
        self.assertFalse(result.program_allows_aml)
        self.assertEqual(result.native_seam_uuids, frozenset({"S1", "S2"}))
        self.assertEqual(codes(result.diagnostics), ["ML007"])

    def test_fallback_is_scoped_to_the_offending_seam(self):
        plan = make_plan([("S1", 2), ("S2", 101)])
        result = capability.select_aml_seams(plan, VALID_CONFIG)
        self.assertTrue(result.program_allows_aml)
        self.assertEqual(result.aml_seam_uuids, frozenset({"S1"}))
        self.assertEqual(result.native_seam_uuids, frozenset({"S2"}))
        self.assertIn("ML009", codes(result.diagnostics))

    def test_dry_run_notice_emitted_whenever_aml_is_produced(self):
        plan = make_plan([("S1", 2)])
        result = capability.select_aml_seams(plan, VALID_CONFIG)
        self.assertIn("ML016", codes(result.diagnostics))

    def test_no_dry_run_notice_when_every_seam_fell_back(self):
        plan = make_plan([("S1", 101)])
        result = capability.select_aml_seams(plan, VALID_CONFIG)
        self.assertEqual(result.aml_seam_uuids, frozenset())
        self.assertNotIn("ML016", codes(result.diagnostics))


def suite():
    loader = unittest.TestLoader()
    result = unittest.TestSuite()
    for case in (Test_ParseVersion, Test_ProgramConfiguration, Test_SeamRestrictions,
                 Test_SelectAmlSeams):
        result.addTests(loader.loadTestsFromTestCase(case))
    return result


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
