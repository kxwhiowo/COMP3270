import sys, parse, grader
from heapq import heappush, heappop

def greedy_search(problem):
    start = problem['start']
    goal = problem['goal']
    frontier = []
    heappush(frontier, (problem[start][0], [start, ])) # add the initial heuristic of starting point
    # in frontier, node: (distance, [list of nodes in the path])
    path = []
    exploredList = list()
    while frontier:
        node = heappop(frontier)
        if node[-1][-1] == goal:
            path = node[-1]
            break
        if node[-1][-1] not in exploredList:
            exploredList.append(node[-1][-1])
            for child in problem[node[-1][-1]]:
                if type(child) == tuple:
                    newSeq = [i for i in node[-1]]
                    newSeq.append(child[0])
                    heappush(frontier, (problem[child[0]][0], newSeq))

    deli = " "
    solution = deli.join(exploredList) + '\n' + deli.join(path)
    return solution


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    grader.grade(problem_id, test_case_id, greedy_search, parse.read_graph_search_problem)
