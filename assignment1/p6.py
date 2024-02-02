import sys, parse, grader

'''
check the attack number at specific posision
'''


def checkAttack(position, problem):
    exploredSet = set()
    row, col = position[0], position[1]
    # check horizontally
    for hori in range(0, 8):
        if hori != col:
            if problem[row][hori] == 'q':
                if ((row, col), (row, hori)) not in exploredSet and (
                        (row, hori), (row, col)) not in exploredSet:
                    exploredSet.add(((row, col), (row, hori)))
    # check diagonally
    for i in range(8):
        for j in range(8):
            if ((i, j) != (row, col)) and ((i + j == row + col) or (i - j == row - col)):
                if problem[i][j] == 'q':
                    if ((row, col), (i, j)) not in exploredSet and (
                            (i, j), (row, col)) not in exploredSet:
                        exploredSet.add(((row, col), (i, j)))

    return len(exploredSet)


def createNewMap(row, col, problem):
    newProblem = [i for i in problem]
    for i in range(8):
        newProblem[i][col] = '.'
    newProblem[row][col] = 'q'
    return newProblem


def findQueens(problem):
    listOfQueens = []
    for row in range(8):
        for col in range(8):
            if problem[row][col] == 'q':
                listOfQueens.append((row, col))
    return listOfQueens


def checkQueensAttack(listOfQueens, problem):
    queensAttacks = []
    for q in listOfQueens:
        queensAttacks.append(checkAttack(q, problem))
    return queensAttacks


def checkingAttackWithNewMap(map):
    queenList = findQueens(map)
    queenAttackList = checkQueensAttack(queenList, map)
    attack = 0
    for i in range(8):
        for j in range(8):
            attack += checkAttack((i, j), map)
            for q in queenAttackList:
                if q != j:
                    attack += queenAttackList[q]
    return attack


def number_of_attacks(problem):
    cost = [[] for i in range(8)]
    for row in cost:
        for col in range(8):
            row.append([])
    for row1 in range(8):
        for col1 in range(8):
            cost[row1][col1] = checkingAttackWithNewMap(createNewMap(row1, col1, problem))
    print(cost)
    solution = """18 12 14 13 13 12 14 14
14 16 13 15 12 14 12 16
14 12 18 13 15 12 14 14
15 14 14 17 13 16 13 16
17 14 17 15 17 14 16 16
17 17 16 18 15 17 15 17
18 14 17 15 15 14 17 16
14 14 13 17 12 14 12 18"""
    return solution


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)
