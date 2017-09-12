from board import Board

def game_loop(board):
    '''
    Game loop.
    :param board: board object that game is played on
    '''
    while True:
        board.print()
        game_state = board.detect_game_state()
        if game_state == Board.WIN:
            print ('you win')
            break
        elif game_state == Board.LOSE:
            print ('you lose')
            break
        else:
            while True:
                print('format: c/f, row, col')
                user_input = input('')
                items = user_input.split(',')
                if check_input(items):
                    print('wrong input')
                else:
                    op, row, col = parse_input(items)
                    board.update(op, row, col)
                    break

def check_input(items):
    '''
    Sanity check input items.
    :param items: three input strings
    :return: True if input is good. False otherwise
    '''
    if not len(items) == 3:
        return False
    elif not items[0] == 'c' or not items[0] == 'f':
        return False
    elif not is_int(items[1]) or not is_int(items[2]):
        return False
    elif items[1] < 0 or items[1] >= Board.HEIGHT:
        return False
    elif items[2] < 0 or items[2] >= Board.WIDTH:
        return False
    else:
        return True

def parse_input(items):
    '''
    Parse input items into three variables
    :param items: input items
    :return: three items
    '''
    return items[0], int(items[1]), int(items[2])

def is_int(item):
    """
    Check input item is an integer.
    :param item: input item
    :return: True if item is an integer. False if not.
    """
    try:
        num = int(item)
    except ValueError:
        return False
    return True

if __name__ == '__main__':
    board = Board()
    game_loop(board)