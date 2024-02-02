import sys, parse, grader, p6


def better_board(problem):
    position = p6.getNumberListAndPosition(problem)
    row, col = position[0], position[1]
    newProblem = [[] for i in range(8)]
    for row1 in newProblem:
        for col1 in range(8):
            row1.append([])
    for a in range(8):
        for b in range(8):
            newProblem[a][b] = problem[a][b]
    for i in range(8):
        newProblem[i][col] = '.'
    newProblem[row][col] = 'q'

    deli = " "
    deliChangeLine = "\n"
    solu = [[] for i in range(8)]
    for i in range(8):
        for j in range(8):
            ori = str(newProblem[i][j])
            solu[i].append(ori)
    solu1 = [deli.join(solu[j]) for j in range(8)]
    soluFinal = deliChangeLine.join(solu1)
    print(soluFinal)
    return soluFinal


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)
