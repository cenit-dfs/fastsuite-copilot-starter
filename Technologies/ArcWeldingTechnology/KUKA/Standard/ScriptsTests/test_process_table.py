"""Pure unit tests for MultiLayerProcessTable (spec section 17.1, items 1-5)."""
import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Scripts"))

import MultiLayerProcessTable as process_table
from _row_fixture import make_row


class Test_ParseRow(unittest.TestCase):
    def test_parses_valid_single_layer_row(self):
        row = make_row()
        record = process_table.parse_row(row)
        self.assertEqual(record.main_id, 100)
        self.assertEqual(record.sub_id, 1)
        self.assertEqual(record.layer, 1)
        self.assertEqual(record.bead, 1)

    def test_parses_valid_multilayer_row_set(self):
        rows = [
            make_row({process_table.Row.LAYER_NUMBER: 0, process_table.Row.BEAD_NUMBER: 1}),
            make_row({process_table.Row.LAYER_NUMBER: 1, process_table.Row.BEAD_NUMBER: 1}),
            make_row({process_table.Row.LAYER_NUMBER: 1, process_table.Row.BEAD_NUMBER: 2}),
        ]
        records = [process_table.parse_row(row) for row in rows]
        self.assertEqual([(r.layer, r.bead) for r in records], [(0, 1), (1, 1), (1, 2)])

    def test_rejects_short_row(self):
        short_row = make_row()[:-1]
        with self.assertRaises(process_table.ProcessTableRowError):
            process_table.parse_row(short_row)

    def test_rejects_type_invalid_row(self):
        bad_row = make_row({process_table.Row.LAYER_NUMBER: "not-a-number"})
        with self.assertRaises(process_table.ProcessTableRowError):
            process_table.parse_row(bad_row)

    def test_fingerprint_ignores_is_used(self):
        row_used = make_row({process_table.Row.IS_USED: True})
        row_unused = make_row({process_table.Row.IS_USED: False})
        record_used = process_table.parse_row(row_used)
        record_unused = process_table.parse_row(row_unused)
        self.assertEqual(record_used.raw_row_fingerprint, record_unused.raw_row_fingerprint)

    def test_fingerprint_changes_with_process_value(self):
        row_a = make_row()
        row_b = make_row({process_table.Row.WELDING_SPEED: 0.009})
        record_a = process_table.parse_row(row_a)
        record_b = process_table.parse_row(row_b)
        self.assertNotEqual(record_a.raw_row_fingerprint, record_b.raw_row_fingerprint)


class Test_FindByStableId(unittest.TestCase):
    def setUp(self):
        self.rows = [
            make_row({process_table.Row.MAIN_ID: 100, process_table.Row.SUB_ID: 1,
                      process_table.Row.LAYER_NUMBER: 0, process_table.Row.BEAD_NUMBER: 1}),
            make_row({process_table.Row.MAIN_ID: 100, process_table.Row.SUB_ID: 2,
                      process_table.Row.LAYER_NUMBER: 1, process_table.Row.BEAD_NUMBER: 1}),
        ]

    def test_matches_by_stable_ids_not_name(self):
        record = process_table.find_by_stable_id(self.rows, main_id=100, sub_id=2, layer=1, bead=1)
        self.assertIsNotNone(record)
        self.assertEqual(record.sub_id, 2)

    def test_returns_none_when_no_stable_match(self):
        record = process_table.find_by_stable_id(self.rows, main_id=999, sub_id=1, layer=0, bead=1)
        self.assertIsNone(record)

    def test_ignores_data_invalid_rows(self):
        rows = self.rows + [make_row({
            process_table.Row.MAIN_ID: 100, process_table.Row.SUB_ID: 3,
            process_table.Row.LAYER_NUMBER: 2, process_table.Row.BEAD_NUMBER: 1,
            process_table.Row.DATA_VALID: False,
        })]
        record = process_table.find_by_stable_id(rows, main_id=100, sub_id=3, layer=2, bead=1)
        self.assertIsNone(record)


class Test_SelectFirstUnused(unittest.TestCase):
    def test_selects_first_unused_matching_row(self):
        rows = [
            make_row({process_table.Row.SUB_ID: 1, process_table.Row.IS_USED: True}),
            make_row({process_table.Row.SUB_ID: 2, process_table.Row.IS_USED: False}),
        ]
        result = process_table.select_first_unused(rows, "WPS_A")
        self.assertIsNotNone(result)
        index, record = result
        self.assertEqual(index, 1)
        self.assertEqual(record.sub_id, 2)

    def test_ignores_single_layer_and_invalid_rows(self):
        rows = [
            make_row({process_table.Row.DATA_VALID: False}),
            make_row({process_table.Row.NAME: "OtherWPS"}),
        ]
        self.assertIsNone(process_table.select_first_unused(rows, "WPS_A"))

    def test_single_pass_wps_is_not_multilayer(self):
        rows = [make_row({process_table.Row.SUB_ID: 1})]
        self.assertFalse(process_table.is_multilayer_wps(rows, "WPS_A"))
        self.assertEqual(process_table.find_candidate_rows(rows, "WPS_A"), [])
        self.assertIsNone(process_table.select_first_unused(rows, "WPS_A"))


