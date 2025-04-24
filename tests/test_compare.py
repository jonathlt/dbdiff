import unittest
from compare import compare
from pg_utils import build_exclusion_list, get_database_name

class TestCompareFunction(unittest.TestCase):
    def test_items_added_and_removed(self):
        dict1 = {"tables": ["table1", "table2", "table3"]}
        dict2 = {"tables": ["table2", "table4"]}
        added, removed = compare(dict1, dict2, "tables")
        self.assertEqual(added, ["table4"])
        self.assertEqual(removed, ["table1", "table3"])

    def test_no_difference(self):
        dict1 = {"tables": ["table1", "table2"]}
        dict2 = {"tables": ["table1", "table2"]}
        added, removed = compare(dict1, dict2, "tables")
        self.assertEqual(added, [])
        self.assertEqual(removed, [])

    def test_empty_dict1(self):
        dict1 = {"tables": []}
        dict2 = {"tables": ["table1", "table2"]}
        added, removed = compare(dict1, dict2, "tables")
        self.assertEqual(added, ["table1", "table2"])
        self.assertEqual(removed, [])

    def test_empty_dict2(self):
        dict1 = {"tables": ["table1", "table2"]}
        dict2 = {"tables": []}
        added, removed = compare(dict1, dict2, "tables")
        self.assertEqual(added, [])
        self.assertEqual(removed, ["table1", "table2"])

    def test_empty_both_dicts(self):
        dict1 = {"tables": []}
        dict2 = {"tables": []}
        added, removed = compare(dict1, dict2, "tables")
        self.assertEqual(added, [])
        self.assertEqual(removed, [])

class TestPgUtilsFunctions(unittest.TestCase):
    def test_build_exclusion_list(self):
        exclusion_key = "tables"
        exclusion_list = build_exclusion_list(exclusion_key)
        self.assertIsInstance(exclusion_list, list)
        self.assertTrue(all(isinstance(item, str) for item in exclusion_list))

    def test_get_database_name(self):
        db_name = get_database_name("database1")
        self.assertIsInstance(db_name, str)
        self.assertTrue(len(db_name) > 0)

if __name__ == '__main__':
    unittest.main()