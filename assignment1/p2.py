import sys, grader, parse, collections


def bfs_search(problem):
    # print(problem)
    path = []
    start = problem['start']
    goal = problem['goal']
    frontier = collections.deque([[start, ]])
    exploredList = list()
    while frontier:
        node = frontier.popleft()
        if node[-1] == goal:
            path = node
            break
        if node[-1] not in exploredList:
            # print('Explore: ' + node[-1])
            exploredList.append(node[-1])
            # print(problem[node[-1]])
            for child in problem[node[-1]]:
                if type(child) is tuple:
                    newNode = [i for i in node]
                    newNode.append(child[0])
                    frontier.append(newNode)
    deli = " "
    solution = deli.join(exploredList) + '\n' + deli.join(path)
    # solution = 'Ar B C D\nAr C G'
    return solution


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, bfs_search, parse.read_graph_search_problem)
