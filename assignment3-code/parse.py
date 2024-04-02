def read_grid_mdp_problem_p1(file_path):
    problem = ''
    with open(file_path) as f:
        lines = f.readlines()
        for i in lines:
            problem += i
    return problem

def read_grid_mdp_problem_p2(file_path):
    problem = ''
    with open(file_path) as f:
        lines = f.readlines()
        for i in lines:
            problem += i
    return problem

def read_grid_mdp_problem_p3(file_path):
    problem = ''
    with open(file_path) as f:
        lines = f.readlines()
        for i in lines:
            problem += i
    return problem

#print(read_grid_mdp_problem_p1("test_cases/p1/1.prob"))