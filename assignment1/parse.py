import os, sys


def read_graph_search_problem(file_path):
    # Your p1 code here
    problem = {}
    with open(file_path) as f:
        lines = f.readlines()
        start = lines[0].split()[1]
        goal = lines[1].split()[1]
        problem['start'] = start
        problem['goal'] = goal
        for i in range(2, len(lines)):
            if len(lines[i].split()) < 3:
                problem[lines[i].split()[0]] = [float(lines[i].split()[1]), ]
            else:
                problem[lines[i].split()[0]].append((lines[i].split()[1],
                                                     float(lines[i].split()[2])))



    return problem


def read_8queens_search_problem(file_path):
    # Your p6 code here
    problem = ''
    return problem


if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases', 'p' + problem_id, test_case_id + '.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases', 'p' + problem_id, test_case_id + '.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')
