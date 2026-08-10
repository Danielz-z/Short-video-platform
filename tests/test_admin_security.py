import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.append(str(Path(__file__).resolve().parents[1] / "backend"))

from routes import admin  # noqa: E402


class AdminSecurityTest(unittest.TestCase):
    def test_resolve_backup_file_accepts_generated_existing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_dir = Path(temp_dir)
            backup_file = backup_dir / "backup_20260810_120000.sql"
            backup_file.write_text("SELECT 1;", encoding="utf-8")

            with patch.object(admin, "BACKUP_DIR", backup_dir):
                resolved = admin._resolve_backup_file(backup_file.name)

            self.assertEqual(resolved, backup_file.resolve())

    def test_resolve_backup_file_rejects_untrusted_names(self):
        invalid_names = (
            "../backup_20260810_120000.sql",
            "notes.sql",
            "backup_2026810_120000.sql",
            "backup_20260810_120000.sql.bak",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.object(admin, "BACKUP_DIR", Path(temp_dir)):
                for filename in invalid_names:
                    with self.subTest(filename=filename):
                        with self.assertRaises(ValueError):
                            admin._resolve_backup_file(filename)

    def test_resolve_backup_file_rejects_missing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.object(admin, "BACKUP_DIR", Path(temp_dir)):
                with self.assertRaises(ValueError):
                    admin._resolve_backup_file("backup_20260810_120000.sql")

    def test_resolve_backup_file_rejects_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_dir = Path(temp_dir)
            (backup_dir / "backup_20260810_120000.sql").mkdir()

            with patch.object(admin, "BACKUP_DIR", backup_dir):
                with self.assertRaises(ValueError):
                    admin._resolve_backup_file("backup_20260810_120000.sql")


if __name__ == "__main__":
    unittest.main()
