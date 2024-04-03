import sys, grader, parse, random
from collections import Counter

PLAYER_POSITION = []
START_POSITION = []
WALL_POSITION = []
LIVING_REWARD = 0
NOISE = 0
DIRECTIONS = ['N', 'E', 'S', 'W']
D = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
SPACE = ""
LEN_SPACE = 0
LINE = "-------------------------------------------- \n"
GRID_HEIGHT = 0
GRID_WIDTH = 0


def play_episode(problem):
    global PLAYER_POSITION, START_POSITION
    global SPACE, LEN_SPACE
    global LIVING_REWARD, NOISE
    global GRID_WIDTH, GRID_HEIGHT, WALL_POSITION

    problem_ = problem.split("\n")
    seed_ = int(problem_[0][6:])
    NOISE = float(problem_[1][7:])
    LIVING_REWARD = float(problem_[2][14:])
    if seed_ != -1:
        random.seed(seed_, version=1)

    c_score = 0.0 # cumulative score
    reward = 0 # the reward taking each step
    
    experience = ''

    grid_, policy_ = problem_.index("grid:"), problem_.index("policy:")
    grid = problem_[grid_ + 1 : policy_]
    policy= problem_[policy_ + 1:]

    # the space before each element in the grid.
    for i in grid[0]:
        if i != " ":
            index_f = grid[0].index(i)
            break
    SPACE = grid[0][:index_f]
    

    for i in range(len(grid)):
        grid[i] = grid[i].strip().split()
    for i in range(len(policy)):
        policy[i] = policy[i].strip().split()
    GRID_HEIGHT, GRID_WIDTH = len(grid), len(grid[0])
    LEN_SPACE = len(SPACE) + len(str(grid[0][0]))
    # print(LEN_SPACE)

    # Find the position of each state
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                START_POSITION = [i, j]
                PLAYER_POSITION = [i, j]
            if grid[i][j] == '#':
                WALL_POSITION.append((i, j))
    
    # initialize the Start state
    experience += "Start state:\n"
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if PLAYER_POSITION == [i, j]:
                experience = experience + " " * (LEN_SPACE - 1) + 'P'
                continue
            experience = experience + " " * (LEN_SPACE - len(str(grid[i][j]))) + grid[i][j]
        experience += '\n'
    experience += f"Cumulative reward sum: {c_score}\n"
    experience += LINE

    while True:
        intend_direction = policy[PLAYER_POSITION[0]][PLAYER_POSITION[1]]
        if intend_direction == 'exit':
            real_direction = "exit"
        else:
            real_direction = random.choices(population=D[intend_direction], weights=[1 - NOISE*2, NOISE, NOISE])[0]
        update_position(translate_move(real_direction))
        reward = get_reward(real_direction, grid)
        c_score = round(c_score + reward, 2)
        experience += render(grid, intend_direction, real_direction, reward, c_score)
        if real_direction == 'exit':
            break
    WALL_POSITION = []
    return experience[:-1]

# translate the moving to positions
def translate_move(direction):
    if direction == 'N':
        return (-1, 0)
    elif direction == 'S':
        return (1, 0)
    elif direction == 'E':
        return (0, 1)
    elif direction == 'W':
        return (0, -1)
    elif direction == 'exit':
        return 'exit'

# Choose the real direction
def intend_to_real(random, intend_direction):
    if intend_direction == 'exit':
        return "exit"
    return random.choices(population=D[intend_direction], weights=[1 - NOISE*2, NOISE, NOISE])[0]

# update the position of player
# if the player touch a wall, it will not 
def update_position(movement):
    global PLAYER_POSITION
    if movement == 'exit':
        return
    
    h = PLAYER_POSITION[0] + movement[0]
    w = PLAYER_POSITION[1] + movement[1]
    # when it exceed the length
    if h < 0:
        h = 0
    elif h >= GRID_HEIGHT:
        h = GRID_HEIGHT - 1
    if w < 0:
        w = 0
    elif w >= GRID_WIDTH:
        w = GRID_WIDTH - 1
    # when it touch the wall
    if (h, w) in WALL_POSITION:
        h, w = PLAYER_POSITION[0], PLAYER_POSITION[1]
    PLAYER_POSITION = [h, w]

# get the reward of each step
def get_reward(direction, grid):
    if direction != "exit":
        return LIVING_REWARD
    else:
        return float(grid[PLAYER_POSITION[0]][PLAYER_POSITION[1]])

# only for rendering the map in each step.
def render(grid, intend_action, real_action, reward, c_score):
    sign = False
    if PLAYER_POSITION == START_POSITION:
        sign = True
    solution = ""
    solution = f"Taking action: {real_action} (intended: {intend_action})" + '\n'
    solution = solution + f"Reward received: {reward}" + '\n'
    solution = solution + "New state:\n"

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S' and sign:
                J = 'P'
                solution = solution + " " * (LEN_SPACE - 1) + J
                continue
            if PLAYER_POSITION == [i, j] and real_action != "exit":
                solution = solution + " " * (LEN_SPACE - 1) + 'P'
                continue
            solution = solution + " " * (LEN_SPACE - len(str(grid[i][j]))) + grid[i][j]
        solution += '\n'

    solution = solution + f"Cumulative reward sum: {c_score}" + '\n'
    if real_action != 'exit':
        solution += LINE
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)

