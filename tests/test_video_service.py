import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


sys.path.append(str(Path(__file__).resolve().parents[1] / "backend"))

from services import video_service  # noqa: E402


class VideoServiceTest(unittest.TestCase):
    @patch("services.video_service.video_dao")
    def test_update_video_requires_author(self, video_dao):
        conn = Mock()
        video_dao.get_video_author.return_value = "owner-id"

        video_service.update_video(conn, "video-id", "New title", "owner-id")

        video_dao.update_video_title.assert_called_once_with(conn, "video-id", "New title")

    @patch("services.video_service.video_dao")
    def test_update_video_rejects_non_author(self, video_dao):
        conn = Mock()
        video_dao.get_video_author.return_value = "owner-id"

        with self.assertRaises(PermissionError):
            video_service.update_video(conn, "video-id", "New title", "other-user")

        video_dao.update_video_title.assert_not_called()

    @patch("services.video_service.video_dao")
    def test_delete_video_requires_author(self, video_dao):
        conn = Mock()
        video_dao.get_video_author.return_value = "owner-id"

        video_service.delete_video(conn, "video-id", "owner-id")

        video_dao.delete_video_by_id.assert_called_once_with(conn, "video-id")


if __name__ == "__main__":
    unittest.main()