class Test_AmbiguousMainIds(unittest.TestCase):
    def test_detects_ambiguous_main_ids_for_same_name(self):
        rows = [
            make_row({process_table.Row.MAIN_ID: 100}),
            make_row({process_table.Row.MAIN_ID: 200}),
        ]
        main_ids = process_table.find_ambiguous_main_ids(rows, "WPS_A")
        self.assertEqual(main_ids, {100, 200})


# Verbatim GetWeldingDataSetsFromDataBase() output, E2 R2026.1.2 / ArcTech 3.7.2.112.
# ML1 and ML2 are multilayer 1/2/3 pyramids, SL1 is single layer. Index 36 is False on
# every row, which is why Multilayer status cannot be read from it.
REAL_TABLE = [
    [1, 1, 'ML1', 'ST', 0.011, 0.0105, 0, 90.0, 0.0, 0, 0.025, 0.0015, False, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 1, 2, 2, 0.0, 0.0, 0.0, 0.0, 0.0, 0, False, False, True],
    [1, 3, 'ML1', 'ST', 0.011, 0.0105, 0, 90.0, 0.0, 0, 0.027, 0.0015, False, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2, 1, 3, 3, -5.0, 3.0, 0.003, 0.0011, 0.003, 0, False, False, True],
    [1, 5, 'ML1', 'ST', 0.011, 0.0105, 0, 90.0, 0.0, 0, 0.027, 0.0015, False, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2, 2, 3, 3, 5.0, 3.0, 0.003, 0.0011, -0.003, 0, False, False, True],
    [1, 2, 'ML1', 'ST', 0.011, 0.0105, 0, 90.0, 0.0, 0, 0.029, 0.0015, True, 0.1, 0.0025, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1, 4, 4, -6.0, 4.0, 0.006, 0.0012, 0.006, 8, False, False, True],
    [1, 4, 'ML1', 'ST', 0.011, 0.0105, 0, 90.0, 0.0, 0, 0.029, 0.0015, True, 0.1, 0.0025, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 2, 4, 4, 0.0, 4.0, 0.006, 0.0012, 0.0, 8, False, False, True],
    [1, 6, 'ML1', 'ST', 0.011, 0.0105, 0, 90.0, 0.0, 0, 0.029, 0.0015, True, 0.1, 0.0025, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 3, 4, 4, 6.0, 4.0, 0.006, 0.0012, -0.006, 8, False, False, True],
    [7, 1, 'SL1', 'AL', 0.006, 0.004, 3, 4.0, 0.005, 8, 0.001, 0.003, True, 13.0, 0.014, 15.0, 16.0, 0.017, 0.018, 19.0, 20.0, 21.0, 366.667, 23.0, 24.0, 5, 6, 1, 2, 7.0, 8.0, 0.01, 0.009, 0.011, 12, False, False, True],
]


class Test_RealArcTechTable(unittest.TestCase):
    def test_row_width_matches_layout(self):
        self.assertTrue(all(len(r) == process_table.Row.COUNT for r in REAL_TABLE))

    def test_index_36_is_not_a_multilayer_flag(self):
        self.assertTrue(all(r[process_table.Row.UNVERIFIED_FLAG] is False for r in REAL_TABLE))

    def test_multilayer_detected_by_pass_count(self):
        self.assertTrue(process_table.is_multilayer_wps(REAL_TABLE, "ML1"))
        self.assertFalse(process_table.is_multilayer_wps(REAL_TABLE, "SL1"))

    def test_layer_bead_pyramid_parsed_from_real_rows(self):
        records = [process_table.parse_row(r) for _, r in process_table.find_candidate_rows(REAL_TABLE, "ML1")]
        self.assertEqual([(r.sub_id, r.layer, r.bead) for r in records],
                         [(1, 1, 1), (3, 2, 1), (5, 2, 2), (2, 3, 1), (4, 3, 2), (6, 3, 3)])

    def test_first_unused_follows_table_order(self):
        index, record = process_table.select_first_unused(REAL_TABLE, "ML1")
        self.assertEqual(index, 0)
        self.assertEqual((record.main_id, record.sub_id, record.layer, record.bead), (1, 1, 1, 1))


def suite():
    loader = unittest.TestLoader()
    result = unittest.TestSuite()
    result.addTests(loader.loadTestsFromTestCase(Test_ParseRow))
    result.addTests(loader.loadTestsFromTestCase(Test_FindByStableId))
    result.addTests(loader.loadTestsFromTestCase(Test_SelectFirstUnused))
    result.addTests(loader.loadTestsFromTestCase(Test_AmbiguousMainIds))
    result.addTests(loader.loadTestsFromTestCase(Test_RealArcTechTable))
    return result


if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
