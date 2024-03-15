import sys, grader, parse, random


EAT_FOOD_SCORE = 10
PACMAN_EATEN_SCORE = -500
PACMAN_WIN_SCORE = 500
PACMAN_MOVING_SCORE = -1


def random_play_multiple_ghosts(problem):
    list_of_game = problem.split('\n')
    seed = int(list_of_game[0].split()[-1])
    world = list_of_game[1:]
    player_now = 'P'
    counter = 0
    score = 0
    random.seed(seed, version=1)
    ghost_list = sorted(check_ghost_list(world))
    counter_for_player = 0
    ghost_list.append('P')
    player_list = sorted(ghost_list)
    ghost_list = sorted(check_ghost_list(world))
    solution = 'seed: ' + str(seed) + '\n0\n'
    is_overlap = [False for i in ghost_list]
    for i in world:
        if len(i) == 16:
            i = i[:-1]
        solution += i + '\n'
        
    while True:
        position = check_player_position(player_now, world)
        if player_now == 'P':
            available_directions = check_available(world, position)
        else:
            available_directions = check_available_for_ghost(world, position, ghost_list)
        if len(available_directions) == 0:
            direction = None
        else:
            direction = random.choice(available_directions)
        score_new, world, is_overlap = make_move(player_now, direction, world, position, is_overlap, ghost_list)
        score += score_new
        counter += 1
        status, winner = check_end_of_game(world, is_overlap, ghost_list)
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
    return solution

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
    
    
def check_end_of_game(map, overlap, ghost_list):
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
            elif i[j] in ghost_list:
                counter_for_player_W += 1
            elif i[j] == '.':
                counter_for_food += 1
    if counter_for_food == 0 and exist_overlap == False:
        return True, 'Pacman'
    elif (counter_for_player_W + counter_for_player_P) != len(ghost_list) + 1:
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
    problem_id = 3
    grader.grade(problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem)