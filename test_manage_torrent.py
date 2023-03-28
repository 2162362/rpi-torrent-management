import unittest
import datetime
import io
from unittest import mock
from unittest.mock import patch, mock_open, call
from io import StringIO
from manage_torrent import copy_file

class TestCopyFile(unittest.TestCase):

    @patch('os.system')
    @patch('os.path.join')
    def test_copy_file_movies(self, mock_join, mock_system):
        mock_join.return_value = "movies/abc.mp4"
        with patch("builtins.open", mock_open()) as mock_file:
            copy_file("Movies", "/mnt/mitsai/torrents/movies/Tar.2022.x264/", "Tar.2022.x264")
            mock_file.assert_called_once_with('/mnt/mitsai/torrents/logs.txt', 'a+')
            mock_file().write.assert_called_once_with(mock.ANY)
            mock_system.assert_called_once_with("cp -r /mnt/mitsai/torrents/movies/Tar.2022.x264/ /mnt/seagate/jellyfin_media/movies/")

    @patch('os.system')
    @patch('os.path.join')
    def test_copy_file_series(self, mock_join, mock_system):
        date_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mock_join.return_value = "series/The.Last.of.Us.S01E05"
        with patch("builtins.open", mock_open()) as mock_file:
            copy_file("Series", "/mnt/mitsai/torrents/series/The.Last.of.Us.S01E05", "The.Last.of.Us.S01E05")
            mock_file.assert_called_once_with('/mnt/mitsai/torrents/logs.txt', 'a+')
            mock_file().write.assert_called_once_with(f"{date_string}: /mnt/mitsai/torrents/series/The.Last.of.Us.S01E05 was copied to /mnt/seagate/jellyfin_media/series/\n")
            mock_system.assert_called_once_with("cp -r /mnt/mitsai/torrents/series/The.Last.of.Us.S01E05 /mnt/seagate/jellyfin_media/series/")

    @patch('os.path.isfile', return_value=True)
    @patch('os.system')
    def test_copy_file_games(self, mock_system, mock_isfile):
        with patch("builtins.open", mock_open()) as mock_file:
            copy_file("Games", "/mnt/mitsai/torrents/games", "game01.iso")
            mock_file.assert_called_once_with('/mnt/mitsai/torrents/logs.txt', 'a+')
            mock_file().write.assert_called_once_with(mock.ANY)
            mock_system.assert_not_called()

    def test_copy_file_other(self):
        with patch("builtins.open", mock_open()) as mock_file:
            copy_file("Other", "/mnt/mitsai/torrents/documents", "doc01.pdf")
            mock_file.assert_called_once_with('/mnt/mitsai/torrents/logs.txt', 'a+')
            mock_file().write.assert_called_once_with(mock.ANY)

    @patch('os.system')
    @patch('os.path.join')
    def test_copy_file_series_execute_script(self, mock_join, mock_system):
        date_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mock_join.return_value = "custom_scripts/The.Last.of.Us.py"
        with patch("builtins.open", mock_open()) as mock_file:
            copy_file("Series", "/mnt/mitsai/torrents/series/The.Last.of.Us.S01E05", "The.Last.of.Us.S01E05")
            mock_file.assert_called_once_with('/mnt/mitsai/torrents/logs.txt', 'a+')
            mock_file().write.assert_has_calls([call(f"{date_string}: Executed custom script custom_scripts/The.Last.of.Us.py\n")])
            mock_system.assert_has_calls([
                call("cp -r /mnt/mitsai/torrents/series/The.Last.of.Us.S01E05 /mnt/seagate/jellyfin_media/series/"),
                call("python custom_scripts/The.Last.of.Us.py /mnt/seagate/jellyfin_media/series/ The.Last.of.Us.S01E05")
            ])


if __name__ == "__main__":
    unittest.main()
