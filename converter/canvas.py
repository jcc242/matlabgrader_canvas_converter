import csv
import copy

def write_grades(filename, data):
    key = next(iter(data))
    assignment_id = []
    for item in data[key]:
        assignment_id += [item[1]]
    with open(filename, 'w+') as csvfile:
        writer = csv.writer(csvfile)
        headrow = ["Student"]
        for myid in assignment_id:
            headrow += [str(myid)] + [str(myid)]
        writer.writerow(headrow)
        for student in data:
            myrow = [student]
            for assignment in data[student]:
                myrow += [assignment[0]] + [assignment[1]]
            writer.writerow(myrow)

def format_grades(grades, key):
    for student in key:
        email = student[3]
        student.append(grades.get(email, [(0,0)])[0][0])
    return key
        
def list_unformated_grades(grades, key):
    tempGrades = copy.deepcopy(grades)
    for student in key:
        email = student[3]
        tempGrades.pop(email, None)
    return tempGrades
