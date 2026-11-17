import ast
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Dict, List, Optional, Tuple
import unittest


DOWNLOADER = Path(__file__).parents[2] / "OLPTranslators" / "KUKA" / "KUKA_KRC5_Arc_Welding.py"


class SeamFindConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = DOWNLOADER.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source)
        selected_names = {
            "load_seam_find_sensor_names",
            "get_seam_find_sensor_name",
            "validate_seam_find_correction_buckets",
            "SeamFindGenerator",
        }
        selected = [
            node for node in cls.tree.body
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in selected_names
        ]
        namespace = {
            "dataclass": dataclass,
            "json": json,
            "os": os,
            "Path": Path,
            "re": re,
            "Dict": Dict,
            "List": List,
            "Optional": Optional,
            "Tuple": Tuple,
            "Pair": Tuple[str, str],
            "RECIPES_FILENAME": "SeamFind_Recipes.json",
            "PROFILES_FILENAME": "SeamFind_Sensor_Profiles.json",
            "_build_seam_find_header": lambda *args, **kwargs: "header",
        }
        exec(compile(ast.Module(body=selected, type_ignores=[]), str(DOWNLOADER), "exec"), namespace)
        cls.load_sensor_names = staticmethod(namespace["load_seam_find_sensor_names"])
        cls.generator_type = namespace["SeamFindGenerator"]

    @staticmethod
    def params(**overrides):
        values = {
            "XCorre": "EMPTY", "XcdParam": "EMPTY",
            "YCorr": "EMPTY", "YcdParam": "EMPTY",
            "Y2Corr": "EMPTY", "Y2cdParam": "EMPTY",
            "ZCorr": "EMPTY", "ZcdParam": "EMPTY",
            "Z2Corr": "EMPTY", "Z2cdParam": "EMPTY",
            "Z3Corr": "EMPTY", "Z3cdParam": "EMPTY",
        }
        values.update(overrides)
        return values

    @staticmethod
    def write_configuration(folder, ilf_params, sensors=None, scan_ops=None):
        profiles = {
            "sensors": sensors if sensors is not None else [],
            "profiles": [{"name": "Top", "ALONG": "CDh", "LATERAL": "CDh", "HEIGHT": "CDv"}],
        }
        recipes = [{"name": "Recipe", "scan_ops": scan_ops or ["ATTR1"], "ilf_params": ilf_params}]
        (folder / "SeamFind_Sensor_Profiles.json").write_text(json.dumps(profiles), encoding="utf-8")
        (folder / "SeamFind_Recipes.json").write_text(json.dumps(recipes), encoding="utf-8")

    def make_generator(self, folder, ilf_params, scan_ops=None):
        scan_ops = scan_ops or ["ATTR1"]
        self.write_configuration(folder, ilf_params, scan_ops=scan_ops)
        tech_tab_file = folder / "SeamFind_Recipes.json"
        return self.generator_type(
            "Recipe", "Top", 1, str(folder), str(tech_tab_file), len(scan_ops), None, "400030000"
        )

    def test_sensor_display_names_are_keyed_by_id(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "profiles.json"
            path.write_text(json.dumps({"sensors": [{"id": 1, "display_name": "LineLaser"}]}), encoding="utf-8")
            self.assertEqual({1: "LineLaser"}, self.load_sensor_names(path))

    def test_sensor_configuration_rejects_duplicates_and_fold_control_text(self):
        invalid = (
            [{"id": 1, "display_name": "A"}, {"id": 1, "display_name": "B"}],
            [{"id": 1, "display_name": "Bad;ENDFOLD"}],
        )
        for sensors in invalid:
            with self.subTest(sensors=sensors), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "profiles.json"
                path.write_text(json.dumps({"sensors": sensors}), encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.load_sensor_names(path)

    def test_legal_empty_single_and_full_buckets_build(self):
        cases = (
            (self.params(), ["ATTR1"]),
            (self.params(ZCorr="ATTR1", ZcdParam="<HEIGHT>"), ["ATTR1"]),
            (self.params(
                ZCorr="ATTR1", ZcdParam="<HEIGHT>",
                Z2Corr="ATTR2", Z2cdParam="<HEIGHT>",
                Z3Corr="ATTR3", Z3cdParam="<HEIGHT>",
            ), ["ATTR1", "ATTR2", "ATTR3"]),
        )
        for params, scan_ops in cases:
            with self.subTest(params=params), tempfile.TemporaryDirectory() as temp:
                self.make_generator(Path(temp), params, scan_ops).build()

    def test_two_entry_z_bucket_is_rejected(self):
        params = self.params(
            ZCorr="ATTR1", ZcdParam="<HEIGHT>",
            Z2Corr="ATTR2", Z2cdParam="<HEIGHT>",
        )
        with tempfile.TemporaryDirectory() as temp:
            generator = self.make_generator(Path(temp), params, ["ATTR1", "ATTR2"])
            with self.assertRaisesRegex(ValueError, "Z bucket has 2 corrections"):
                generator.build()

    def test_half_empty_and_unknown_scan_reference_are_rejected(self):
        cases = (
            self.params(ZCorr="ATTR1", ZcdParam="EMPTY"),
            self.params(ZCorr="ATTR2", ZcdParam="<HEIGHT>"),
        )
        for params in cases:
            with self.subTest(params=params), tempfile.TemporaryDirectory() as temp:
                generator = self.make_generator(Path(temp), params, ["ATTR1"])
                with self.assertRaises(ValueError):
                    generator.build()

    def test_program_end_switches_off_active_finding_before_base_footer(self):
        downloader = next(
            node for node in self.tree.body
            if isinstance(node, ast.ClassDef) and node.name == "KUKA_KRC5_Arc_Welding"
        )
        method = next(
            node for node in downloader.body
            if isinstance(node, ast.FunctionDef) and node.name == "ProgramEnd"
        )
        source = ast.get_source_segment(self.source, method)
        self.assertIn("BF_CorrOff()", source)
        self.assertLess(source.index("BF_CorrOff()"), source.index("super().ProgramEnd"))

    def test_finding_clear_is_emitted_after_correction_build(self):
        build_index = self.source.index("self.AddLineToSource(builder.build())")
        clear_index = self.source.index("BF_ClearSensor()", build_index)
        active_index = self.source.index("self.SeamFindCorrectionActive = True", build_index)
        self.assertLess(build_index, clear_index)
        self.assertLess(clear_index, active_index)

    def test_finding_init_uses_optional_display_name_without_changing_sensor_number(self):
        self.assertIn("sensorName = get_seam_find_sensor_name", self.source)
        self.assertIn("sensorLabel = ': ' + sensorName if sensorName else ''", self.source)
        self.assertIn("SeamFind.SensorNo='+f'{self.TouchInfo.SensorId:d}", self.source)
        self.assertIn("BF_Init('+f'{self.TouchInfo.SensorId:d}", self.source)


if __name__ == "__main__":
    unittest.main()
