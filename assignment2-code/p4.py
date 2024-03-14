import math
import sys, parse
import time, os, copy, random

EAT_FOOD_SCORE = 10
PACMAN_EATEN_SCORE = -500
PACMAN_WIN_SCORE = 500
PACMAN_MOVING_SCORE = -1

def better_play_mulitple_ghosts(problem):
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
    is_overlap = [False for i in ghost_list]
    solution = 'seed: ' + str(seed) + '\n0\n'
    for i in world:
        solution += i + '\n'
        
    while True:
        position = check_player_position(player_now, world)
        if player_now == 'P':
            available_directions = check_available(world, position)
            direction = choose_better_direction_for_player(world, available_directions, position, ghost_list)
        else:
            available_directions = check_available_for_ghost(world, position, ghost_list)
            direction = choose_direction_for_ghost(world, available_directions)
        
        score_new, world, is_overlap = make_move(player_now, direction, world, position, is_overlap, ghost_list)
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

def check_ghost_list(map):

    ghost_list = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] != 'P' and map[i][j] != '.' and map[i][j] != '%' and map[i][j] != ' ':
                ghost_list.append(map[i][j])
    return ghost_list
    
def check_available_for_ghost(map, position, ghost_list):
    directions = []
    if map[position[0]][position[1] + 1] != '%' and map[position[0]][position[1] + 1] not in ghost_list:
        directions.append('E')
    if map[position[0] - 1][position[1]] != '%' and map[position[0] - 1][position[1]] not in ghost_list:
        directions.append('N')
    if map[position[0] + 1][position[1]] != '%' and map[position[0] + 1][position[1]] not in ghost_list:
        directions.append('S')
    if map[position[0]][position[1] - 1] != '%' and map[position[0]][position[1] - 1] not in ghost_list:
        directions.append('W')
    return tuple(directions)

def choose_direction_for_ghost(map, available_directions):
    if len(available_directions) == 0:
        return None
    direction = random.choice(available_directions)
    return direction

def choose_better_direction_for_player(map, available_directions, player_position, ghost_list):
    closest_distance = []
    for d in available_directions:
        if d == 'N':
            closest = len(map[0]) - 2
            for i in range(player_position[0] - 1, 0, -1):
                if map[i][player_position[1]] == '%':
                    break
                elif map[i][player_position[1]] == '.':
                    closest = player_position[0] - i
            positions_ghost = check_nearest_ghost_position(map, (player_position[0] - 1, player_position[1]), ghost_list)
            closest_ = calculate_closest_score((player_position[0] - 1, player_position[1]), positions_ghost, closest)
            closest_distance.append((closest_, 'N'))
        if d == 'S':
            closest = len(map[0]) - 2
            for i in range(player_position[0] + 1, len(map)):
                if map[i][player_position[1]] == '%':
                    break
                elif map[i][player_position[1]] == '.':
                    closest = - player_position[0] + i
            positions_ghost = check_nearest_ghost_position(map, (player_position[0], player_position[1] - 1), ghost_list)
            closest_ = calculate_closest_score((player_position[0], player_position[1] - 1), positions_ghost, closest)
            closest_distance.append((closest_, 'S'))
        if d == 'E':
            closest = len(map[0]) - 2
            for i in range(player_position[1] + 1, len(map[0])):
                if map[player_position[0]][i] == '%':
                    break
                if map[player_position[0]][i] == '.':
                    closest = - player_position[1] + i
            positions_ghost = check_nearest_ghost_position(map, (player_position[0], player_position[1] + 1), ghost_list)
            closest_ = calculate_closest_score((player_position[0], player_position[1] + 1), positions_ghost, closest)
            closest_distance.append((closest_, 'E'))
        if d == 'W':
            closest = len(map[0]) - 2
            for i in range(player_position[1] - 1, 0, -1):
                if map[player_position[0]][i] == '%':
                    break
                elif map[player_position[0]][i] == '.':
                    closest = player_position[1] - i
            positions_ghost = check_nearest_ghost_position(map, (player_position[0], player_position[1] - 1), ghost_list)
            closest_ = calculate_closest_score((player_position[0], player_position[1] - 1), positions_ghost, closest)
            closest_distance.append((closest_, 'W'))
    distance = max([i[0] for i in closest_distance])
    
    better_direction = 'A'
    for i in closest_distance:
        if i[0] == distance:
            better_direction = i[1]
    return better_direction

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
def check_nearest_ghost_position(map, player_position, ghost_list):
    ghost_positions = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] in ghost_list:
                ghost_positions.append((i, j))
    sorted_points = sorted(ghost_positions, key=lambda p: math.dist(p, player_position), reverse=True)
    return sorted_points
def calculate_closest_score(player_position, ghost_position_list, food_distance):
    player_x, player_y = player_position[0], player_position[1]
    score = - food_distance
    weight = 2
    num_of_ghosts = len(ghost_position_list)
    for _ in range(len(ghost_position_list)):
        dist = (abs(player_x - ghost_position_list[_][0]) + abs(player_y - ghost_position_list[_][1]))
        if dist == 0:
            score -= 10000
        else:
            score += weight * num_of_ghosts * 1/dist
        weight -= 0.5
    return score

def check_player_position(player, map):
    position = ()
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == player:
                return (i, j)
    return position    
def make_move(player, direction, map, position, overlap, ghost_list):
    score = 0
    ghost_possible_list = ['W', 'X', 'Y', 'Z']
    x, y = position[0], position[1]
    if player == 'P':
        x_next, y_next = choose_next_position(position, direction)
        if map[x_next][y_next] == '.':
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
        x_next, y_next = choose_next_position(position, direction)
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
    
    
def check_end_of_game(map, overlap):
    counter_for_player_P = 0
    counter_for_player_W = 0
    counter_for_food = 0
    exist_overlap = False
    if True in overlap:
        exist_overlap = True
    for i in map:
        for j in range(len(i)):
            if i[j] == 'P':
               counter_for_player_P += 1
            elif i[j] == 'W':
                counter_for_player_W += 1
            elif i[j] == '.':
                counter_for_food += 1
    if counter_for_food == 0 and exist_overlap == False:
        return True, 'Pacman'
    elif (counter_for_player_W + counter_for_player_P) != 2:
        return True, 'Ghost'
    else:
        if counter_for_player_P == 1:
            return False, 'Pacman' 
        elif counter_for_player_W == 1:
            return False, 'Ghost'

def transfer_map_to_solution(map, score, count, player, direction):
    solution = str(count) + ': ' + player + ' moving ' + direction + '\n'
    for i in range(len(map)):
        solution += map[i] + '\n'
    solution += 'score: ' + str(score) + '\n'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 4
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_mulitple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)