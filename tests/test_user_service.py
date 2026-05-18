import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


sys.path.append(str(Path(__file__).resolve().parents[1] / "backend"))

from services import user_service  # noqa: E402


class UserServiceTest(unittest.TestCase):
    def test_validate_password_requires_length_letters_and_digits(self):
        self.assertTrue(user_service.validate_password("DemoPass123"))
        self.assertFalse(user_service.validate_password("short1"))
        self.assertFalse(user_service.validate_password("NoDigitsHere"))
        self.assertFalse(user_service.validate_password("12345678"))

    def test_normalize_role_accepts_known_roles(self):
        self.assertEqual(user_service.normalize_role("admin"), "admin")
        self.assertEqual(user_service.normalize_role("USER"), "user")
        self.assertEqual(user_service.normalize_role(None), "user")

    def test_normalize_role_rejects_unknown_roles(self):
        with self.assertRaises(ValueError):
            user_service.normalize_role("owner")

    @patch("services.user_service.user_dao")
    def test_is_admin_uses_role_field(self, user_dao):
        conn = Mock()
        user_dao.get_user_by_id.return_value = {"user_id": "u1", "username": "alice", "role": "admin"}

        self.assertTrue(user_service.is_admin(conn, "u1"))

        user_dao.get_user_by_id.return_value = {"user_id": "u2", "username": "admin_name_only", "role": "user"}
        self.assertFalse(user_service.is_admin(conn, "u2"))

    @patch("services.user_service.generate_password_hash", return_value="hashed-password")
    @patch("services.user_service.user_dao")
    def test_register_user_hashes_password_and_persists_role(self, user_dao, _hash):
        conn = Mock()

        user_id = user_service.register_user(conn, "creator", "creator@example.com", "DemoPass123", "admin")

        self.assertTrue(user_id)
        user_dao.create_user.assert_called_once()
        args = user_dao.create_user.call_args.args
        self.assertEqual(args[2], "creator")
        self.assertEqual(args[4], "hashed-password")
        self.assertEqual(args[5], "admin")


if __name__ == "__main__":
    unittest.main()
