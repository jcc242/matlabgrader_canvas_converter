import csv

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
