import sys, random, grader, parse

EAT_FOOD_SCORE = 10
PACMAN_EATEN_SCORE = -500
PACMAN_WIN_SCORE = 500
PACMAN_MOVING_SCORE = -1

def random_play_single_ghost(problem):
    list_of_game = problem.split('\n')
    seed = int(list_of_game[0].split()[-1])
    world = list_of_game[1:]
    player_now = 'P'
    counter = 0
    score = 0
    is_overlap = False
    random.seed(seed, version=1)
    solution = 'seed: ' + str(seed) + '\n0\n'
    for i in world:
        solution += i + '\n'

    while True:
        position = check_player_position(player_now, world)
        available_directions = check_available(world, position)
        direction = random.choice(available_directions)
        score_new, world, is_overlap = make_move(player_now, direction, world, position, is_overlap)
        score += score_new
        counter += 1
        status, winner = check_end_of_game(world)
        if status:
            if winner == 'Pacman':
                score += PACMAN_WIN_SCORE
            
            solution += transfer_map_to_solution(world, score, counter, player_now, direction)
            solution += 'WIN: ' + winner
            break
        else:
            solution += transfer_map_to_solution(world, score, counter, player_now, direction)
            if player_now == 'P':
                player_now = 'W'
            else:
                player_now = 'P'
    with open('1.txt', 'wt') as f:
        print(solution, file=f)
    print(world)
    return solution

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
    print(i, j)
    return position    

def make_move(player, direction, map, position, overlap):
    score = 0
    x, y = position[0], position[1]
    if player == 'P':
        x_next, y_next = choose_next_position(position, direction)
        if map[x_next][y_next] == '.':
            score += EAT_FOOD_SCORE
        elif map[x_next][y_next] == 'W':
            map[x] = map[x][:y] + ' ' + map[x][y + 1:]
            # for i in map:
            #     if i[-1] == ' ' or i[-1] == '\n':
            #         i = i[:-1]
            return score + PACMAN_EATEN_SCORE + PACMAN_MOVING_SCORE, map, overlap
        map[x_next] = map[x_next][:y_next] + player + map[x_next][y_next + 1:]
        map[x] = map[x][:y] + ' ' + map[x][y + 1:]
        #print(map)
        # for i in map:
        #         if i[-1] == ' ' or i[-1] == '\n':
        #             i = i[:-1]
        return score + PACMAN_MOVING_SCORE, map, overlap
    if player == 'W':
        x_next, y_next = choose_next_position(position, direction)
        if map[x_next][y_next] == 'P':
            score += PACMAN_EATEN_SCORE
        if overlap:
            map[x] = map[x][:y] + '.' + map[x][y + 1:]
            overlap = False
        else:
            map[x] = map[x][:y] + ' ' + map[x][y + 1:]
        if map[x_next][y_next] == '.':
            overlap = True
        map[x_next] = map[x_next][:y_next] + player + map[x_next][y_next + 1:]
        #print(map)
        # for i in map:
        #         if i[-1] == ' ' or i[-1] == '\n':
        #             i = i[:-1]
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
    
    
def check_end_of_game(map):
    counter_for_player_P = 0
    counter_for_player_W = 0
    counter_for_food = 0
    for i in map:
        for j in range(len(i)):
            if i[j] == 'P':
               counter_for_player_P += 1
            elif i[j] == 'W':
                counter_for_player_W += 1
            elif i[j] == '.':
                counter_for_food += 1
    if counter_for_food == 0:
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
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)