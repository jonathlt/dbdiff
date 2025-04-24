import unittest
from unittest.mock import patch, MagicMock
from pg_utils import build_exclusion_list, get_sql, run_sql, get_data

class TestPgUtils(unittest.TestCase):
    @patch("pg_utils.Path.iterdir")
    @patch("pg_utils.csvfile_to_list")
    def test_build_exclusion_list(self, mock_csvfile_to_list, mock_iterdir):
        # Mock the files in the directory
        mock_iterdir.return_value = [MagicMock(), MagicMock()]
        mock_csvfile_to_list.side_effect = [["item1", "item2"], ["item3"]]

        exclusion_list = build_exclusion_list("tables")
        self.assertEqual(exclusion_list, ["item1", "item2", "item3"])
        mock_iterdir.assert_called_once()
        self.assertEqual(mock_csvfile_to_list.call_count, 2)

    @patch("pg_utils.configparser.ConfigParser")
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="SELECT * FROM table;")
    def test_get_sql(self, mock_open, mock_config_parser):
        mock_config = MagicMock()
        mock_config.get.return_value = "sqlfile.sql"
        mock_config_parser.return_value = mock_config

        sql = get_sql("query_name", "config.ini")
        self.assertEqual(sql, "SELECT * FROM table;")
        mock_config.get.assert_called_with("query_name", "sqlfile")

    @patch("pg_utils.pg8000.native.Connection.run")
    @patch("pg_utils.pg8000.native.Connection.columns", new_callable=MagicMock)
    def test_run_sql(self, mock_columns, mock_run):
        mock_run.return_value = [[1, "data1"], [2, "data2"]]
        mock_columns.return_value = [{"name": "id"}, {"name": "value"}]

        conn = MagicMock()
        conn.run = mock_run
        conn.columns = [{"name": "id"}, {"name": "value"}]

        result = run_sql(conn, "SELECT * FROM table;", "resultkey")
        expected = {
            "resultkey": [
                {"id": 1, "value": "data1"},
                {"id": 2, "value": "data2"}
            ]
        }
        self.assertEqual(result, expected)
        mock_run.assert_called_once_with("SELECT * FROM table;")

    @patch("pg_utils.get_sql")
    @patch("pg_utils.get_connection")
    @patch("pg_utils.run_sql")
    def test_get_data(self, mock_run_sql, mock_get_connection, mock_get_sql):
        mock_get_sql.return_value = "SELECT * FROM table;"
        mock_get_connection.return_value = MagicMock()
        mock_run_sql.return_value = {"resultkey": [{"id": 1, "value": "data1"}]}

        result = get_data("db_alias", "queryname", "resultkey")
        expected = {"resultkey": [{"id": 1, "value": "data1"}]}
        self.assertEqual(result, expected)
        mock_get_sql.assert_called_once_with("queryname", "config.ini")
        mock_get_connection.assert_called_once_with("db_alias", "config.ini")
        mock_run_sql.assert_called_once_with(mock_get_connection.return_value, "SELECT * FROM table;", "resultkey")

if __name__ == "__main__":
    unittest.main()