"""Pure unit tests for MultiLayerDiagnostics."""
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Scripts"))

import MultiLayerDiagnostics as diag


class Test_MakeDiagnostic(unittest.TestCase):
    def test_builds_known_code_with_default_message(self):
        d = diag.make_diagnostic("ML007", seam_uuid="seam-1")
        self.assertEqual(d.severity, diag.Severity.WARNING)
        self.assertEqual(d.seam_uuid, "seam-1")
        self.assertEqual(d.message, diag.CODES["ML007"][1])

    def test_builds_known_code_with_custom_message(self):
        d = diag.make_diagnostic("ML005", message="custom", layer=1, bead=1)
        self.assertEqual(d.message, "custom")
        self.assertEqual(d.layer, 1)
        self.assertEqual(d.bead, 1)

    def test_rejects_unknown_code(self):
        with self.assertRaises(ValueError):
            diag.make_diagnostic("ML999")

    def test_all_defined_codes_are_warnings(self):
        # Spec section 14 defines every ML0xx code as Warning severity.
        for code, (severity, _) in diag.CODES.items():
            self.assertEqual(severity, diag.Severity.WARNING, code)


class Test_SeamsWithCode(unittest.TestCase):
    def test_filters_by_code_and_seam(self):
        diagnostics = (
            diag.make_diagnostic("ML005", seam_uuid="seam-A"),
            diag.make_diagnostic("ML007", seam_uuid="seam-B"),
        )
        self.assertEqual(diag.seams_with_code(diagnostics, "ML005"), {"seam-A"})
        self.assertEqual(diag.seams_with_code(diagnostics, "ML007"), {"seam-B"})
        self.assertEqual(diag.seams_with_code(diagnostics, "ML009"), set())


def suite():
    loader = unittest.TestLoader()
    result = unittest.TestSuite()
    result.addTests(loader.loadTestsFromTestCase(Test_MakeDiagnostic))
    result.addTests(loader.loadTestsFromTestCase(Test_SeamsWithCode))
    return result


if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
