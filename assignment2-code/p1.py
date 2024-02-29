import sys, random, grader, parse

def random_play_single_ghost(problem):
    list_of_game = problem.split('\n')
    seed = list_of_game[0].split()[-1]
    world = list_of_game[1:]
    random.seed(seed, version=1)
    random.choice(('N', 'S', 'E', 'W'))

    while True:
        
        
        
        
        break


    solution = ''
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)