import ast
from pathlib import Path
import unittest


DOWNLOADER = Path(__file__).parents[2] / "OLPTranslators" / "KUKA" / "KUKA_KRC5_Arc_Welding.py"


class AmlDownloaderSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = DOWNLOADER.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source)
        guard_node = next(
            node
            for node in cls.tree.body
            if isinstance(node, ast.ClassDef) and node.name == "OutputBufferGuard"
        )
        namespace = {}
        exec(compile(ast.Module(body=[guard_node], type_ignores=[]), str(DOWNLOADER), "exec"), namespace)
        cls.guard_type = namespace["OutputBufferGuard"]

    def make_owner(self):
        owner = type("Owner", (), {})()
        for name in self.guard_type.BUFFER_NAMES:
            setattr(owner, name, [f"original-{name}"])
        return owner

    def test_guard_captures_and_restores_every_buffer(self):
        self.assertEqual(
            (
                "Source", "Data", "DataE6POS", "DataE6AXIS", "DataFDAT", "DataLDAT", "DataPDAT",
                "DataTechDAT1", "DataTechDAT2", "DataTechDAT3",
            ),
            self.guard_type.BUFFER_NAMES,
        )
        owner = self.make_owner()
        original = {name: getattr(owner, name) for name in self.guard_type.BUFFER_NAMES}

        with self.guard_type(owner) as guard:
            for name in self.guard_type.BUFFER_NAMES:
                getattr(owner, name).append(f"captured-{name}")

        for name in self.guard_type.BUFFER_NAMES:
            self.assertIs(original[name], getattr(owner, name))
            self.assertEqual([f"captured-{name}"], guard.captured[name])

    def test_guard_restores_every_buffer_after_exception(self):
        owner = self.make_owner()
        original = {name: getattr(owner, name) for name in self.guard_type.BUFFER_NAMES}

        with self.assertRaisesRegex(RuntimeError, "capture failed"):
            with self.guard_type(owner) as guard:
                owner.Source.append("partial")
                raise RuntimeError("capture failed")

        for name in self.guard_type.BUFFER_NAMES:
            self.assertIs(original[name], getattr(owner, name))
        self.assertEqual(["partial"], guard.captured["Source"])

    def test_arc_event_pairing_state_is_instance_owned(self):
        self.assertNotIn("OutputArcOnEvent.skipNext", self.source)
        self.assertNotIn("OutputArcOffEvent.skipNext", self.source)
        self.assertIn("self._output_arc_on_event_skip_next", self.source)
        self.assertIn("self._output_arc_off_event_skip_next", self.source)


if __name__ == "__main__":
    unittest.main()