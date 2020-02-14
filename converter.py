#!/usr/bin/python3

import sys, getopt
from converter import myload, organize, grade, canvas


def main(argv):
    inputdir = ''
    outputfile = ''

    helpstring = 'convert.py -i <inputfile> -o <outputfile>'

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print(helpstring)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(helpstring)
            sys.exit()
        elif opt in ("-i","--ifile"):
            inputfile = arg
        elif opt in ("-o","--ofile"):
            outputfile = arg
    if(not inputfile) or (not outputfile):
        print("Need an input file and an output file")
        sys.exit(2)

    # files = myload.get_csv_files(inputfile)
    # print("Files: {}".format(files))

    # all_grades = []
    # assignments = []

    # for inputfile in files:
    with open(inputfile, 'r') as myfile:
        data = myload.parse_csv(myfile)

        # problems = organize.convert_csv_to_problems(data)
        # assignments += [organize.create_assignment_from_csv(data)]
        # students += [organize.read_csv_to_students(data)]

    keep_columns = [1,5,6,8,10,11,14,16]
    prob_id_column_before_filter = 11
    prob_id_column_after_filter = 5

    filtered = organize.filter_info(data, keep_columns)
    indices = organize.build_split_indices(filtered, prob_id_column_after_filter)
    combined_problems = organize.combine_problems_by_student(organize.split_problems(filtered, indices))

    num_cols_per_problem = 7
    grade_col = 3
    assignment_col = 5
    graded = grade.reduce_assignment_to_one_grade(combined_problems,
                                                  num_cols_per_problem,
                                                  grade_col,
                                                  assignment_col)

        # all_grades.append(graded)

    # reduced_grades = all_grades[0]
    # itergrades = iter(all_grades)
    # next(itergrades)
    # for grades in itergrades:
    #     reduced_grades = organize.combine_grades(reduced_grades,grades)

    # print("reduced grades: {}".format(reduced_grades))
    canvas.write_grades(outputfile, graded)

if __name__ == "__main__":
    main(sys.argv[1:])
