import os
from unittest import TestCase
from unittest.mock import patch, mock_open, call

from textwrap import dedent

from converter import canvas

class CanvasTest(TestCase):
    DATA = {'student1@mail.edu' : (1.,12345),
            'student2@mail.edu' : (0.625,12345),
            'student3@mail.edu' : (0.,12345),
            'student4@mail.edu' : (0.25,12345)}

    MULTIDATA = {'student1@mail.edu' : [(1.,12345), (0.9,12346)],
                 'student2@mail.edu' : [(0.625,12345), (0.7,12346)],
                 'student3@mail.edu' : [(0.,12345), (0.6,12346)],
                 'student4@mail.edu' : [(0.25,12345), (0.5,12346)],
                 'student5@mail.edu' : [(0.5,12346)]}

    @patch("builtins.open", mock_open())
    def test_save_file(self):
        filename = "filename"
        canvas.write_grades(filename, self.DATA)

        # self.assertEqual(os.path.exists.received_args[0], filename)
        open.assert_called_once_with("filename", "w+")
        handle = open()
        calls = [call('Student,12345\r\n'),
                 call('student1@mail.edu,1.0\r\n'),
                 call('student2@mail.edu,0.625\r\n'),
                 call('student3@mail.edu,0.0\r\n'),
                 call('student4@mail.edu,0.25\r\n')]
        handle.write.assert_has_calls(calls, any_order=False)

    @patch("builtins.open", mock_open())
    def test_save_file(self):
        filename = "filename"
        canvas.write_grades(filename, self.MULTIDATA)

        # self.assertEqual(os.path.exists.received_args[0], filename)
        open.assert_called_once_with("filename", "w+")
        handle = open()
        calls = [call('Student,12345,12345,12346,12346\r\n'),
                 call('student1@mail.edu,1.0,12345,0.9,12346\r\n'),
                 call('student2@mail.edu,0.625,12345,0.7,12346\r\n'),
                 call('student3@mail.edu,0.0,12345,0.6,12346\r\n'),
                 call('student4@mail.edu,0.25,12345,0.5,12346\r\n'),
                 call('student5@mail.edu,0.5,12346\r\n')]
        handle.write.assert_has_calls(calls, any_order=False)

