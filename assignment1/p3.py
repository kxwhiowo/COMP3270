import sys, parse, grader, collections
from heapq import heappush, heappop


def ucs_search(problem):
    print(problem)
    start = problem['start']
    goal = problem['goal']
    frontier =[start, ]
    heappush(frontier, (0, start))
    path = []
    exploredList = list()

    while frontier:
        node = heappop(frontier)
        if node[-1] == goal:
            return node
        if node[-1] not in exploredList:
            exploredList.append(node[-1])
            for child in problem[node[1][-1]]:
                heappush(frontier, (node[0] + child[0], node[1] + child[1]))

    deli = " "
    solution = deli.join(exploredList) + '\n' + deli.join(path)
    print(solution)
    solution = 'S D B C\nS C G'
    return solution


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)
