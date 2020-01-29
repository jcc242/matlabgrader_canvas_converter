def reduce_assignment_to_one_grade(data, num_cols_per_problem, grade_col, assignment_col):
    output = {}

    for student in data:
        num_problems = int(data[student][0])
        num_completed = int(data[student][1])
        grade_total = 0
        for i in range(num_completed):
            gradeidx = 2+grade_col+num_cols_per_problem*i
            grade_total += str_percent_to_float(data[student][gradeidx])

        grade_total /= num_problems
        assignment_id = int(data[student][2+assignment_col])
        output[student] = [(grade_total, assignment_id)]
    return output

def compute_grade(students, problems, assignments):
    for student in students:
        assignment_score = {}
        for grade in students[student].grades:
            for assign in assignments:
                for prob in assign.problems:
                    if prob.problem_id == grade.problem_id:
                        assignment_score[assign.assignment_id] += grade.score
        for assign in assignments:
            assignment_score[assign.assignment_id] /= assign.problems.size()
    return assignment_score



def str_percent_to_float(percent):
    return float(percent.strip('%')) / 100.0
