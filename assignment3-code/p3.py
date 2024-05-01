import sys, grader, parse

START_POSITION = []
WALL_POSITION = []
VALUE_POSITION = []
LIVING_REWARD = 0
NOISE = 0
DISCOUNT = 0
ITERATION = 0
DIRECTIONS = ['N', 'E', 'S', 'W']
D = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
NON_NUM_ELEMENT = ['S', '_']
ALL_NON_NUM = ['S', '_', '#']
SPACE = ""
GRID_HEIGHT = 0
GRID_WIDTH = 0

def value_iteration(problem):
    global START_POSITION
    global LIVING_REWARD, NOISE, DISCOUNT, ITERATION
    global GRID_WIDTH, GRID_HEIGHT, WALL_POSITION

    problem_ = problem.split("\n")

    DISCOUNT = float(problem_[0][10:])
    NOISE = float(problem_[1][7:])
    LIVING_REWARD = float(problem_[2][14:])
    ITERATION = int(problem_[3][12:])
    
    experience = ''

    grid_ = problem_.index("grid:")
    grid = problem_[grid_ + 1 :]


    for i in range(len(grid)):
        grid[i] = grid[i].strip().split()
    GRID_HEIGHT, GRID_WIDTH = len(grid), len(grid[0])

    policy = [[] for _ in range(GRID_HEIGHT)]

    # Find the position of each state
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                START_POSITION = [i, j]
            if grid[i][j] == '#':
                WALL_POSITION.append((i, j))
            if grid[i][j] not in ALL_NON_NUM:
                VALUE_POSITION.append((i, j))

    # initialize the Start state
    experience += "V_k=0\n"
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '#':
                experience += "| ##### |"
            else:
                experience += '|{:7.2f}|'.format(0.00)
        experience += '\n'
    
    # initialize the 1st state
    experience += "V_k=1\n"
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] not in ALL_NON_NUM:
                experience += '|{:7.2f}|'.format(float(grid[i][j]))
            elif grid[i][j] == '#':
                experience += "| ##### |"
            else:
                experience += '|{:7.2f}|'.format(LIVING_REWARD)
        experience += '\n'
    
    # change the grid to the 1st value
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] not in NON_NUM_ELEMENT and grid[i][j] != '#':
                grid[i][j] = float(grid[i][j])
            elif grid[i][j] == '#':
                grid[i][j] = '#'
            else:
                grid[i][j] = LIVING_REWARD

    # initialize the policy grid
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if (i, j) in VALUE_POSITION:
                policy[i].append('x')
                continue
            if (i, j) in WALL_POSITION:
                policy[i].append('#')
                continue
            else:
                policy[i].append('N')
    
    experience += 'pi_k=1\n'
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH): 
            experience += f'| {policy[i][j]} |'
        experience += '\n'
    
    # update the value new grid 
    for _ in range(2, ITERATION):
        new_grid = [[float('-inf') for w in range(len(grid[0]))] for q in range(len(grid))]
        # update the values in the new grid
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '#':
                    new_grid[i][j] = '#'
                    continue
                if (i, j) in VALUE_POSITION:
                    new_grid[i][j] = grid[i][j]
                    continue
                max_direction = 'N'
                for di in DIRECTIONS:
                    noise_directions = D[di]
                    new_value = 0.00
                    for d in noise_directions:
                        position = get_new_position(translate_move(d), (i, j))
                        v_prime = grid[position[0]][position[1]]
                        if d == di:
                            new_value += (1 - 2 * NOISE) * (LIVING_REWARD + DISCOUNT * v_prime)
                        else:
                            new_value += NOISE * (LIVING_REWARD + DISCOUNT * v_prime)
                    if new_value > new_grid[i][j]:
                        new_grid[i][j] = new_value
                        max_direction = di
                policy[i][j] = max_direction
        experience += render(new_grid, policy, _)
        grid = new_grid
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

# update the position of player
# intend_position: the moving parameters, position: the position in the grid.
# if the player touch a wall, it will not change its position
# returns a position after moving
def get_new_position(intend_direction, position):
    if intend_direction == 'exit':
        return
    
    h = position[0] + intend_direction[0]
    w = position[1] + intend_direction[1]

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
        h, w = position[0], position[1]
    return (h, w)


# only for rendering the map in each step.
def render(grid, policy, k):
    solution = ""
    
    solution += f'V_k={k}\n'
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '#':
                solution += "| ##### |"
            else:
                solution += '|{:7.2f}|'.format(grid[i][j])
        solution += '\n'
    
    
    solution += f'pi_k={k}\n'
    for i in range(len(policy)):
        for j in range(len(policy[0])):
            solution += f"| {policy[i][j]} |"
        solution += '\n'
    return solution



if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)