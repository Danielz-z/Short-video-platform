import sys
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


sys.path.append(str(Path(__file__).resolve().parents[1] / "backend"))

mysql_module = types.ModuleType("mysql")
connector_module = types.ModuleType("mysql.connector")
pooling_module = types.ModuleType("mysql.connector.pooling")


class FakeMysqlError(Exception):
    pass


connector_module.Error = FakeMysqlError
connector_module.connect = Mock()
connector_module.pooling = pooling_module
pooling_module.MySQLConnectionPool = Mock()
mysql_module.connector = connector_module

sys.modules.setdefault("mysql", mysql_module)
sys.modules.setdefault("mysql.connector", connector_module)
sys.modules.setdefault("mysql.connector.pooling", pooling_module)

from utils import db  # noqa: E402


class DbPoolTest(unittest.TestCase):
    def tearDown(self):
        db._pool = None

    @patch("utils.db.pooling.MySQLConnectionPool")
    def test_get_connection_pool_reuses_single_pool(self, pool_cls):
        pool_cls.return_value = Mock()

        first = db.get_connection_pool()
        second = db.get_connection_pool()

        self.assertIs(first, second)
        pool_cls.assert_called_once()

    @patch("utils.db.mysql.connector.connect")
    @patch("utils.db.get_connection_pool")
    def test_get_db_connection_falls_back_to_direct_connection(self, get_pool, connect):
        get_pool.side_effect = db.mysql.connector.Error("pool unavailable")
        connect.return_value = "direct-connection"

        self.assertEqual(db.get_db_connection(), "direct-connection")


if __name__ == "__main__":
    unittest.main()
