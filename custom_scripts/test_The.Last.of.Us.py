import os
import unittest
from unittest.mock import patch, mock_open
import importlib.util
import imp
my_module = imp.load_source('*', 'The.Last.of.Us.py')

class TestTheLastOfUs(unittest.TestCase):
    def setUp(self):
        self.file_name = "file_name"
        self.destination = "destination"
        self.full_path = os.path.join(self.destination, self.file_name)

    def test_no_arguments(self):
        with patch("sys.stderr", new=mock_open()) as fake_stderr:
            with self.assertRaises(SystemExit):
                main([])
        fake_stderr.assert_called_once_with()

    def test_missing_file(self):
        with patch("os.path.isfile", return_value=False):
            with self.assertRaises(FileNotFoundError):
                main([self.destination, self.file_name])

    def test_copy_file(self):
        with patch("os.path.isfile", return_value=True):
            with patch("shutil.copy2") as mock_copy:
                main([self.destination, self.file_name])
        mock_copy.assert_called_once_with(self.full_path, "../The Last of Us/Season 1/file_name")

    def test_copy_file_without_extension(self):
        file_name_without_ext = "file_name_without_ext"
        full_path_without_ext = os.path.join(self.destination, file_name_without_ext)
        with patch("os.path.isfile", side_effect=[False, True]):
            with patch("os.path.splitext", return_value=[file_name_without_ext, ""]) as mock_splitext:
                with patch("shutil.copy2") as mock_copy:
                    main([self.destination, file_name_without_ext])
        mock_splitext.assert_called_once_with(self.file_name)
        mock_copy.assert_called_once_with(full_path_without_ext, "../The Last of Us/Season 1/file_name_without_ext")


if __name__ == "__main__":
    unittest.main()
