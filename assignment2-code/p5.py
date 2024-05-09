import sys, parse
import time, os, copy, random, math

EAT_FOOD_SCORE = 10
PACMAN_EATEN_SCORE = -500
PACMAN_WIN_SCORE = 500
PACMAN_MOVING_SCORE = -1
GHOST_NUMBER = 0
FOOD_NUMBER = 0
GHOST_LIST = []
PLAYER_LIST = []
OK_LIST = ['P', '.', ' ']

def min_max_mulitple_ghosts(problem, k):
    global GHOST_NUMBER
    global FOOD_NUMBER
    global GHOST_LIST
    global PLAYER_LIST
    depth = k
    list_of_game = problem.split('\n')
    seed = int(list_of_game[0].split()[-1])
    world = list_of_game[1:]
    player_now = 'P'
    counter = 0
    score = 0
    ghost_list = sorted(check_ghost_list(world))
    counter_for_player = 0
    ghost_list.append('P')
    player_list = sorted(ghost_list)
    ghost_list = sorted(check_ghost_list(world))
    
    GHOST_NUMBER = len(ghost_list)
    FOOD_NUMBER = check_food_number(world)
    GHOST_LIST = ghost_list
    PLAYER_LIST = player_list
    
    is_overlap = [False for i in ghost_list]
    solution = 'seed: ' + str(seed) + '\n0\n'
    for i in world:
        solution += i + '\n'
        
    while True:
        position = check_player_position(player_now, world)
        if player_now == 'P':
            available_directions = check_available(world, position)
            direction = choose_better_direction_for_player(world, available_directions, position, ghost_list, depth)
        else:
            available_directions = check_available_for_ghost(world, position, player_now)
            print(player_now, 'has', available_directions)
            direction = choose_better_direction_for_ghost(world, available_directions, position, player_now, depth)
        
        score_new, world, is_overlap = make_move(player_now, direction, world, position, is_overlap, ghost_list)
        print("\n".join(world))
        print()
        
        score += score_new
        counter += 1
        status, winner = check_end_of_game(world, is_overlap)
        if status:
            if winner == 'Pacman':
                score += PACMAN_WIN_SCORE
            solution += transfer_map_to_solution(world, score, counter, player_now, direction)
            solution += 'WIN: ' + winner
            break
        else:
            if direction == None:
                direction = ""
            solution += transfer_map_to_solution(world, score, counter, player_now, direction)
            counter_for_player += 1
            if counter_for_player == len(player_list):
                counter_for_player = 0
            player_now = player_list[counter_for_player]
    with open('1.txt', 'wt') as f:
        print(solution, file=f)
    return solution, winner
# check the food number in the map.
def check_food_number(map):
    food_number = 0
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == '.':
                food_number += 1
    return food_number
# check the ghost in the map, returns a list of existing ghosts.
def check_ghost_list(map):

    ghost_list = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] != 'P' and map[i][j] != '.' and map[i][j] != '%' and map[i][j] != ' ':
                ghost_list.append(map[i][j])
    return ghost_list

# check available directions for ghost.
def check_available_for_ghost(map, position, ghost_list):
    directions = []
    
    if map[position[0]][position[1] + 1] in OK_LIST:
        directions.append('E')
    if map[position[0] - 1][position[1]] in OK_LIST:
        directions.append('N')
    if map[position[0] + 1][position[1]] in OK_LIST:
        directions.append('S')
    if map[position[0]][position[1] - 1] in OK_LIST:
        directions.append('W')
    return tuple(directions)
# return a optimized direction for ghost.
def choose_better_direction_for_ghost(map, available_directions, position, player, depth):
    if len(available_directions) == 0:
        return None
    direction = minimax(available_directions, map, position, depth, player)
    print(direction)
    return direction

# return a optimized direction for player.
def choose_better_direction_for_player(map, available_directions, player_position, ghost_list, depth):
    return minimax(available_directions, map, player_position, depth, 'P')

# minimax function, return a target direction
def minimax(available_diretions, map, position, depth, player):
    #print('minimax: ', position, player)
    direction_target = None
    overlap = [False for _ in range(len(GHOST_LIST))]
    print(available_diretions)
    if player == 'P':    
        max_value = float("-inf")
        for direction in available_diretions:
            map_future, overlap_new = minimax_make_move(map, position, direction, overlap)
            value_future = value_calculator(map_future, depth, 0, overlap_new)
            print(direction, value_future, end="")
            if value_future > max_value:
                max_value = value_future
                direction_target = direction
    else:
        player_num = GHOST_LIST.index(player)
        min_value = 1000000000
        for direction in available_diretions:
            map_future, overlap_new = minimax_make_move(map, position, direction, overlap)
            value_future = value_calculator(map_future, depth, player_num, overlap_new)
            if value_future < min_value:
                min_value = value_future
                direction_target = direction
    # print(direction_target)
    return direction_target
