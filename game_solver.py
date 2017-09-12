from board import Board
from square import Square
import random
import itertools
import pyautogui

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

# Define mouse speed
MOUSE_SPEED = 0.15

# Define square coordinates
POSITIONS = [[object() for row in range(8)] for col in range(8)]
YCOORDS = [90, 111, 131, 150, 170, 190, 210, 230]
XCOORDS = [150, 172, 192, 212, 232, 252, 273, 293]
for row in range(8):
    for col in range(8):
        POSITIONS[row][col] = XCOORDS[col], YCOORDS[row]

def solve_game(board, auto):
    '''
    Main function for solving the minesweeper game
    :param board: board to be played with
    :return: True if game is solved successfully, false otherwise
    '''
    first_click(board, auto)
    game_state = board.detect_game_state()
    while not game_state == board.WIN and not game_state == board.LOSE:
        front_squares = []
        for row in range(0, board.height):
            for col in range(0, board.width):
                cur_square = board.squares[row][col]
                if is_int(cur_square.display()):
                    front_squares.append([cur_square, row, col])
        safest_operation(board, front_squares, auto)
        game_state = board.detect_game_state()
    if game_state == board.WIN:
        return True
    else:
        return False


def safest_operation(board, front_squares, auto):
    '''
    Perform the safest operation to current board
    :param board: board to be played with
    :param front_squares: list holding square in the margin of
    '''
    min_probability = 1.0
    safest_neighbor_blank_squares = None
    safest_op = None
    position = None
    need_to_guess = True
    blank_squares_combinations = []

    for square, row, col in front_squares:
        neighbor_blank_squares, neighbor_flags = get_neighbor_squares_info(board, square)
        neighbor_mines = int(square.display())
        if len(neighbor_blank_squares) == 0:
            pass
        else:
            if neighbor_mines - neighbor_flags > 0:
                probability = (neighbor_mines - neighbor_flags) / len(neighbor_blank_squares)
                if probability == 1.0:
                    safest_op = Board.FLAG
                    safest_neighbor_blank_squares = neighbor_blank_squares
                    random_pos = random.randrange(0, len(safest_neighbor_blank_squares))
                    position = safest_neighbor_blank_squares[random_pos]
                    need_to_guess = False
                    break
                else:
                    blank_squares_combinations.append((neighbor_blank_squares, itertools.combinations(neighbor_blank_squares, (neighbor_mines - neighbor_flags))))
                    if probability < min_probability:
                        min_probability = probability
                        safest_neighbor_blank_squares = neighbor_blank_squares
                        safest_op = Board.CLICK
            else:
                safest_op = Board.DOUBLE
                position = row, col
                need_to_guess = False
                break
    if need_to_guess:
        safest_neighbor_blank_squares, safest_op = find_safest_square_to_be_left_clicked(blank_squares_combinations, min_probability, safest_neighbor_blank_squares, safest_op)
    perform_safest_operation(board, position, safest_neighbor_blank_squares, safest_op, auto)


def find_safest_square_to_be_left_clicked(blank_squares_combinations, min_probability, safest_neighbor_blank_squares, safest_op):
    '''
    Find the safest square that should be left clicked
    :param blank_squares_combinations: list of pair of neighbor blank squares and its possible bomb combination
    :param min_probability: minimum probability that a click gets a bomb
    :param safest_neighbor_blank_squares: list of safest squares that can be clicked
    :param safest_op: safest operation like left click, right click, and left and right click
    :return: list of safest squares that can be clicked, safest operation
    '''
    pair_of_blank_squares_combinations = itertools.combinations(blank_squares_combinations, 2)
    for pair in pair_of_blank_squares_combinations:
        intersection = get_intersection(pair[0][0], pair[1][0])
        if not len(intersection) == 0:
            combined_set = combine(pair[0][0], pair[1][0])
            new_combinations = cartesian_product_no_contradiction(pair[0][1], pair[1][1], intersection)
            probability, safe_square = find_safer_operation_from_new_combination(combined_set, new_combinations)
            if probability < min_probability:
                min_probability = probability
                safest_op = Board.CLICK
                safest_neighbor_blank_squares = [safe_square]

    trio_of_blank_squares_combinations = itertools.combinations(blank_squares_combinations, 3)
    for trio in trio_of_blank_squares_combinations:
        intersection = get_intersection(trio[0][0], trio[1][0])
        if not len(intersection) == 0:
            combined_set = combine(trio[0][0], trio[1][0])
            new_combinations = cartesian_product_no_contradiction(trio[0][1], trio[1][1], intersection)
            intersection_2 = get_intersection(combined_set, trio[2][0])
            if not len(intersection_2) == 0:
                combined_set_2 = combine(combined_set, trio[2][0])
                new_combinations_2 = cartesian_product_no_contradiction(new_combinations, trio[2][1], intersection_2)
                probability, safe_square = find_safer_operation_from_new_combination(combined_set_2, new_combinations_2)
                if probability < min_probability:
                    min_probability = probability
                    safest_op = Board.CLICK
                    safest_neighbor_blank_squares = [safe_square]

    return safest_neighbor_blank_squares, safest_op


