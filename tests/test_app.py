import unittest
from app import profile_rows
class DataQualityTests(unittest.TestCase):
    def test_missing_duplicate_and_schema_checks(self):
        rows=[{"id":"1","amount":"10"},{"id":"2","amount":""},{"id":"2","amount":""}]
        result=profile_rows(rows,["id","amount","email"])
        self.assertEqual(result["duplicate_rows"],1)
        self.assertIn("missing_columns",[issue["type"] for issue in result["issues"]])
        self.assertEqual(result["missing_cells"]["amount"],2)
    def test_empty_dataset_rejected(self):
        with self.assertRaises(ValueError): profile_rows([])
    def test_row_count(self):
        self.assertEqual(profile_rows([{"a":"1"},{"a":"2"}])["row_count"],2)
if __name__=="__main__": unittest.main()
