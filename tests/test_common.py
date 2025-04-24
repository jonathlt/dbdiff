import unittest
from common import update_value

class TestUpdateValue(unittest.TestCase):
    def test_update_existing_key(self):
        data = [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]
        update_value(data, 'age', 35)
        self.assertEqual(data, [{'name': 'Alice', 'age': 35}, {'name': 'Bob', 'age': 35}])

    def test_add_new_key(self):
        data = [{'name': 'Alice'}, {'name': 'Bob'}]
        update_value(data, 'age', 35)
        self.assertEqual(data, [{'name': 'Alice', 'age': 35}, {'name': 'Bob', 'age': 35}])

    def test_empty_list(self):
        data = []
        update_value(data, 'age', 35)
        self.assertEqual(data, [])

    def test_mixed_keys(self):
        data = [{'name': 'Alice', 'age': 25}, {'name': 'Bob'}]
        update_value(data, 'age', 35)
        self.assertEqual(data, [{'name': 'Alice', 'age': 35}, {'name': 'Bob', 'age': 35}])

if __name__ == '__main__':
    unittest.main()