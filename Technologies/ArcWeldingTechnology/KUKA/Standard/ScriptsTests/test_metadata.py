"""Guard against edits that silently swallow a constant into a preceding comment.

Every ATTR_*/PG_* name referenced by the technology scripts must resolve. This catches the
class of defect where a lost newline merged a definition into a comment line.
"""
import os
import re
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Scripts"))

import MultiLayerMetadata as ml_meta

SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKMETHOD = os.path.join(SCRIPTS_DIR, "Scripts", "StitchWeldingWorkMethod.py")
TECHNOLOGY = os.path.join(SCRIPTS_DIR, "Scripts", "ArcWeldingTechnology.py")
SETTINGS = os.path.join(SCRIPTS_DIR, "ControllerSettings", "Settings.xml")

REQUIRED_NAMES = (
    "SCHEMA_VERSION",
    "ATTR_WPS_AUTOMATIC", "ATTR_WPS_AUTOMATIC_NAMES",
    "PG_CAD_MATCH_INTEGER_ATTRIBUTES", "PG_CAD_MATCH_STRING_ATTRIBUTES", "PG_CAD_MATCH_DOUBLE_ATTRIBUTES",
    "ATTR_OUTPUT_MODE", "ATTR_SEQUENCE_MODE", "ATTR_DIRECTION_MODE", "ATTR_DIRECTION_OVERRIDE",
    "ATTR_KUKA_AML_INSTALLED", "ATTR_KUKA_AML_VERSION",
    "ATTR_METADATA_VERSION", "ATTR_USES_PROCESS_TABLE", "ATTR_WPS_MAIN_ID", "ATTR_WPS_SUB_ID",
    "ATTR_WPS_NAME", "ATTR_LAYER_NUMBER", "ATTR_BEAD_NUMBER", "ATTR_FLAT_PASS_INDEX",
    "ATTR_SEAM_UUID", "ATTR_RECIPE_FINGERPRINT", "ATTR_RECIPE_STATE",
    "ATTR_WORK_ANGLE_OFFSET", "ATTR_ABSOLUTE_TRAVEL_ANGLE", "ATTR_NORMAL_OFFSET",
    "ATTR_CONTOUR_START_OFFSET", "ATTR_CONTOUR_OFFSET",
    "OUTPUT_MODE_LITERALS", "OUTPUT_MODE_DEFAULT", "OUTPUT_MODE_E2_NATIVE", "OUTPUT_MODE_KUKA_AML",
    "SEQUENCE_MODE_LITERALS", "SEQUENCE_MODE_DEFAULT",
    "DIRECTION_MODE_LITERALS", "DIRECTION_MODE_DEFAULT",
    "DIRECTION_OVERRIDE_LITERALS", "DIRECTION_OVERRIDE_DEFAULT",
    "RECIPE_STATE_LITERALS", "RECIPE_STATE_NOT_APPLICABLE", "RECIPE_STATE_CURRENT_SNAPSHOT",
    "KUKA_AML_INSTALLED_DEFAULT", "KUKA_AML_VERSION_DEFAULT",
    "METADATA_DEFAULTS",
)


class Test_MetadataSurface(unittest.TestCase):
    def test_every_required_name_exists(self):
        missing = [name for name in REQUIRED_NAMES if not hasattr(ml_meta, name)]
        self.assertEqual(missing, [], "MultiLayerMetadata is missing: %s" % missing)

    def test_attribute_names_are_non_empty_strings(self):
        for name in REQUIRED_NAMES:
            if not name.startswith("ATTR_"):
                continue
            value = getattr(ml_meta, name)
            self.assertIsInstance(value, str, "%s must be a string" % name)
            self.assertTrue(value.strip(), "%s must not be empty" % name)

    def test_geometry_metadata_is_created_persisted_and_registered(self):
        geometry_names = (
            ml_meta.ATTR_WORK_ANGLE_OFFSET,
            ml_meta.ATTR_ABSOLUTE_TRAVEL_ANGLE,
            ml_meta.ATTR_NORMAL_OFFSET,
            ml_meta.ATTR_CONTOUR_START_OFFSET,
            ml_meta.ATTR_CONTOUR_OFFSET,
        )
        with open(WORKMETHOD, "r", encoding="utf-8") as source_file:
            source = source_file.read()
        registered = {
            element.attrib["Name"]
            for element in ET.parse(SETTINGS).iter("Attribute")
        }
        for name in geometry_names:
            self.assertIn("AddDouble(geometryAttribute", source)
            self.assertIn("SetDouble(ml_meta.", source)
            self.assertIn(name, registered)

    def test_native_and_kuka_aml_modes_are_user_selectable(self):
        with open(TECHNOLOGY, "r", encoding="utf-8") as source_file:
            source = source_file.read()

        output_block = re.search(
            r"AddEnum\(ml_meta\.ATTR_OUTPUT_MODE,.*?(?=attribIntENM = attribCreator\.AddEnum\(ml_meta\.ATTR_SEQUENCE_MODE)",
            source,
            re.DOTALL,
        )
        installed_block = re.search(
            r"AddBool\(ml_meta\.ATTR_KUKA_AML_INSTALLED,.*?(?=attribString = attribCreator\.AddString\(ml_meta\.ATTR_KUKA_AML_VERSION)",
            source,
            re.DOTALL,
        )
        self.assertIsNotNone(output_block)
        self.assertIsNotNone(installed_block)
        self.assertNotIn("SetReadOnly(True)", output_block.group(0))
        self.assertNotIn("SetReadOnly(True)", installed_block.group(0))

    def test_cross_seam_sequence_mode_remains_feature_gated(self):
        with open(TECHNOLOGY, "r", encoding="utf-8") as source_file:
            source = source_file.read()
        sequence_block = re.search(
            r"AddEnum\(ml_meta\.ATTR_SEQUENCE_MODE,.*?(?=attribIntENM = attribCreator\.AddEnum\(ml_meta\.ATTR_DIRECTION_MODE)",
            source,
            re.DOTALL,
        )
        self.assertIsNotNone(sequence_block)
        self.assertIn("SetReadOnly(True)", sequence_block.group(0))

    def test_multilayer_options_have_dynamic_visibility_owners(self):
        with open(TECHNOLOGY, "r", encoding="utf-8") as source_file:
            technology_source = source_file.read()
        with open(WORKMETHOD, "r", encoding="utf-8") as source_file:
            workmethod_source = source_file.read()

        for attribute in (
            "ml_meta.ATTR_OUTPUT_MODE",
            "ml_meta.ATTR_SEQUENCE_MODE",
            "ml_meta.ATTR_DIRECTION_MODE",
        ):
            self.assertIn(attribute, technology_source)
        self.assertIn("versionAttrib.SetVisibility(installed)", technology_source)
        self.assertIn("setDirectionOverrideVisible(True)", workmethod_source)
        self.assertIn("setDirectionOverrideVisible(False)", workmethod_source)


def suite():
    loader = unittest.TestLoader()
    result = unittest.TestSuite()
    result.addTests(loader.loadTestsFromTestCase(Test_MetadataSurface))
    return result


if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