# get the value of minimax.
def value_calculator(map, depth, player_number, overlap):
    is_terminated, terminate_value = check_terminate_state(map, overlap, player_number)
    if is_terminated or depth == 0:
        return terminate_value
    if player_number == 0:
        return max_value(map, depth, 0, overlap)
    else:
        return min_value(map, depth, player_number, overlap)
# max value in minimax
def max_value(map, depth, player_number, overlap):
    value = -100000
    player = PLAYER_LIST[player_number]
    player_position = check_player_position(player, map)
    directions = check_available(map, player_position)
    for d in directions:
        player_position = check_player_position(player, map)
        new_map, overlap_new = minimax_make_move(map, player_position, d, overlap)
        value = max(value, value_calculator(new_map, depth - 1, 1, overlap_new))
    return value - 2
# min value in minimax
def min_value(map, depth, player_number, overlap):
    value = 100000
    player = PLAYER_LIST[player_number]
    player_position = check_player_position(player, map)
    directions = check_available(map, player_position)
    for d in directions:

        player_position = check_player_position(player, map)
        new_map, overlap_new = minimax_make_move(map, player_position, d, overlap)
        if player_number == len(PLAYER_LIST) - 1:
            value = min(value, value_calculator(new_map, depth - 1, 0, overlap_new))
        else:
            value = min(value, value_calculator(new_map, depth - 1, player_number + 1, overlap_new))
    return value - 2
# return a winning or losing score, or return a evaluation score for the map now.
def check_terminate_state(map, overlap, player_number):
    counter_for_player_P = 0
    counter_for_food = 0
    for i in map:
        for j in range(len(i)):
            if i[j] == 'P':
               counter_for_player_P += 1
    for k in map:
        for h in range(len(k)):
            if k[h] == '.':
                counter_for_food += 1
    if counter_for_food == 0 and True not in overlap and counter_for_player_P == 1:
        return True, 10000
    if counter_for_player_P == 0:
        return True, -10000
    return False, evaluate_func(map, player_number)
# evaluate the map's score. 
def evaluate_func(map, player_number):
    closest_distance = []
    player_position = check_player_position('P', map)
    if player_position == None:
        return -10000
    food_position = check_nearest_food_position(map, player_position)
    positions_ghost = check_nearest_ghost_position(map, (player_position[0] - 1, player_position[1]), GHOST_LIST)
    closest_ = calculate_closest_score(player_position, positions_ghost,food_position, player_number)
    return closest_

# to build a new map especially for minimax
def minimax_make_move(map_, position, direction, overlap):
    map = map_.copy()
    ghost_list = GHOST_LIST
    x, y = position[0], position[1]
    player = map[x][y]
    
    
    if player == 'P':
        x_next, y_next = choose_next_position(position, direction)
        if map[x_next][y_next] in ghost_list:
            map[x] = map[x][:y] + ' ' + map[x][y + 1:]
            return map, overlap # need to check the situation when P is gone after. 
        map[x_next] = map[x_next][:y_next] + player + map[x_next][y_next + 1:]
        map[x] = map[x][:y] + ' ' + map[x][y + 1:]
        return map, overlap
    if player in GHOST_LIST:
        if direction == None or player == None:
            return map, overlap
        ghost = None
        for g in range(len(ghost_list)):
            if GHOST_LIST[g] == player:
                ghost = g
        x_next, y_next = choose_next_position(position, direction)
        if map[x_next][y_next] in GHOST_LIST:
            return map, overlap
        if overlap[ghost]:
            map[x] = map[x][:y] + '.' + map[x][y + 1:]
            overlap[ghost] = False
        else:
            map[x] = map[x][:y] + ' ' + map[x][y + 1:]
        if map[x_next][y_next] == '.':
            overlap[ghost] = True
        map[x_next] = map[x_next][:y_next] + player + map[x_next][y_next + 1:]
        return map, overlap
    # situation that player is ' '
    pass

# check available directions for a player.
def check_available(map, position):
    directions = []
    if map[position[0]][position[1] + 1] != '%':
        directions.append('E')
    if map[position[0] - 1][position[1]] != '%':
        directions.append('N')
    if map[position[0] + 1][position[1]] != '%':
        directions.append('S')
    if map[position[0]][position[1] - 1] != '%':
        directions.append('W')
    return tuple(directions)
