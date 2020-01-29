from itertools import chain
from converter import grade

class Student:
    def __init__(self, email):
        self.email = email
        self.grades = []

    def add_grade(self, grade):
        self.grades.append(grade)

class Problem:
    def __init__(self, name, problem_id):
        self.problem_id = problem_id
        self.name = name

class Assignment:
    def __init__(self, name, assignment_id):
        self.assignment_id = assignment_id
        self.name = name
        self.problems = []

    def addProblem(self, problem):
        self.problems.append(problem)

class Grade:
    def __init__(self, problem_id, score):
        self.score = score
        self.problem_id = problem_id


def split_problems(data, indices):
    temp = zip(chain([0], indices), chain(indices, [None]))
    res = list(data[i : j] for i,j in temp)
    return res

def build_split_indices(data, id_col):
    last_id = data[0][id_col];
    indices = []
    for index, row in enumerate(data) :
        if row[id_col] != last_id:
            last_id = row[id_col]
            indices.append(index)
    return indices

def filter_info(data, keep_columns):
    output = []
    for row in data:
        new_row = []
        for col in keep_columns:
            new_row.append(row[col])
        output.append(new_row)
    return output

def combine_problems_by_student(problem_list):
    output = {}
    num_problems = len(problem_list)
    for problem in problem_list:
        for student in problem:
            if student[0] in output:
                existing = output[student[0]]
                num_seen = int(existing[1])
                num_seen += 1
                existing[1] = str(num_seen)
                output[student[0]] = existing + student[1:]
            else:
                output[student[0]] = [str(num_problems)] + ['1'] + student[1:]
    return output

def combine_grades(first, second):
    output = {}
    for student in first:
        output[student] = first[student]
    for student in second:
        grade = second[student]
        if student in first:
            output[student] = first[student] + grade
        else:
            output[student] = grade
    return output

def create_assignment_from_csv(csvdata):
    return Assignment(csvdata[0][14],int(csvdata[0][13]))

def convert_csv_to_problems(csvdata):
    id_col = 10
    indices = build_split_indices(csvdata, id_col)
    problems = []
    problems.append(Problem(csvdata[0][11], int(csvdata[0][10])))
    for idx in indices:
        problems.append(Problem(csvdata[idx][11], int(csvdata[idx][10])))

    return problems

def read_csv_to_students(data):
    students = {}
    for row in data:
        grade_val = grade.str_percent_to_float(row[9])
        prob_id = int(row[10])
        grade_prob = Grade(prob_id, grade_val)
        student_email = row[0]
        if student_email in students:
            student = students[student_email]
            student.add_grade(grade_prob)
        else:
            student = Student(student_email)
            student.add_grade(grade_prob)
            students[student_email] = student
    return students