def perform_safest_operation(board, position, safest_neighbor_blank_squares, safest_op, auto):
    '''
    Perfrom the safest operation according to safest_op and safest_neighbor_blank_squares
    :param board: board that solver is playing with
    :param position: safest position to be clicked, used when no need to guess
    :param safest_neighbor_blank_squares: list of safest squares that can be clicked
    :param safest_op: safest operation like left click, right click, and left and right click
    '''
    if safest_op == Board.FLAG:
        if auto:
            x, y = POSITIONS[board.width - 1 - position[0]][position[1]]
            pyautogui.moveTo(x, y, duration=MOUSE_SPEED)
            pyautogui.rightClick(x, y)
        else:
            board.update(Board.FLAG, position[0], position[1])
        print(Board.FLAG, position[0], position[1])

    elif safest_op == Board.DOUBLE:
        if auto:
            x, y = POSITIONS[board.width - 1 - position[0]][position[1]]
            pyautogui.moveTo(x, y, duration=MOUSE_SPEED)
            pyautogui.doubleClick(x, y)
        else:
            board.update(Board.DOUBLE, position[0], position[1])
        print(Board.DOUBLE, position[0], position[1])

    elif safest_op == Board.CLICK:
        random_pos = random.randrange(0, len(safest_neighbor_blank_squares))
        position = safest_neighbor_blank_squares[random_pos]
        if auto:
            x, y = POSITIONS[board.width - 1 - position[0]][position[1]]
            pyautogui.moveTo(x, y, duration=MOUSE_SPEED)
            pyautogui.click(x, y)
        else:
            board.update(Board.CLICK, position[0], position[1])
        print(Board.CLICK, position[0], position[1])
    else:
        print('do nothing')
        pass


def get_neighbor_squares_info(board, square):
    '''
    Get neighbor blank squares and number of flags around current square
    :param square: current square
    :return: neighbor blank squares and number of flags around current square
    '''
    neighbors = square.nearby_squares()
    neighbor_flags = 0
    neighbor_blank_squares = []
    for row, col in neighbors:
        if board.squares[row][col].display() == Square.BLANK:
            neighbor_blank_squares.append((row, col))
        elif board.squares[row][col].display() == Square.FLAG:
            neighbor_flags += 1

    return neighbor_blank_squares, neighbor_flags

def first_click(board, auto):
    '''
    Perform the first random click on the board
    :param board: board to be played with
    '''
    row = random.randrange(0, board.height)
    col = random.randrange(0, board.width)
    if auto:
        x, y = POSITIONS[board.width - 1 - row][col]
        pyautogui.moveTo(x, y, duration=MOUSE_SPEED)
        pyautogui.click(x, y)
    else:
        board.update(Board.CLICK, row, col)
    print(Board.CLICK, row, col)

def find_safer_operation_from_new_combination(combined_set, new_combinations):
    '''
    Find safer operation by making use of info from two front squares
    :param combined_set: combined neighbor blank square of two front squares
    :param new_combinations: combinations of possible bombs
    :return: probability of current safest square and the square itself
    '''
    min_probability = 1.0
    safest_square = None
    if len(new_combinations) == 0:
        return 1.0, None
    else:
        for square in combined_set:
            occurrence = 0
            for combination in new_combinations:
                if square in combination:
                    occurrence += 1
            probability = occurrence / len(new_combinations)
            if probability < min_probability:
                min_probability = probability
                safest_square = square
        return min_probability, safest_square


def cartesian_product_no_contradiction(possible_combination_1, possible_combination_2, intersection):
    '''
    Do Cartesian product to the two combinations and then discard all contradicted results.
    A contradiction would be if, within the intersection of the areas, the two sets didn't have exactly the same mines.
    :param possible_combination_1: possible bombs combination 1
    :param possible_combination_2: possible bombs combination 2
    :param intersection: intersections of neighbor blank squares of two front squares
    :return: new possible bomb combinations
    '''
    filtered_crts_product = []
    for combination_1 in possible_combination_1:
        for combination_2 in possible_combination_2:
            new_combination = combine(combination_1, combination_2)
            intersection_bombs = get_intersection(new_combination, intersection)
            if squares_appear_in_intersection(intersection_bombs, combination_1) == squares_appear_in_intersection(intersection_bombs, combination_2):
                filtered_crts_product.append(new_combination)
    return filtered_crts_product

def squares_appear_in_intersection(intersection_bombs, combination):
    '''
    Get the set of suares from combination which appeared in bomb combination
    :param intersection_bombs: bomb intersection by new combination and intersection
    :param combination: possible bomb combination by info of one square
    :return: the set of suares from combination which appeared in bomb combination
    '''
    squares = []
    for square in intersection_bombs:
        if square in combination:
            squares.append(square)
    return set(squares)

def combine(set_1, set_2):
    '''
    Combine two sets to a unique one
    :param set_1: set 1
    :param set_2: set 2
    :return: one unique set
    '''
    new_set = list(set_2)
    if len(set_1) >= len(set_2):
        new_set = list(set_1)
    for square in set_2:
        if not square in set_1:
            new_set.append(square)
    return new_set

def get_intersection(set_1, set_2):
    '''
    Get intersection of two sets
    :param set_1: set 1
    :param set_2: set 2
    :return: intersection of two sets
    '''
    intersection = []
    for square in set_1:
        if square in set_2:
            intersection.append(square)
    return intersection

def is_int(i):
    """
    Check input item is an integer.
    :param i: input item
    :return: True if item is an integer. False if not.
    """
    try:
        num = int(i)
    except ValueError:
        return False
    return True


if __name__ == '__main__':
    count = 1
    size = [30, 16, 99]
    board = Board(size)
    print('turn ' + str(count) + ' started')

    while not solve_game(board, auto=False) and count <= 101:
        board.print()
        count += 1
        print('\n\nturn ' + str(count) + ' started')
        board = Board(size)
    board.print()

    print("game solved in " + str(count) + " times.")
