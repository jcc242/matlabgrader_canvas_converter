#!/usr/bin/python3

import sys, getopt, csv
from converter import myload, organize, grade, canvas


def main(argv):
    inputdir = ''
    outputfile = ''
    keyfile = ''

    helpstring = 'convert.py -i <inputfile> -o <outputfile>'

    try:
        opts, args = getopt.getopt(argv,"hi:o:k:",["infile=","outfile=","keyfile="])
    except getopt.GetoptError:
        print(helpstring)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(helpstring)
            sys.exit()
        elif opt in ("-i","--infile"):
            inputfile = arg
        elif opt in ("-o","--outfile"):
            outputfile = arg
        elif opt in ("-k","--keyfile"):
            keyfile = arg
    if(not inputfile) or (not outputfile):
        print("Need an input file and an output file")
        sys.exit(2)

    # # Read in multiple files
    # files = myload.get_csv_files(inputfile)
    # print("Files: {}".format(files))

    # all_grades = []
    # assignments = []

    # for inputfile in files:
    # Read in the report from Matlab Grader
    with open(inputfile, 'r') as myfile:
        data = myload.parse_csv(myfile)
        
        # problems = organize.convert_csv_to_problems(data)
        # assignments += [organize.create_assignment_from_csv(data)]
        # students += [organize.read_csv_to_students(data)]

    # Cut out extra data (probably unnecessary)
    keep_columns = [1,5,6,8,10,11,14,16]
    prob_id_column_before_filter = 11
    prob_id_column_after_filter = 5

    filtered = organize.filter_info(data, keep_columns)
    indices = organize.build_split_indices(filtered,
                                           prob_id_column_after_filter)
    combined_problems = organize.combine_problems_by_student(organize.split_problems(filtered, indices))

    # Get a single assignment grade
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

    if not keyfile:
        print("Writing unsorted grades to " + outputfile)
        # print("reduced grades: {}".format(reduced_grades))

        canvas.write_grades("raw"+outputfile, graded)

    else:
        # Read the key for Canvas student names from Matlab grader emails
        print("Writing sorted grades to " + outputfile)
        with open(keyfile, 'r') as keyFile:
            keyData = myload.parse_csv(keyFile)

        fgraded = canvas.format_grades(graded, keyData)
        # check the key got all the grades we have
        unformated = canvas.list_unformated_grades(graded, keyData)
        if unformated:
            print("No key found for grades:")
            print(unformated)
        #print(fgraded)
        #canvas.write_grades(outputfile, fgraded)

        with open(outputfile, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ')
            for line in fgraded:
                writer.writerow(line)

    print("Finished")
    
if __name__ == "__main__":
    main(sys.argv[1:])