# check the distance of nearest food.
def check_nearest_food_position(map, player_position):
    food_positions = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == '.':
                food_positions.append((i, j))
    value = 100000
    if len(food_positions) == 0:
        return 0
    for points in food_positions:
        dist = abs(points[0] - player_position[0]) + abs(points[1] - player_position[1])
        if dist < value:
            value = dist

    return value
# check nearest ghost position
def check_nearest_ghost_position(map, player_position, ghost_list):
    ghost_positions = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] in ghost_list:
                ghost_positions.append((i, j))
    sorted_points = sorted(ghost_positions, key=lambda p: math.dist(p, player_position), reverse=True)
    return sorted_points
# compute the score for a terminate situation.
def calculate_closest_score(player_position, ghost_position_list, food_distance, player_number):
    player_x, player_y = player_position[0], player_position[1]
    score = 0
    score = 4 / food_distance
    num_of_ghosts = len(ghost_position_list)
    dist = (abs(player_x - ghost_position_list[0][0]) + abs(player_y - ghost_position_list[0][1]))
    if dist == 0:
        score -= 10000
    else:
        score += 2 / dist
    if num_of_ghosts == 1:
        return score
    weight = 1
    return score + 0.5 / (abs(player_x - ghost_position_list[1][0]) + abs(player_y - ghost_position_list[1][1]))
# check player's position
def check_player_position(player, map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == player:
                return (i, j)
    return None  
# make move for the final map.
def make_move(player, direction, map, position, overlap, ghost_list):
    global FOOD_NUMBER
    score = 0
    ghost_possible_list = GHOST_LIST
    x, y = position[0], position[1]
    if player == 'P':
        x_next, y_next = choose_next_position(position, direction)
        if map[x_next][y_next] == '.':
            FOOD_NUMBER -= 1
            score += EAT_FOOD_SCORE
        elif map[x_next][y_next] in ghost_list:
            map[x] = map[x][:y] + ' ' + map[x][y + 1:]
            return score + PACMAN_EATEN_SCORE + PACMAN_MOVING_SCORE, map, overlap
        map[x_next] = map[x_next][:y_next] + player + map[x_next][y_next + 1:]
        map[x] = map[x][:y] + ' ' + map[x][y + 1:]
        return score + PACMAN_MOVING_SCORE, map, overlap
    if player != 'P':
        
        if direction == None:
            return score, map, overlap
        ghost = None
        for g in range(len(ghost_list)):
            if ghost_list[g] == player:
                ghost = g
        print("ghost: " , player, ' moving')
        x_next, y_next = choose_next_position(position, direction)
        print(x_next, y_next)
        if map[x_next][y_next] == 'P':
            score += PACMAN_EATEN_SCORE
        if map[x_next][y_next] in ghost_possible_list:
            return score, map, overlap
        if overlap[ghost]:
            map[x] = map[x][:y] + '.' + map[x][y + 1:]
            overlap[ghost] = False
        else:
            map[x] = map[x][:y] + ' ' + map[x][y + 1:]
        if map[x_next][y_next] == '.':
            overlap[ghost] = True
        map[x_next] = map[x_next][:y_next] + player + map[x_next][y_next + 1:]
        return score, map, overlap

    return 0 
# take direction and an original position, return the updated position
def choose_next_position(position, direction):
    x = position[0]
    y = position[1]
    if direction == 'E':
        return (x, y + 1)
    elif direction == 'N':
        return (x - 1, y)
    elif direction == 'S':
        return (x + 1, y)
    elif direction == 'W':
        return (x, y - 1)
# check whether the game ends 
def check_end_of_game(map, overlap):
    c = overlap.count(True)
    counter_for_player_P = 0
    for i in map:
        for j in range(len(i)):
            if i[j] == 'P':
               counter_for_player_P += 1
    if c == 0 and counter_for_player_P == 1 and FOOD_NUMBER == 0:
        return True, 'Pacman'
    elif counter_for_player_P != 1:
        return True, 'Ghost'
    else:
        if counter_for_player_P == 1:
            return False, 'Pacman' 
        else:
            return False, 'Ghost'

# transfer the map and other stuffs to a solution string.
def transfer_map_to_solution(map, score, count, player, direction):
    solution = str(count) + ': ' + player + ' moving ' + direction + '\n'
    for i in range(len(map)):
        solution += map[i] + '\n'
    solution += 'score: ' + str(score) + '\n'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 5
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:',test_case_id)
    print('k:',k)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = min_max_mulitple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)