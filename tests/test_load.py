from unittest import TestCase
from unittest.mock import patch, mock_open

from textwrap import dedent

from converter import myload

class OpenTest(TestCase):
    DATA = dedent("""
        head1,head2,head3
        a,b,c
        x,y,z
        """).strip()

    @patch("builtins.open", mock_open(read_data=DATA))
    def test_load_file(self):

        filehandle = myload.load_file("filename")

        data = filehandle.read()

        open.assert_called_once_with("filename", "r")
        self.assertEqual(self.DATA, data)
        self.assertEqual("head1,head2,head3\na,b,c\nx,y,z", data)

    @patch("builtins.open", mock_open(read_data=DATA))
    def test_parse_csv(self):
        filehandle = myload.load_file("filename")
        data = myload.parse_csv(filehandle)
        self.assertEqual(data[0], ['a','b','c'])
        self.assertEqual(data[1], ['x','y','z'])
