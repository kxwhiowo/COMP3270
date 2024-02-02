import sys, parse, grader


def checkAttack(position, problem):
    exploredSet = set()
    count = 0
    row, col = position[0], position[1]
    # check horizontally
    for hori in range(0, 8):
        if hori > col:
            if problem[row][hori] == 'q':
                count += 1
                exploredSet.add(((row, col), (row, hori)))
    # check diagonally
    for i in range(8):
        for j in range(8):
            if j <= col:
                continue
            elif ((i, j) != (row, col)) and ((i + j == row + col) or (i - j == row - col)):
                if problem[i][j] == 'q':
                    exploredSet.add(((row, col), (i, j)))
                    count += 1
    return count


def createNewMap(row, col, problem):  # !!!!!!!!
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
    return newProblem


def findQueens(problem):
    listOfQueens = []
    for row in range(8):
        for col in range(8):
            if problem[row][col] == 'q':
                listOfQueens.append((row, col))
    return listOfQueens


def checkingAttackWithNewMap(row, col, map):
    queenList = findQueens(map)
    attack = 0
    attack += checkAttack((row, col), map)
    for q in queenList:
        if q[1] != col:
            attack += checkAttack((q[0], q[1]), map)
    return attack


def getNumberListAndPosition(problem):
    cost = [[] for i in range(8)]
    for row in cost:
        for col in range(8):
            row.append(0)
    for row1 in range(8):
        for col1 in range(8):
            cost[row1][col1] = checkingAttackWithNewMap(row1, col1, createNewMap(row1, col1, problem))
    numList = [[] for i in range(8)]
    lowest = cost[0][0]
    position = (0, 0)
    for i in range(8):
        for j in range(8):
            numList[i].append(cost[i][j])
            if cost[i][j] < lowest:
                lowest = cost[i][j]
                position = (i, j)
    return position


def number_of_attacks(problem):
    cost = [[] for i in range(8)]
    for row in cost:
        for col in range(8):
            row.append(0)
    for row1 in range(8):
        for col1 in range(8):
            cost[row1][col1] = checkingAttackWithNewMap(row1, col1, createNewMap(row1, col1, problem))
    deli = " "
    deliChangeLine = "\n"
    solu = [[] for i in range(8)]
    for i in range(8):
        for j in range(8):
            ori = str(cost[i][j])
            if cost[i][j] < 10:
                ori = ' ' + ori
            solu[i].append(ori)
    solu1 = [deli.join(solu[j]) for j in range(8)]
    soluFinal = deliChangeLine.join(solu1)
    return soluFinal


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)
