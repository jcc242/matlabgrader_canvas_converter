from unittest import TestCase
from unittest.mock import patch, mock_open

from textwrap import dedent

from converter import organize

class OrganizeTest(TestCase):

    DATA = [['student1@mail.edu', '12345678', '87654321', "% This script computes the exponential growth rate of doubling\n% the number of grains of rice per chess board square.\nclc; close all;\n% DO NOT use the clear command, it prevents MATLAB Grader from checking\n% your work and you won't get credit. You don't need to clear on MATLAB grader.\n% Make sure you define the variables x_0, r, t, and x_t below.\nx_0=1/2\nr=1\nt=64\nx_t=x_0*(r+1)^(t)", '4', '4', '2018-09-09 20:18:12 MDT', '1', '32', '100%', '123456', 'My first problem name', '123456', '12345', 'My assignment name', 'N'],
            ['student2@mail.edu', '12345678', '87654321', "% This script computes the exponential growth rate of doubling\n% the number of grains of rice per chess board square.\nclc; close all;\n% DO NOT use the clear command, it prevents MATLAB Grader from checking\n% your work and you won't get credit. You don't need to clear on MATLAB grader.\n% Make sure you define the variables x_0, r, t, and x_t below.\nx_0=(1/2);\nt=64;\nr=1;\nx_t=x_0*(1+r)^t\n", '3', '4', '2018-09-10 09:42:44 MDT', '1', '32', '75%', '123456', 'My first problem name', '123456', '12345', 'My assignment name', 'N'],
            ['student3@mail.edu', '12345678', '12345678', "% This script computes the exponential growth rate of doubling\n% the number of grains of rice per chess board square.\nclc; close all;\n% DO NOT use the clear command, it prevents MATLAB Grader from checking\n% your work and you won't get credit. You don't need to clear on MATLAB grader.\n% Make sure you define the variables x_0, r, t, and x_t below.\nx_0=0.5;\nr=1;\nt=64\nx_t=x_0*(1+r)^t;\n\n", '0', '4', '2019-09-09 10:00:53 MDT', '1', '29', '0%', '123456', 'My first problem name', '123456', '12345', 'My assignment name', 'N'],
            ['student1@mail.edu', '12345678', '87654321', '%This script computes the specific gravity of three balls\nclc; close all;\n%Do NOT use a calculator to make the conversion! Write the conversion formula here and let MATLAB calculate it.\n%Define variables: circumfrence, radius, volume, mass, density, and specificGravity below\ncircumference=8\ncmcir=circumference*2.54\nradius=cmcir/2/pi\nvolume=(4/3)*pi*radius^3\nmass=160\ndensity=mass/volume\nspecificGravity=density/1\n\n\n\n\n%Write the formula for specificGravity below', '6', '6', '2019-10-10 21:30:37 MDT', '1', '55', '100%', '123457', 'My second problem name', '123457', '12345', 'My assignment name', 'N'],
            ['student2@mail.edu', '12345678', '87654321', '%This script computes the specific gravity of three balls\nclc; close all;\n%Do NOT use a calculator to make the conversion! Write the conversion formula here and let MATLAB calculate it.\n%Define variables: circumfrence, radius, volume, mass, density, and specificGravity below\ncircumference=8;\nradius=(circumference/(2*pi))*2.54;\nvolume=(4/3)*pi*(radius^3);\nmass=160;\ndensity=mass/volume;\nspecificGravity=density/1\n\n\n\n%Write the formula for specificGravity below', '3', '6', '2019-10-04 10:10:11 MDT', '1', '54', '50%', '123457', 'My second problem name', '123457', '12345', 'My assignment name', 'N'],
            ['student3@mail.edu', '12345678', '87654321', '%This script computes the specific gravity of three balls\nclc; close all;\n%Do NOT use a calculator to make the conversion! Write the conversion formula here and let MATLAB calculate it.\n%Define variables: circumfrence, radius, volume, mass, density, and specificGravity below\ncircumference=8;\nradius=((circumference)/(2*pi))*(2.54)\nvolume=(4/3)*(pi)*(radius)^3\nmass=160;\ndensity=mass/volume\nspecificGravity=density/1\n\n\n\n\n\n%Write the formula for specificGravity below', '0', '6', '2019-10-09 10:15:58 MDT', '1', '57', '0%', '123457', 'My second problem name', '123457', '12345', 'My assignment name', 'N'],
            ['student4@mail.edu', '12345678', '87654321', '%This script computes the specific gravity of three balls\nclc; close all;\n%Do NOT use a calculator to make the conversion! Write the conversion formula here and let MATLAB calculate it.\n%Define variables: circumfrence, radius, volume, mass, density, and specificGravity below\ncircumference=8;\nradius=((circumference)/(2*pi))*(2.54)\nvolume=(4/3)*(pi)*(radius)^3\nmass=160;\ndensity=mass/volume\nspecificGravity=density/1\n\n\n\n\n\n%Write the formula for specificGravity below', '3', '6', '2019-10-09 10:15:58 MDT', '1', '57', '50%', '123457', 'My second problem name', '123457', '12345', 'My assignment name', 'N']]


    GRADES1 = {'student1@mail.edu' : [(1.,12345)],
               'student2@mail.edu' : [(0.625,12345)],
               'student3@mail.edu' : [(0.,12345)],
               'student4@mail.edu' : [(0.25,12345)],
               'student5@mail.edu' : [(0.25,12345)]}

    GRADES2 = {'student1@mail.edu' : [(0.9,12346)],
               'student2@mail.edu' : [(0.7,12346)],
               'student3@mail.edu' : [(0.6,12346)],
               'student4@mail.edu' : [(0.5,12346)]}

    keep_columns = [0,4,5,7,9,10,13,15]
    prob_id_column_before_filter = 10
    prob_id_columns_after_filter = 5

    def test_filter_info(self):
        filtered_data = organize.filter_info(self.DATA, self.keep_columns)
        self.assertEqual(filtered_data, [['student1@mail.edu', '4', '4', '1', '100%', '123456', '12345', 'N'],
                                         ['student2@mail.edu', '3', '4', '1',  '75%', '123456', '12345', 'N'],
                                         ['student3@mail.edu', '0', '4', '1',   '0%', '123456', '12345', 'N'],
                                         ['student1@mail.edu', '6', '6', '1', '100%', '123457', '12345', 'N'],
                                         ['student2@mail.edu', '3', '6', '1',  '50%', '123457', '12345', 'N'],
                                         ['student3@mail.edu', '0', '6', '1',   '0%', '123457', '12345', 'N'],
                                         ['student4@mail.edu', '3', '6', '1',  '50%', '123457', '12345', 'N']])

    def test_build_split_indices(self):
        indices = organize.build_split_indices(self.DATA, self.prob_id_column_before_filter)

        self.assertEqual(indices, [3])

    def test_split_problems(self):
        filtered_data = organize.filter_info(self.DATA, self.keep_columns)
        indices = organize.build_split_indices(filtered_data, self.prob_id_columns_after_filter)
        problems = organize.split_problems(filtered_data, indices)

        self.assertEqual(problems, [[['student1@mail.edu','4', '4', '1', '100%', '123456', '12345', 'N'],
                                     ['student2@mail.edu', '3', '4', '1',  '75%', '123456', '12345', 'N'],
                                     ['student3@mail.edu', '0', '4', '1',   '0%', '123456', '12345', 'N']],
                                    [['student1@mail.edu', '6', '6', '1', '100%', '123457', '12345', 'N'],
                                     ['student2@mail.edu', '3', '6', '1',  '50%', '123457', '12345', 'N'],
                                     ['student3@mail.edu', '0', '6', '1',   '0%', '123457', '12345', 'N'],
                                     ['student4@mail.edu', '3', '6', '1',  '50%', '123457', '12345', 'N']]])

    def test_combine_problems_by_student(self):
        filtered_data = organize.filter_info(self.DATA, self.keep_columns)
        indices = organize.build_split_indices(filtered_data, self.prob_id_columns_after_filter)
        problems = organize.split_problems(filtered_data, indices)

        combined_problems = organize.combine_problems_by_student(problems)

        self.assertEqual(combined_problems, {'student1@mail.edu' : ['2', '2', '4', '4', '1', '100%', '123456', '12345', 'N', '6', '6', '1', '100%', '123457', '12345', 'N'],
                                             'student2@mail.edu' : ['2', '2', '3', '4', '1',  '75%', '123456', '12345', 'N', '3', '6', '1',  '50%', '123457', '12345', 'N'],
                                             'student3@mail.edu' : ['2', '2', '0', '4', '1',   '0%', '123456', '12345', 'N', '0', '6', '1',   '0%', '123457', '12345', 'N'],
                                             'student4@mail.edu' : ['2', '1', '3', '6', '1',  '50%', '123457', '12345', 'N']})
    def test_combine_grades(self):
        combined_grades = organize.combine_grades(self.GRADES1, self.GRADES2)

        self.assertEqual(combined_grades, {'student1@mail.edu' : [(1.,12345), (0.9,12346)],
                                           'student2@mail.edu' : [(0.625,12345), (0.7,12346)],
                                           'student3@mail.edu' : [(0.,12345), (0.6,12346)],
                                           'student4@mail.edu' : [(0.25,12345), (0.5,12346)],
                                           'student5@mail.edu' : [(0.25,12345)]})

    def test_create_assignment_from_csv(self):
        assignment = organize.create_assignment_from_csv(self.DATA)

        self.assertEqual(assignment.name, 'My assignment name')
        self.assertEqual(assignment.assignment_id, 12345)

    def test_convert_csv_to_problems(self):
        problems = organize.convert_csv_to_problems(self.DATA)

        self.assertEqual(problems[0].name, 'My first problem name')
        self.assertEqual(problems[0].problem_id, 123456)
        self.assertEqual(problems[1].name, 'My second problem name')
        self.assertEqual(problems[1].problem_id, 123457)

    def test_read_csv_to_students(self):
        students = organize.read_csv_to_students(self.DATA)

        self.assertEqual(students['student1@mail.edu'].grades[0].problem_id, 123456)
        self.assertEqual(students['student1@mail.edu'].grades[1].problem_id, 123457)
        self.assertEqual(students['student1@mail.edu'].grades[0].grade, 1.0)
        self.assertEqual(students['student1@mail.edu'].grades[1].grade, 1.0)

        self.assertEqual(students['student2@mail.edu'].grades[0].problem_id, 123456)
        self.assertEqual(students['student2@mail.edu'].grades[1].problem_id, 123457)
        self.assertEqual(students['student2@mail.edu'].grades[0].grade, 0.75)
        self.assertEqual(students['student2@mail.edu'].grades[1].grade, 0.5)

        self.assertEqual(students['student3@mail.edu'].grades[0].problem_id, 123456)
        self.assertEqual(students['student3@mail.edu'].grades[1].problem_id, 123457)
        self.assertEqual(students['student3@mail.edu'].grades[0].grade, 0.0)
        self.assertEqual(students['student3@mail.edu'].grades[1].grade, 0.0)

        self.assertEqual(students['student4@mail.edu'].grades[0].problem_id, 123457)
        self.assertEqual(students['student4@mail.edu'].grades[0].grade, 0.5)
