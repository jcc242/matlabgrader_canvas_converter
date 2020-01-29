from unittest import TestCase

from textwrap import dedent

from converter import grade

class GradeTest(TestCase):
    DATA = {'student1@mail.edu' : ['2', '2', '4', '4', '1', '100%', '123456', '12345', 'N', '6', '6', '1', '100%', '123457', '12345', 'N'],
            'student2@mail.edu' : ['2', '2', '3', '4', '1',  '75%', '123456', '12345', 'N', '3', '6', '1',  '50%', '123457', '12345', 'N'],
            'student3@mail.edu' : ['2', '2', '0', '4', '1',   '0%', '123456', '12345', 'N', '0', '6', '1',   '0%', '123457', '12345', 'N'],
            'student4@mail.edu' : ['2', '1', '3', '6', '1',  '50%', '123457', '12345', 'N']}

    num_cols_per_problem = 7
    grade_col = 3
    assignment_col = 5

    def test_reduce_assignment_to_one_grade(self):
        graded = grade.reduce_assignment_to_one_grade(self.DATA,
                                                      self.num_cols_per_problem,
                                                      self.grade_col,
                                                      self.assignment_col)
        self.assertEqual(graded, {'student1@mail.edu' : [(1.,12345)],
                                  'student2@mail.edu' : [(0.625,12345)],
                                  'student3@mail.edu' : [(0.,12345)],
                                  'student4@mail.edu' : [(0.25,12345)]})

    def test_str_percent_to_float(self):
        data1 = '0%'
        data2 = '12.5%'
        data3 = '100%'

        output1 = grade.str_percent_to_float(data1)
        output2 = grade.str_percent_to_float(data2)
        output3 = grade.str_percent_to_float(data3)

        self.assertEqual(0., output1)
        self.assertEqual(0.125, output2)
        self.assertEqual(1., output3)
