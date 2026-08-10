import ast
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.append(str(Path(__file__).resolve().parents[1] / "backend"))

from routes import admin  # noqa: E402


class AdminSecurityTest(unittest.TestCase):
    def test_flask_entry_point_does_not_enable_debug(self):
        app_path = Path(__file__).resolve().parents[1] / "backend" / "app.py"
        tree = ast.parse(app_path.read_text(encoding="utf-8"))
        run_calls = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "app"
            and node.func.attr == "run"
        ]

        self.assertEqual(len(run_calls), 1)
        debug_keywords = [keyword for keyword in run_calls[0].keywords if keyword.arg == "debug"]
        if debug_keywords:
            self.assertIsInstance(debug_keywords[0].value, ast.Constant)
            self.assertIs(debug_keywords[0].value.value, False)

    def test_resolve_backup_file_accepts_generated_existing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_dir = Path(temp_dir)
            backup_file = backup_dir / "backup_20260810_120000.sql"
            backup_file.write_text("SELECT 1;", encoding="utf-8")

            with patch.object(admin, "BACKUP_DIR", backup_dir):
                resolved = admin._resolve_backup_file(backup_file.name)

            self.assertEqual(resolved, backup_file)

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

    def test_resolve_backup_file_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_dir = Path(temp_dir)
            target = backup_dir / "target.sql"
            target.write_text("SELECT 1;", encoding="utf-8")
            symlink = backup_dir / "backup_20260810_120000.sql"
            symlink.symlink_to(target)

            with patch.object(admin, "BACKUP_DIR", backup_dir):
                with self.assertRaises(ValueError):
                    admin._resolve_backup_file(symlink.name)

    def test_resolve_backup_file_rejects_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_dir = Path(temp_dir)
            (backup_dir / "backup_20260810_120000.sql").mkdir()

            with patch.object(admin, "BACKUP_DIR", backup_dir):
                with self.assertRaises(ValueError):
                    admin._resolve_backup_file("backup_20260810_120000.sql")


if __name__ == "__main__":
    unittest.main()
