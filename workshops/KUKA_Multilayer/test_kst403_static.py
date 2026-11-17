import ast
from pathlib import Path
import unittest


DOWNLOADER = Path(__file__).parents[2] / "OLPTranslators" / "KUKA" / "KUKA_KRC5_Arc_Welding.py"
class SeamTechTracking403StaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = DOWNLOADER.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source)
        cls.downloader_class = next(
            node
            for node in cls.tree.body
            if isinstance(node, ast.ClassDef) and node.name == "KUKA_KRC5_Arc_Welding"
        )

    @classmethod
    def method_source(cls, name):
        method = next(
            node
            for node in cls.downloader_class.body
            if isinstance(node, ast.FunctionDef) and node.name == name
        )
        return ast.get_source_segment(cls.source, method)

    def test_403_version_threshold_is_numeric(self):
        method = self.method_source("IsSeamTechTracking403OrNewer")
        self.assertIn(">= 400030000", method)

    def test_normal_tracking_keeps_distinct_legacy_and_403_forms(self):
        leadin = self.method_source("OutputSeamTrackingLeadinEvent")
        self.assertIn("STTg_SensorOn(STT", leadin)
        self.assertIn("STTg_SensorOn(STTg_Para_Act)", leadin)
        self.assertIn("tracking403 = self.IsSeamTechTracking403OrNewer()", leadin)
        self.assertIn("if tracking403:", leadin)

    def test_403_omits_legacy_weave_helpers(self):
        placeholders = self.method_source("FillTechPlaceholders")
        self.assertEqual(2, placeholders.count("STT_PrepareWeave"))
        self.assertEqual(2, placeholders.count("STT_SensorWeave"))
        self.assertEqual(2, placeholders.count("not self.IsSeamTechTracking403OrNewer()"))

    def test_search_start_keeps_legacy_form_and_defers_403_close(self):
        search = self.method_source("OutputSeamTrackingSearchStartEvent")
        motion = self.method_source("OutputMotionData")
        self.assertIn("STTg_SearchLin(", search)
        self.assertIn("STTg_SearchSeamStart(", search)
        self.assertIn("self.PendingSeamTrackSearchStart =", search)
        self.assertIn("super().OutputMotionData", motion)
        self.assertLess(
            motion.index("super().OutputMotionData"),
            motion.index("self.Source.append(self.PendingSeamTrackSearchStart)"),
        )

    def test_native_reuse_forces_keep_and_clears_on_final_pass(self):
        track_off = self.method_source("OutputSeamTrackingOffEvent")
        operation_end = self.method_source("OperationEnd")
        self.assertIn("trackingOffKeepDistance = True", track_off)
        self.assertIn("and not retainNativeOffset", operation_end)
        self.assertIn("self.NativeSeamRemainingPasses[self.CurrentNativeSeamUuid] -= 1", operation_end)

    def test_finding_403_threshold_preserves_legacy_branch(self):
        finding_class = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.ClassDef) and node.name == "SeamFindGenerator"
        )
        finding_source = ast.get_source_segment(self.source, finding_class)
        self.assertEqual(3, self.source.count("seamfind_version < '400030000'"))
        self.assertIn("SeamFind.CorrUniversal", finding_source)
        self.assertIn("SeamFind.CorrLoadAndOn", finding_source)
        self.assertIn("SeamFind.CorrCalcAndOn", finding_source)


if __name__ == "__main__":
    unittest.main()